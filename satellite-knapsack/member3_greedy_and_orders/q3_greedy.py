"""MEMBER 3 - Question 3: value-per-kg greedy vs optimum (counterexample).
Run:  python member3_greedy_and_orders/q3_greedy.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import INSTANCE, CAPACITY, greedy_density, brute_force, fmt_kg

for stop in (True, False):
    names, v, m, p = greedy_density(INSTANCE, CAPACITY, stop_at_first_misfit=stop)
    tag = "stop at first misfit ('until full')" if stop else "skip misfits, keep scanning"
    print(f"Greedy [{tag}]: {names} value {v} mass {fmt_kg(m)} kg")
opt = brute_force(INSTANCE, CAPACITY)
print(f"Optimum: {opt[1]} value {opt[0]}")
g = greedy_density(INSTANCE, CAPACITY, stop_at_first_misfit=False)[1]
print(f"Greedy loses {opt[0]-g} value units even in its best variant -> greedy-choice property FAILS.")
print("Reason: P4 (6.1 kg) is skipped because it no longer fits after P1+P2+P3 (10.5 kg);")
print("the optimum drops P1 to make room for P4. Density order ignores 'wasted' capacity.")
