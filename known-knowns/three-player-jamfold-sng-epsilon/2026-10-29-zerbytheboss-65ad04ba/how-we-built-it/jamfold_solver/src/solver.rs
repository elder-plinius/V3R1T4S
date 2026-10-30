// Outer loop Policy Iteration & Newton-Raphson indifference polishing solver

use crate::cards::CardTables;
use crate::equity::EquityEngine;
use crate::eval::Evaluator;
use crate::stage::{EliminationConvention, StageSolver, StateStrategy};
use crate::state::{icm_3player, StateTable, NUM_POSITION_STATES, NUM_STATES};
use rayon::prelude::*;
use std::time::Instant;

pub struct GameSolver<'a> {
    pub state_table: StateTable,
    pub cards: &'a CardTables,
    pub equity: &'a EquityEngine,
    pub eval: &'a Evaluator,
    pub conv: EliminationConvention,
}

impl<'a> GameSolver<'a> {
    pub fn new(
        cards: &'a CardTables,
        equity: &'a EquityEngine,
        eval: &'a Evaluator,
        conv: EliminationConvention,
    ) -> Self {
        GameSolver {
            state_table: StateTable::new(),
            cards,
            equity,
            eval,
            conv,
        }
    }

    // Initialize value vector V0 using 3-player ICM across all 946 stack vectors
    pub fn init_v0(&self) -> Vec<f64> {
        let mut v = vec![0.0f64; NUM_POSITION_STATES];
        for (idx, &(s1, s2, s3)) in self.state_table.index_to_stack.iter().enumerate() {
            let icm = icm_3player(s1, s2, s3);
            v[idx * 3 + 0] = icm[0]; // BTN
            v[idx * 3 + 1] = icm[1]; // SB
            v[idx * 3 + 2] = icm[2]; // BB
        }
        v
    }

    // Run one outer-loop iteration: solves stage games at all 946 states in parallel
    pub fn solve_all_stages(
        &self,
        v: &[f64],
        num_stage_iters: usize,
    ) -> Vec<StateStrategy> {
        let stage_solver = StageSolver::new(self.cards, self.equity, self.eval, self.conv);

        self.state_table.index_to_stack.par_iter().map(|&(s1, s2, s3)| {
            stage_solver.solve_stage(s1, s2, s3, v, num_stage_iters, None)
        }).collect()
    }
}
