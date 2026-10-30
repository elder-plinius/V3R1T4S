// State space and ICM calculations for 3-player Jam/Fold SnG
// Total chips: 13,500 = 45 units of 300 chips.
// Non-terminal states: (s1, s2, s3) with s1 + s2 + s3 = 45, si >= 1. Total 946 states.
// Position-states in MDP: 946 * 3 = 2,838 states.

pub const TOTAL_CHIPS: u8 = 45;
pub const NUM_STATES: usize = 946;
pub const NUM_POSITION_STATES: usize = 2838;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct StackVector {
    pub s1: u8, // BTN stack in units (1..43)
    pub s2: u8, // SB stack in units (1..43)
    pub s3: u8, // BB stack in units (1..43)
}

#[inline(always)]
pub fn stack_to_index(s1: u8, s2: u8, _s3: u8) -> usize {
    let s1f = s1 as f64;
    let s2f = s2 as f64;
    (-0.5 * s1f * s1f + s1f * 44.5 + s2f - 45.0).round() as usize
}

pub struct StateTable {
    pub states: Vec<StackVector>,
    pub index_to_stack: Vec<(u8, u8, u8)>,
}

impl StateTable {
    pub fn new() -> Self {
        let mut states = Vec::with_capacity(NUM_STATES);
        let mut index_to_stack = vec![(0u8, 0u8, 0u8); NUM_STATES];

        for s1 in 1..44u8 {
            for s2 in 1..(45 - s1) {
                let s3 = 45 - s1 - s2;
                let idx = stack_to_index(s1, s2, s3);
                assert!(idx < NUM_STATES);
                states.push(StackVector { s1, s2, s3 });
                index_to_stack[idx] = (s1, s2, s3);
            }
        }
        assert_eq!(states.len(), NUM_STATES);

        StateTable {
            states,
            index_to_stack,
        }
    }
}

// 2-player ICM terminal values:
// 1st place gets $50, 2nd gets $30, 3rd gets $20 (already awarded to eliminated player).
// For the 2 survivors with stacks c_A, c_B (c_A + c_B = 45):
// V_A = 30 + 20 * (c_A / 45)
// V_B = 30 + 20 * (c_B / 45)
#[inline(always)]
pub fn icm_2player(c_a: u8, _c_b: u8) -> f64 {
    30.0 + 20.0 * (c_a as f64) / 45.0
}

// 3-player ICM for initial warm-start
pub fn icm_3player(s1: u8, s2: u8, s3: u8) -> [f64; 3] {
    let s = [s1 as f64, s2 as f64, s3 as f64];
    let total = 45.0;
    let payouts = [50.0, 30.0, 20.0];
    let mut vals = [0.0; 3];

    for i in 0..3 {
        let p1 = s[i] / total;
        let mut p2 = 0.0;
        for j in 0..3 {
            if j != i {
                p2 += (s[j] / total) * (s[i] / (total - s[j]));
            }
        }
        let mut p3 = 0.0;
        for j in 0..3 {
            if j == i { continue; }
            for k in 0..3 {
                if k == i || k == j { continue; }
                p3 += (s[j] / total) * (s[k] / (total - s[j])) * (s[i] / (total - s[j] - s[k]));
            }
        }
        vals[i] = payouts[0] * p1 + payouts[1] * p2 + payouts[2] * p3;
    }
    vals
}
