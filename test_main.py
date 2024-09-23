import unittest
import polars as pl
import os
from main import (
    load_dataset,
    generate_summary_statistics,
    group_by,
    build_histogram,
    save_to_markdown,
    print_head,
)


class TestPolarsFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dataset_path = "player_overview.csv"
        cls.df = load_dataset(cls.dataset_path)

    def test_load_dataset(self):
        """Test if dataset loads correctly."""
        self.assertIsNotNone(self.df)
        self.assertGreater(self.df.height, 0, "Dataframe is empty")

    def test_print_head(self):
        """Test if the head of the dataframe prints correctly."""
        head = print_head(self.df)
        self.assertEqual(len(head), 5, "Head does not return 5 rows")

    def test_summary_statistics(self):
        """Test if summary statistics are generated correctly."""
        summary_stats = generate_summary_statistics(self.df)
        self.assertGreater(summary_stats.width, 0, "Summary statistics are empty")

    def test_group_by(self):
        """Test if group_by function works for categorical columns."""
        group_result = group_by(self.df, "Position")
        self.assertGreater(len(group_result), 0, "Group by returned empty result")

    def test_build_histogram(self):
        """Test if the histogram is created and saved."""
        build_histogram(self.df, "Goals", "test_goals_histogram.png")
        self.assertTrue(os.path.exists("test_goals_histogram.png"))
        os.remove("test_goals_histogram.png")

    def test_save_to_markdown(self):
        """Test if summary statistics are saved to markdown."""
        summary_stats = generate_summary_statistics(self.df)
        save_to_markdown(summary_stats, "test_player_summary.md")
        self.assertTrue(os.path.exists("test_player_summary.md"))
        os.remove("test_player_summary.md")


if __name__ == "__main__":
    unittest.main()
