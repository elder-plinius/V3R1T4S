// 169 strategically distinct hand classes in Texas Hold'em
// Cards: 0..51. rank = c >> 2 (0..12, 0=2, 12=A), suit = c & 3 (0..3).

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum HandType {
    Pair,
    Suited,
    Offsuit,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct HandClass {
    pub r1: u8, // High rank: 0..12
    pub r2: u8, // Low rank: 0..12 (r1 >= r2)
    pub kind: HandType,
}

pub const NUM_HAND_CLASSES: usize = 169;

pub struct CardTables {
    pub classes: Vec<HandClass>,
    pub class_combos: Vec<Vec<[u8; 2]>>, // 169 lists of specific 2-card hands
    pub card_to_class: [[usize; 52]; 52],
    pub combos_2: [[u16; NUM_HAND_CLASSES]; NUM_HAND_CLASSES],
    pub cond_prob_2: [[f64; NUM_HAND_CLASSES]; NUM_HAND_CLASSES],
}

impl CardTables {
    pub fn new() -> Self {
        let mut classes = Vec::with_capacity(169);
        // Canonical ordering:
        // 13 pocket pairs (from AA down to 22)
        for r in (0..13).rev() {
            classes.push(HandClass { r1: r, r2: r, kind: HandType::Pair });
        }
        // 78 suited hands (AKs down to 32s)
        for r1 in (1..13).rev() {
            for r2 in (0..r1).rev() {
                classes.push(HandClass { r1, r2, kind: HandType::Suited });
            }
        }
        // 78 offsuit hands (AKo down to 32o)
        for r1 in (1..13).rev() {
            for r2 in (0..r1).rev() {
                classes.push(HandClass { r1, r2, kind: HandType::Offsuit });
            }
        }
        assert_eq!(classes.len(), 169);

        // Generate combos for each class
        let mut class_combos = Vec::with_capacity(169);
        for hc in &classes {
            let mut combos = Vec::new();
            match hc.kind {
                HandType::Pair => {
                    for s1 in 0..4u8 {
                        for s2 in (s1+1)..4u8 {
                            let c1 = (hc.r1 << 2) | s1;
                            let c2 = (hc.r2 << 2) | s2;
                            combos.push([c1, c2]);
                        }
                    }
                    assert_eq!(combos.len(), 6);
                }
                HandType::Suited => {
                    for s in 0..4u8 {
                        let c1 = (hc.r1 << 2) | s;
                        let c2 = (hc.r2 << 2) | s;
                        combos.push([c1, c2]);
                    }
                    assert_eq!(combos.len(), 4);
                }
                HandType::Offsuit => {
                    for s1 in 0..4u8 {
                        for s2 in 0..4u8 {
                            if s1 != s2 {
                                let c1 = (hc.r1 << 2) | s1;
                                let c2 = (hc.r2 << 2) | s2;
                                combos.push([c1, c2]);
                            }
                        }
                    }
                    assert_eq!(combos.len(), 12);
                }
            }
            class_combos.push(combos);
        }

        // Map any pair of cards (c1, c2) to class index
        let mut card_to_class = [[0usize; 52]; 52];
        for (c_idx, combos) in class_combos.iter().enumerate() {
            for &[c1, c2] in combos {
                card_to_class[c1 as usize][c2 as usize] = c_idx;
                card_to_class[c2 as usize][c1 as usize] = c_idx;
            }
        }

        // Precompute combos_2 and cond_prob_2
        let mut combos_2 = [[0u16; NUM_HAND_CLASSES]; NUM_HAND_CLASSES];
        let mut cond_prob_2 = [[0.0f64; NUM_HAND_CLASSES]; NUM_HAND_CLASSES];

        for c1 in 0..NUM_HAND_CLASSES {
            let n1 = class_combos[c1].len() as f64;
            for c2 in 0..NUM_HAND_CLASSES {
                let mut valid = 0u16;
                for &h1 in &class_combos[c1] {
                    for &h2 in &class_combos[c2] {
                        if h1[0] != h2[0] && h1[0] != h2[1] && h1[1] != h2[0] && h1[1] != h2[1] {
                            valid += 1;
                        }
                    }
                }
                combos_2[c1][c2] = valid;
                cond_prob_2[c1][c2] = (valid as f64) / (n1 * 1225.0);
            }
        }

        CardTables {
            classes,
            class_combos,
            card_to_class,
            combos_2,
            cond_prob_2,
        }
    }

    #[inline(always)]
    pub fn get_class(&self, c1: u8, c2: u8) -> usize {
        self.card_to_class[c1 as usize][c2 as usize]
    }
}
