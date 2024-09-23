import unittest
import polars as pl
import os
from main import (
    load_dataset,
    generate_summary_statistics,
    group_by,
    build_log_histogram,
    save_to_markdown,
    print_head,
)


class TestPolarsFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the dataset once before running the tests
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

    def test_build_log_histogram(self):
        """Test if the log histogram is created and saved."""
        output_file = "test_goals_log_histogram.png"
        build_log_histogram(self.df, "Goals", output_file)

        # Check if the file was created
        self.assertTrue(
            os.path.exists(output_file),
            "Logarithmic histogram image file was not created",
        )

        # Clean up the file after test
        os.remove(output_file)

    def test_save_to_markdown(self):
        """Test if summary statistics are saved to markdown."""
        summary_stats = generate_summary_statistics(self.df)
        output_file = "test_player_summary.md"
        save_to_markdown(summary_stats, output_file)

        # Check if the markdown file was created
        self.assertTrue(os.path.exists(output_file), "Markdown file was not created")

        # Clean up the markdown file after test
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
