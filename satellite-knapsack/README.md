# Batch 5 - Selecting satellite instruments (0/1 knapsack, real-valued masses)

**Technique chosen: Branch and Bound** with a fractional (LP-relaxation) bound.
Rejected: Greedy (counterexample on the instance), DP (needs a 0.1 g grid, pseudo-polynomial,
multiplies with a 2nd constraint), Backtracking without bound (2^n), Divide & Conquer (subproblems are not independent).

## Results on the given instance
| Question | Answer |
|---|---|
| Q1 table size | 15,000 g -> 7 x 15,001 = 105,007 cells; at the true 0.1 g precision -> 7 x 150,001 = 1,050,007 cells. Fine for n = 6, but pseudo-polynomial O(nW). |
| Q2 optimum | {P2, P3, P4}, value **174**, mass 14.1 kg. Best-first B&B generates 47 nodes (23 expanded), vs 64 complete selections / 127 tree nodes. |
| Q3 greedy | Stops at {P1,P2,P3} = 142 (10.5 kg). Even if it keeps scanning: {P1,P2,P3,P5} = 160. Optimum is 174, so greedy fails. |
| Q4 orders | DFS (stack): 47 nodes generated, optimum found at node 42; BFS (queue): 49 total, optimum found at node 24 but proved only at the end, frontier up to 8; best-first (heap): 47 total, optimum found at node 36. BFS *reaches* the optimum fastest here (a level-order coincidence); best-first is the best overall because the bound lets it stop as soon as the heap top cannot beat 174. See `q4_orders.py`. |
| Q5 + 35 W | {P2,P3,P4} needs 37 W -> infeasible. New optimum **172**: {P1,P3,P4} (13.4 kg, 33 W), tied with {P1,P3,P5,P6} (14.4 kg, 31 W). |

## Who does what (4 members)
| Member | Folder | Eight components + extras they own |
|---|---|---|
| 1 | `member1_problem_and_dp/` | (1) Problem modelling, (2) data-structure table, (4) rejection of DP and D&C, Q1 |
| 2 | `member2_branch_and_bound/` | (3) technique + proof of bounding property, (5) pseudocode, (6) trace, proof of correctness, Q2 |
| 3 | `member3_greedy_and_orders/` | (4) rejection of Greedy and Backtracking, Q3, Q4 (three orders + data structures) |
| 4 | `member4_power_and_experiments/` | (7) complexity, (8) changed requirement Q5, benchmark + plot, worst-case input, real-world reference |

Everyone reviews one other member's section (see GITHUB_GUIDE.md).

## Run
```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # only needed for the plot
python tests/test_all.py                                 # all algorithms agree with brute force
python member1_problem_and_dp/q1_formulation_dp.py
python member2_branch_and_bound/q2_solve_and_trace.py
python member3_greedy_and_orders/q3_greedy.py
python member3_greedy_and_orders/q4_orders.py
python member4_power_and_experiments/q5_power.py
python member4_power_and_experiments/benchmark.py        # -> results/timings.csv, results/timing_plot.png
python member4_power_and_experiments/worst_case.py
```
Shared code is in `src/core.py` (masses stored as integers in 0.1 g, so no floating-point errors).

## Notes for the report
* Worst case: all densities equal, all masses even, capacity odd -> the bound is never tight, B&B visits ~half of 2^(n+1) nodes (`worst_case.py`).
* Practical case: on random weakly-correlated instances B&B visits a few hundred nodes at n = 24 while backtracking needs ~10^6 at n = 20.
* Real-world reference to cite/compare: B&B for knapsack in Martello & Toth, *Knapsack Problems* (1990) (MT1 algorithm), and MILP solvers (e.g. CBC/SCIP/Gurobi) which use LP-relaxation bounds in the same way, plus cutting planes and presolve that this version lacks.
* Replace the numbers in your slides with your own run of the scripts (timings depend on the machine).
