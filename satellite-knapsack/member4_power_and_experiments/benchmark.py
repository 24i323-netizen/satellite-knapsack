"""MEMBER 4 - empirical analysis: B&B (ours) vs DP table and plain backtracking.
Run:  python member4_power_and_experiments/benchmark.py
Writes results/timings.csv and results/timing_plot.png (needs matplotlib).
"""
import csv, random, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from core import Item, UNITS_PER_KG, sort_by_density, branch_and_bound, dp_knapsack, backtracking

SIZES = [8, 12, 16, 20, 24]
BACKTRACK_MAX_N = 20           # beyond this plain backtracking takes too long


def random_instance(n, seed=1):
    rnd = random.Random(seed * 1000 + n)
    items = []
    for i in range(n):
        mass = rnd.randint(5_000, 50_000)                 # 0.5 - 5.0 kg, 0.1 g steps
        value = int(mass / 1000 * 10 + rnd.randint(-15, 15)) + 20   # weakly correlated
        items.append(Item(f"P{i+1}", mass, max(value, 1)))
    cap = sum(it.mass for it in items) // 2
    return items, cap


def timeit(fn, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter(); out = fn(); best = min(best, time.perf_counter() - t)
        if best > 2: break
    return best, out


rows = []
print(f"{'n':>3} {'B&B s':>10} {'DP s':>10} {'backtrack s':>12} {'B&B nodes':>10} {'backtrack nodes':>16}")
for n in SIZES:
    items, cap = random_instance(n)
    srt = sort_by_density(items)
    tb, rb = timeit(lambda: branch_and_bound(srt, cap, strategy="dfs"))
    td, rd = timeit(lambda: dp_knapsack(items, cap), repeats=1)
    assert rb["best"] == rd[0], (n, rb["best"], rd[0])
    if n <= BACKTRACK_MAX_N:
        tk, rk = timeit(lambda: backtracking(items, cap), repeats=1)
        assert rk[0] == rb["best"]
        kn = rk[1]
    else:
        tk, kn = float("nan"), float("nan")
    rows.append((n, tb, td, tk, rb["stats"]["generated"], kn))
    print(f"{n:>3} {tb:>10.5f} {td:>10.4f} {tk:>12.4f} {rb['stats']['generated']:>10} {kn:>16}")

out = ROOT / "results"; out.mkdir(exist_ok=True)
with open(out / "timings.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n", "bnb_seconds", "dp_seconds", "backtracking_seconds", "bnb_nodes", "backtracking_nodes"])
    w.writerows(rows)

try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ns = [r[0] for r in rows]
    plt.figure(figsize=(7, 4.5))
    plt.semilogy(ns, [r[1] for r in rows], "o-", label="Branch & bound (ours)")
    plt.semilogy(ns, [r[2] for r in rows], "s-", label="DP table, 0.1 g grid (rejected)")
    bt = [(r[0], r[3]) for r in rows if r[3] == r[3]]
    plt.semilogy([a for a, _ in bt], [b for _, b in bt], "^-", label="Plain backtracking (rejected)")
    a0, b0 = bt[1]
    plt.semilogy(ns, [b0 * 2 ** (n - a0) for n in ns], "k--", alpha=.5, label=r"reference $c\cdot 2^n$")
    plt.xlabel("number of instruments n"); plt.ylabel("running time (s, log scale)")
    plt.title("Running time vs n"); plt.grid(True, which="both", alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig(out / "timing_plot.png", dpi=150)
    print("saved results/timing_plot.png")
except ImportError:
    print("matplotlib not installed: run  pip install matplotlib  and re-run to get the plot.")
