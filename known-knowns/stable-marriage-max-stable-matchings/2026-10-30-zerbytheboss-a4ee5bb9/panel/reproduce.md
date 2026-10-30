context: subagent

Independent reproduction and verification of the claimed stable marriage instance of order n = 17:

1. Parsed `claim/object/instance_n17.txt`:
   - Line count: exactly 34 non-empty lines (17 men's preference lists followed by 17 women's preference lists).
   - Strict completeness: each row contains exactly 17 integer entries.
   - Permutation check: sorted row elements equal `[1, 2, ..., 17]` for every single row. All preference lists are strict, complete permutations.

2. Evaluated stable matchings using Method 1 (Irving-Leather rotation poset closed-set enumeration with memoized bitsets):
   - Rotations discovered: 121
   - Memoized states: 32,886
   - Exact count: 206,728 stable matchings (0.0057s).

3. Evaluated stable matchings using Method 2 (Gusfield stable matching lattice traversal with direct blocking-pair stability verification of every visited matching):
   - Starting from the man-optimal matching M0 produced by Gale-Shapley: stable.
   - Traversed all downward edges via exposed rotation eliminations to woman-optimal matching Mz: stable.
   - Every intermediate matching visited was verified to contain zero blocking pairs against the raw preference rank tables.
   - Exact count: 206,728 stable matchings (0.1188s in C, 14.05s in Python standard library).

4. Numerical Agreement:
   - Both independent algorithms agree exactly on 206,728 stable matchings.

pass: true
