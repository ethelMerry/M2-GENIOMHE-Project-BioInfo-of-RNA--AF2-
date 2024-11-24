import os
import pandas as pd
from scipy.stats import spearmanr, pearsonr

def compute_correlations(file_path, target_column, other_columns):
    """
    Compute Spearman and Pearson correlation coefficients between a target column and a list of other columns.
    :param file_path: Path to the CSV file containing the data.
    :param target_column: Name of the column to compute correlations with.
    :param other_columns: List of column names to compute correlations against the target column.
    :return: Dictionary of correlation results.
    :outfile: Detailed correlation results
    """
    try:
        # Load CSV and clean column names
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip()  # Strip leading/trailing spaces
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

    # Check for missing columns
    missing_columns = [col for col in [target_column] + other_columns if col not in data.columns]
    if missing_columns:
        print(f"Error: Missing columns in the file {file_path}: {missing_columns}")
        return None

    # Remove rows with NaN or inf values in the relevant columns
    data = data[[target_column] + other_columns].replace([float("inf"), float("-inf")], None).dropna()

    results = {}
    for col in other_columns:
        x = data[target_column]
        y = data[col]

        # Compute correlations
        spearman_corr, spearman_p = spearmanr(x, y)
        pearson_corr, pearson_p = pearsonr(x, y)

        # Save results
        results[col] = {
            "Spearman Correlation": spearman_corr,
            "Spearman P-value": spearman_p,
            "Pearson Correlation": pearson_corr,
            "Pearson P-value": pearson_p,
        }

    return results

def save_detailed_results_to_file(results, output_file="detailed_correlation_results.txt"):
    """
    Save correlation results to a file with a more readable and detailed format.
    :param results: Dictionary of correlation results grouped by file.
    :param output_file: Path to save the results.
    """
    with open(output_file, "w") as f:
        f.write("Detailed Correlation Results\n")
        f.write("=" * 80 + "\n\n")
        
        for file_name, correlations in results.items():
            f.write(f"File: {file_name}\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Metric':<10} {'Spearman Correlation':<20} {'Spearman P-value':<20} {'Pearson Correlation':<20} {'Pearson P-value':<20}\n")
            f.write("=" * 80 + "\n")
            
            for metric, corr_values in correlations.items():
                f.write(
                    f"{metric:<10} {corr_values['Spearman Correlation']:<20.3f} "
                    f"{corr_values['Spearman P-value']:<20.3e} "
                    f"{corr_values['Pearson Correlation']:<20.3f} "
                    f"{corr_values['Pearson P-value']:<20.3e}\n"
                )
            
            f.write("\n")
            f.write("-" * 80 + "\n")
        
        print(f"Detailed results saved to {output_file}")

def process_directory_detailed(input_dir, target_column, other_columns, output_file="detailed_correlation_results.txt"):
    """
    Process all CSV files in a directory and compute correlations for each, saving detailed results.
    :param input_dir: Path to the directory containing CSV files.
    :param target_column: Name of the column to compute correlations with.
    :param other_columns: List of column names to compute correlations against the target column.
    :param output_file: Path to save the detailed correlation results.
    """
    if not os.path.exists(input_dir):
        print(f"Error: Directory {input_dir} does not exist.")
        return

    results = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing file: {file_path}")
            correlations = compute_correlations(file_path, target_column, other_columns)
            if correlations is not None:
                results[file_name] = correlations

    save_detailed_results_to_file(results, output_file)

if __name__ == "__main__":
    input_dir = input("Enter the directory containing CSV files: ")
    target_column = "RSSD"
    other_columns = ["RMSD", "MCQ", "TM-score"]
    output_file = "detailed_correlation_results.txt"

    process_directory_detailed(input_dir, target_column, other_columns, output_file)