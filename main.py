import polars as pl
import matplotlib.pyplot as plt


# Load dataset from csv file using Polars
def load_dataset(dataset_path):
    """
    Loads a dataset from a given path using Polars.

    :param dataset_path: str, path to the dataset
    :return: Polars DataFrame
    """
    df = pl.read_csv(dataset_path)
    return df


# Print the head of the dataset
def print_head(df, n=5):
    """
    Prints and returns the first n rows of the dataframe.

    :param df: Polars DataFrame
    :param n: int, number of rows to display (default is 5)
    :return: Polars DataFrame head
    """
    data_head = df.head(n)
    print(data_head)
    return data_head


# Generate descriptive statistics: mean, median, std for numeric columns
def generate_summary_statistics(df):
    """
    Generates summary statistics (mean, median, std) for numeric columns in the dataframe.

    :param df: Polars DataFrame
    :return: Polars DataFrame with summary statistics
    """
    summary_stats = df.select(
        [
            pl.col(column).mean().alias(f"{column}_mean")
            for column, dtype in df.schema.items()
            if dtype in [pl.Float64, pl.Int64]
        ]
        + [
            pl.col(column).median().alias(f"{column}_median")
            for column, dtype in df.schema.items()
            if dtype in [pl.Float64, pl.Int64]
        ]
        + [
            pl.col(column).std().alias(f"{column}_std")
            for column, dtype in df.schema.items()
            if dtype in [pl.Float64, pl.Int64]
        ]
    )
    return summary_stats


# Group by a categorical column and count occurrences
def group_by(df, column_name):
    """
    Groups by a categorical column and counts occurrences.

    :param df: Polars DataFrame
    :param column_name: str, column to group by
    :return: Polars DataFrame with value counts
    """
    return df.select(pl.col(column_name).value_counts())


# Create a logarithmic histogram for a given numeric column
def build_log_histogram(df, column_name, output_file):
    """
    Creates a logarithmic histogram for a specified numeric column.

    :param df: Polars DataFrame
    :param column_name: str, column to build histogram for
    :param output_file: str, path to save the histogram image
    """
    column_data = df[column_name].to_numpy()

    # Create the histogram with a logarithmic scale on the x-axis
    plt.hist(
        column_data, bins=10, edgecolor="white", log=True
    )  # Use log scale for y-axis

    # Set labels and title
    plt.xlabel(column_name)
    plt.ylabel("Frequency (Log Scale)")
    plt.title(f"{column_name} Logarithmic Histogram")

    # Save and show the plot
    plt.savefig(output_file)
    plt.show()


# Save summary statistics to markdown
def save_to_markdown(summary_stats, output_file):
    """
    Saves the summary statistics to a markdown file.

    :param summary_stats: Polars DataFrame with summary statistics
    :param output_file: str, path to save the markdown file
    """
    markdown_table = str(summary_stats)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("# Summary Statistics\n")
        file.write(markdown_table)


# Main function to execute the script
def main():
    dataset_path = "player_overview.csv"
    dataframe = load_dataset(dataset_path)

    if dataframe is not None:
        # Print the head of the dataset
        print_head(dataframe)

        # Generate and print summary statistics
        summary_stats = generate_summary_statistics(dataframe)
        print(summary_stats)

        # Group by example columns
        print(group_by(dataframe, "Position"))
        print(group_by(dataframe, "Nationality"))

        # Build and save histogram for "Goals"
        build_log_histogram(dataframe, "Goals", "goals_log_histogram.png")

        # Save the summary statistics to markdown
        save_to_markdown(summary_stats, "player_summary.md")
    else:
        print("Dataset was not successfully loaded")


# Run the main function
if __name__ == "__main__":
    main()
