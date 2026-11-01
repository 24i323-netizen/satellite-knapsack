"""MEMBER 4 - worst-case input for branch and bound.

Construction: every value equals its mass (all densities identical) and all masses
are EVEN while the capacity is ODD.  The fractional bound is then always exactly C,
but the true optimum is at most C-1, so floor(bound) > best forever and NO internal node
is pruned by the bound (only overweight and leaf nodes drop out): the search explores every feasible partial
selection -> Theta(2^n).
Run:  python member4_power_and_experiments/worst_case.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import Item, branch_and_bound, sort_by_density


def worst_case(n):
    items = [Item(f"W{i+1}", 2 * (10_000 + 137 * i), 2 * (10_000 + 137 * i)) for i in range(n)]
    cap = sum(it.mass for it in items) // 2
    if cap % 2 == 0:
        cap += 1
    return sort_by_density(items), cap


print(f"{'n':>3} {'generated':>10} {'full tree 2^(n+1)-1':>20} {'fraction':>9} {"pruned (leaves)":>16} {'seconds':>9}")
for n in (8, 10, 12, 14, 16, 18):
    items, cap = worst_case(n)
    t = time.perf_counter()
    r = branch_and_bound(items, cap, strategy="dfs")
    dt = time.perf_counter() - t
    st = r["stats"]
    full = 2 ** (n + 1) - 1
    print(f"{n:>3} {st['generated']:>10} {full:>20} {st['generated']/full:>9.2f} {st['pruned']:>16} {dt:>9.3f}")
print("\nNodes roughly double with each +1 in n: exponential, as predicted by the worst-case bound O(2^n).")
