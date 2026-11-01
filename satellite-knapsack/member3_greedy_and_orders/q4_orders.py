"""MEMBER 3 - Question 4: three exploration orders + data structure for each.
Run:  python member3_greedy_and_orders/q4_orders.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import INSTANCE, CAPACITY, sort_by_density, branch_and_bound

items = sort_by_density(INSTANCE)
ds = {"dfs": "stack (list)", "bfs": "FIFO queue (deque)", "best": "priority queue (binary heap on bound)"}
print(f"{'order':<8}{'data structure':<40}{'generated':>10}{'expanded':>10}{'pruned':>8}{'max frontier':>14}{'gen. when optimum found':>26}")
for s in ("dfs", "bfs", "best"):
    r = branch_and_bound(items, CAPACITY, strategy=s)
    st = r["stats"]
    print(f"{s:<8}{ds[s]:<40}{st['generated']:>10}{st['expanded']:>10}{st['pruned']:>8}{st['max_frontier']:>14}{st['gen_at_best']:>26}")
    assert r["best"] == 174
print("\nTime/space of the structures (n = frontier size):")
print("  stack  : push O(1), pop O(1), space O(depth) = O(n)")
print("  queue  : push O(1), pop O(1), space up to O(2^n) (a whole level)")
print("  heap   : push O(log n), pop O(log n), space up to O(2^n) in the worst case")
