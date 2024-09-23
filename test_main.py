import unittest
import polars as pl
import os


class TestPolarsDescriptiveStats(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method runs once before any test
        cls.file_path = (
            "/Users/liuliangcheng/Desktop/Duke/ids_de_polars/player_overview.csv"
        )
        cls.df = pl.read_csv(cls.file_path)

    def test_data_loading(self):
        """Test if the CSV file is loaded correctly"""
        self.assertIsNotNone(self.df, "DataFrame is None")
        self.assertGreater(self.df.height, 0, "DataFrame is empty")

    def test_summary_statistics(self):
        """Test if summary statistics are calculated correctly"""
        summary_stats = self.df.select(
            [
                pl.col(column).mean().alias(f"{column}_mean")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
            + [
                pl.col(column).median().alias(f"{column}_median")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
            + [
                pl.col(column).std().alias(f"{column}_std")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
        )

        # Check if summary statistics DataFrame has data
        self.assertGreater(summary_stats.height, 0, "Summary statistics are empty")
        self.assertGreaterEqual(
            summary_stats.width,
            6,
            "Summary statistics does not contain expected number of columns",
        )

    def test_csv_output(self):
        """Test if the CSV file with summary statistics is created"""
        summary_stats = self.df.select(
            [
                pl.col(column).mean().alias(f"{column}_mean")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
            + [
                pl.col(column).median().alias(f"{column}_median")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
            + [
                pl.col(column).std().alias(f"{column}_std")
                for column, dtype in self.df.schema.items()
                if dtype in [pl.Float64, pl.Int64]
            ]
        )
        # Write the statistics to a CSV file
        summary_stats.write_csv("test_summary_statistics.csv")

        # Test if the file was created
        self.assertTrue(
            os.path.exists("test_summary_statistics.csv"),
            "Summary statistics CSV file was not created",
        )

        # Optionally, clean up the file after test
        os.remove("test_summary_statistics.csv")


if __name__ == "__main__":
    unittest.main()
