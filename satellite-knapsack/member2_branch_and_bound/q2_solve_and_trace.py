"""MEMBER 2 - Question 2: optimal selection by branch and bound + full trace.
Run:  python member2_branch_and_bound/q2_solve_and_trace.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import (INSTANCE, CAPACITY, sort_by_density, branch_and_bound,
                  brute_force, totals, fmt_kg)

items = sort_by_density(INSTANCE)
print("Items sorted by value per kg:")
for it in items:
    print(f"  {it.name}: {fmt_kg(it.mass):>4} kg  value {it.value:>3}  density {it.density:6.3f}")

res = branch_and_bound(items, CAPACITY, strategy="best", trace=True)
print("\nBEST-FIRST BRANCH & BOUND TRACE")
print("\n".join(res["log"]))

v, m, p = totals(items, res["best_set"])
s = res["stats"]
print(f"\nOPTIMUM: {res['best_set']}  value {v}  mass {fmt_kg(m)} kg")
print(f"Nodes generated/examined : {s['generated']}  (vs 2^6 = 64 complete selections; full tree has 127 nodes)")
print(f"Nodes expanded           : {s['expanded']}")
print(f"Nodes pruned             : {s['pruned']}   infeasible (overweight): {s['infeasible']}")
bf = brute_force(INSTANCE, CAPACITY)
assert bf[0] == res["best"], "B&B disagrees with brute force!"
print(f"Verified against brute force: {bf[0]} {bf[1]}")
