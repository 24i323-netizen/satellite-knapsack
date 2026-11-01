import sys, random, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from core import *


class T(unittest.TestCase):
    def test_instance_optimum(self):
        bf = brute_force(INSTANCE, CAPACITY)
        self.assertEqual(bf[0], 174)
        self.assertEqual(bf[1], [("P2", "P3", "P4")])

    def test_all_strategies_match_brute_force(self):
        items = sort_by_density(INSTANCE)
        for s in ("dfs", "bfs", "best"):
            self.assertEqual(branch_and_bound(items, CAPACITY, strategy=s)["best"], 174)
            r = branch_and_bound(items, CAPACITY, POWER_CAP, strategy=s)
            self.assertEqual(r["best"], brute_force(INSTANCE, CAPACITY, POWER_CAP)[0])

    def test_greedy(self):
        self.assertEqual(greedy_density(INSTANCE, CAPACITY)[1], 142)
        self.assertEqual(greedy_density(INSTANCE, CAPACITY, stop_at_first_misfit=False)[1], 160)

    def test_dp_matches(self):
        self.assertEqual(dp_knapsack(INSTANCE, CAPACITY)[0], 174)

    def test_random_agreement(self):
        rnd = random.Random(7)
        for _ in range(60):
            n = rnd.randint(3, 11)
            items = [Item(f"x{i}", rnd.randint(1000, 9000), rnd.randint(1, 60), rnd.randint(1, 12)) for i in range(n)]
            cap = sum(i.mass for i in items) // 2
            pc = sum(i.power for i in items) // 2
            srt = sort_by_density(items)
            for s in ("dfs", "bfs", "best"):
                self.assertEqual(branch_and_bound(srt, cap, strategy=s)["best"], brute_force(items, cap)[0])
                self.assertEqual(branch_and_bound(srt, cap, pc, strategy=s)["best"], brute_force(items, cap, pc)[0])


if __name__ == "__main__":
    unittest.main()
