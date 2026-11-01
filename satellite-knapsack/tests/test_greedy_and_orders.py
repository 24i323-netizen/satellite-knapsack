"""Tests for Member 3: greedy selection and search exploration orders."""

import unittest

from src.core import (
    INSTANCE,
    CAPACITY,
    greedy_density,
    brute_force,
    branch_and_bound,
    sort_by_density,
    totals,
)


class TestGreedyAndOrders(unittest.TestCase):

    def test_greedy_is_not_optimal_for_project_instance(self):
        greedy = greedy_density(
            INSTANCE, CAPACITY, stop_at_first_misfit=False
        )
        optimal = brute_force(INSTANCE, CAPACITY)

        self.assertLess(greedy[1], optimal[0])

    def test_greedy_respects_capacity(self):
        names, value, mass, power = greedy_density(
            INSTANCE, CAPACITY, stop_at_first_misfit=False
        )
        self.assertLessEqual(mass, CAPACITY)
        self.assertGreaterEqual(value, 0)

    def test_both_greedy_variants_respect_capacity(self):
        for stop in (True, False):
            with self.subTest(stop_at_first_misfit=stop):
                names, value, mass, power = greedy_density(
                    INSTANCE, CAPACITY, stop_at_first_misfit=stop
                )
                self.assertLessEqual(mass, CAPACITY)

    def test_all_search_orders_find_optimum(self):
        optimal_value = brute_force(INSTANCE, CAPACITY)[0]
        items = sort_by_density(INSTANCE)

        for strategy in ("dfs", "bfs", "best"):
            with self.subTest(strategy=strategy):
                result = branch_and_bound(
                    items, CAPACITY, strategy=strategy
                )
                self.assertEqual(result["best"], optimal_value)

    def test_all_search_orders_return_feasible_selection(self):
        items = sort_by_density(INSTANCE)

        for strategy in ("dfs", "bfs", "best"):
            with self.subTest(strategy=strategy):
                result = branch_and_bound(
                    items, CAPACITY, strategy=strategy
                )
                value, mass, power = totals(
                    INSTANCE, result["best_set"]
                )
                self.assertEqual(value, result["best"])
                self.assertLessEqual(mass, CAPACITY)

    def test_search_statistics_are_consistent(self):
        items = sort_by_density(INSTANCE)

        for strategy in ("dfs", "bfs", "best"):
            with self.subTest(strategy=strategy):
                result = branch_and_bound(
                    items, CAPACITY, strategy=strategy
                )
                stats = result["stats"]

                self.assertGreaterEqual(stats["generated"], 1)
                self.assertGreaterEqual(stats["expanded"], 0)
                self.assertGreaterEqual(stats["pruned"], 0)
                self.assertGreaterEqual(stats["max_frontier"], 1)


if __name__ == "__main__":
    unittest.main()
