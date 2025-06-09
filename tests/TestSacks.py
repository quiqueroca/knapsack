import os
import unittest
from main import read_knapsack_items, read_sack, calculate_sack
from config import MAX_VOLUME, MAX_WEIGHT

class TestSacks(unittest.TestCase):
    def setUp(self):
        self.knapsack_items_path = "data/knapsack_items.csv"
        self.sacks_folder = "sacks/"
        self.max_weight = MAX_WEIGHT
        self.max_volume = MAX_VOLUME
        self.knapsack_items = read_knapsack_items(self.knapsack_items_path)

    def test_sacks_within_limits(self):
        for sack_file in os.listdir(self.sacks_folder):
            sack_path = os.path.join(self.sacks_folder, sack_file)
            sack = read_sack(sack_path)

            total_value, total_weight, total_volume = calculate_sack(sack, self.knapsack_items)

            with self.subTest(sack_file=sack_file):
                self.assertLessEqual(total_weight, self.max_weight, f"Sack {sack_file} exceeds MAX_WEIGHT")
                self.assertLessEqual(total_volume, self.max_volume, f"Sack {sack_file} exceeds MAX_VOLUME")

    def test_sacks_no_repeated_items(self):
        for sack_file in os.listdir(self.sacks_folder):
            sack_path = os.path.join(self.sacks_folder, sack_file)
            sack = read_sack(sack_path)

            with self.subTest(sack_file=sack_file):
                self.assertEqual(len(sack), len(set(sack)), f"Sack {sack_file} has repeated items")
