"""MEMBER 4 - Question 5: add the 35 W power limit and re-solve.
Run:  python member4_power_and_experiments/q5_power.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import (INSTANCE, CAPACITY, POWER_CAP, sort_by_density,
                  branch_and_bound, brute_force, totals, fmt_kg)

items = sort_by_density(INSTANCE)
old = ("P2", "P3", "P4")
v, m, p = totals(items, old)
print(f"Old optimum {old}: value {v}, mass {fmt_kg(m)} kg, power {p} W -> "
      f"{'violates' if p > POWER_CAP else 'meets'} the {POWER_CAP} W limit")

for s in ("dfs", "bfs", "best"):
    r = branch_and_bound(items, CAPACITY, POWER_CAP, strategy=s, trace=(s == "best"))
    if s == "best":
        print("\nBEST-FIRST TRACE (bound = min(mass-relaxation, power-relaxation))")
        print("\n".join(r["log"]))
    v, m, p = totals(items, r["best_set"])
    print(f"\n[{s}] best {r['best_set']} value {v} mass {fmt_kg(m)} kg power {p} W | "
          f"generated {r['stats']['generated']} expanded {r['stats']['expanded']}")

bf = brute_force(INSTANCE, CAPACITY, POWER_CAP)
print(f"\nBrute force: optimum {bf[0]}; ALL optimal sets: {bf[1]}; feasible subsets {bf[2]}/64")
print("Dynamic programming would now need a 2-D capacity table (kg x W): the cells multiply;")
print("branch and bound only needs one more feasibility test and a min() of two bounds.")
