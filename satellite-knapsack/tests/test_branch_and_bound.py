import unittest

from src.core import Item, branch_and_bound, sort_by_density, totals


class TestBranchAndBoundEdgeCases(unittest.TestCase):

    def test_empty_items(self):
        result = branch_and_bound([], 100, strategy="best")
        self.assertEqual(result["best"], 0)
        self.assertEqual(result["best_set"], ())

    def test_zero_capacity(self):
        items = [
            Item("A", 10, 50, 5),
            Item("B", 20, 80, 8)
        ]
        result = branch_and_bound(items, 0, strategy="best")
        self.assertEqual(result["best"], 0)
        self.assertEqual(result["best_set"], ())

    def test_exact_capacity(self):
        items = [
            Item("A", 40, 100, 5),
            Item("B", 60, 150, 8)
        ]
        result = branch_and_bound(items, 100, strategy="best")
        self.assertEqual(result["best"], 250)
        self.assertEqual(set(result["best_set"]), {"A", "B"})

    def test_item_exceeding_capacity(self):
        items = [Item("A", 101, 100, 5)]
        result = branch_and_bound(items, 100, strategy="best")
        self.assertEqual(result["best"], 0)
        self.assertEqual(result["best_set"], ())

    def test_power_constraint(self):
        items = [
            Item("A", 30, 100, 20),
            Item("B", 30, 90, 20)
        ]
        result = branch_and_bound(items, 100, 30, strategy="best")
        self.assertEqual(result["best"], 100)
        self.assertEqual(result["best_set"], ("A",))

    def test_selected_items_respect_constraints(self):
        items = [
            Item("A", 20, 60, 5),
            Item("B", 30, 80, 10),
            Item("C", 40, 90, 15)
        ]
        capacity = 60
        power_capacity = 20

        result = branch_and_bound(
            sort_by_density(items),
            capacity,
            power_capacity,
            strategy="best"
        )

        value, mass, power = totals(items, result["best_set"])

        self.assertEqual(value, result["best"])
        self.assertLessEqual(mass, capacity)
        self.assertLessEqual(power, power_capacity)


if __name__ == "__main__":
    unittest.main()
