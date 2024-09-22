import polars as pl

# Load your CSV file
file_path = "/Users/liuliangcheng/Desktop/Duke/ids_de_polars/player_overview.csv"

# Read the dataset using Polars
df = pl.read_csv(file_path)

# Generate descriptive statistics: mean, median, and standard deviation for numeric columns
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

# Print the summary statistics
print(summary_stats)

# Optionally, save the summary statistics to a new CSV file
summary_stats.write_csv("summary_statistics.csv")
import matplotlib.pyplot as plt

# Convert one of the columns (e.g., 'Goals') to a NumPy array for plotting
goals_data = df["Goals"].to_numpy()

# Create a histogram
plt.hist(goals_data, bins=10, color="blue")
plt.title("Goals Distribution")
plt.xlabel("Goals")
plt.ylabel("Frequency")
plt.savefig("goals_histogram.png")  # Save the histogram
plt.show()
