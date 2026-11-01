"""MEMBER 1 - Question 1: formal model + size of the gram-table DP.
Run:  python member1_problem_and_dp/q1_formulation_dp.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import INSTANCE, CAPACITY, UNITS_PER_KG, dp_knapsack, brute_force, fmt_kg

n = len(INSTANCE)
print("PROBLEM MODEL (0/1 knapsack - an OPTIMISATION problem)")
print("  Input : n instruments, real mass m_i (0.1 g precision), value v_i, capacity C = 15.0 kg")
print("  Output: x in {0,1}^n")
print("  Max   : sum v_i x_i      s.t.  sum m_i x_i <= C")
print("  Decision version 'is value >= K reachable?' is NP-complete.\n")

for label, units_per_kg in [("whole grams", 1000), ("0.1 g (true precision)", 10_000)]:
    W = 15 * units_per_kg
    cells = (n + 1) * (W + 1)
    print(f"Table in {label}: W = {W:,} columns, {n+1} rows -> {cells:,} cells")
print("\nScaling: cells = (n+1)(W+1); W is a NUMBER, not its bit-length -> pseudo-polynomial.")
for nn in (6, 100, 1000):
    print(f"  n={nn:<5} at 0.1 g: {(nn+1)*(15*UNITS_PER_KG+1):>14,} cells")
print("Acceptable for 6 items (about 1e6 cells), but not a principled method:")
print("  halving the measurement error doubles W; masses must be rounded to a grid;")
print("  any extra decimal of precision multiplies the table by 10.\n")

val, names, cells = dp_knapsack(INSTANCE, CAPACITY)
print(f"DP result (0.1 g grid): value {val}, set {names}, cells = {cells:,}")
bf = brute_force(INSTANCE, CAPACITY)
print(f"Brute-force check     : value {bf[0]}, sets {bf[1]}, feasible subsets {bf[2]} of {2**n}")
