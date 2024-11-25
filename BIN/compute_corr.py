import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt


def ensure_dir_exists(file_path):
    """
    Ensure the directory for a given file path exists. Create it if it doesn't.
    :param file_path: The file path for which the directory needs to be ensured.
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def compute_correlations(data_file):
    """
    Compute Pearson and Spearman correlations between CG-RMSD and other metrics (RMSD, MCQ, TM-score).
    Handle missing or infinite values in the data.
    :param data_file: Path to the CSV file containing CG-RMSD and metrics.
    :return: Correlation results as a dictionary.
    """
    # Load the merged CSV file
    data = pd.read_csv(data_file)

    # Extract relevant columns
    cg_rmsd = data["rssd"]
    rmsd = data["RMSD"]
    mcq = data["MCQ"]
    tm_score = data["TM-score"]

    # Remove rows with NaN or inf values
    valid_data = data[
        np.isfinite(cg_rmsd) &
        np.isfinite(rmsd) &
        np.isfinite(mcq) &
        np.isfinite(tm_score)
    ]

    if valid_data.empty:
        raise ValueError("Data contains only NaN or inf values after filtering. Cannot compute correlations.")

    # Extract cleaned columns
    cg_rmsd = valid_data["rssd"]
    rmsd = valid_data["RMSD"]
    mcq = valid_data["MCQ"]
    tm_score = valid_data["TM-score"]

    # Compute correlations
    correlations = {
        "RMSD": {
            "pearson": pearsonr(cg_rmsd, rmsd),
            "spearman": spearmanr(cg_rmsd, rmsd),
        },
        "MCQ": {
            "pearson": pearsonr(cg_rmsd, mcq),
            "spearman": spearmanr(cg_rmsd, mcq),
        },
        "TM-score": {
            "pearson": pearsonr(cg_rmsd, tm_score),
            "spearman": spearmanr(cg_rmsd, tm_score),
        },
    }

    return correlations


def plot_correlations(data_file, output_folder):
    """
    Plot scatter plots of CG-RMSD vs other metrics and save them to the specified folder.
    :param data_file: Path to the CSV file containing CG-RMSD and metrics.
    :param output_folder: Folder to save the scatter plot images.
    """
    # Ensure the output folder exists
    ensure_dir_exists(os.path.join(output_folder, "dummy_file"))

    # Load the merged CSV file
    data = pd.read_csv(data_file)

    # Extract relevant columns
    cg_rmsd = data["rssd"]
    rmsd = data["RMSD"]
    mcq = data["MCQ"]
    tm_score = data["TM-score"]

    # Plot RSSD vs RMSD
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_rmsd.png")
    plt.figure()
    plt.scatter(cg_rmsd, rmsd, alpha=0.7)
    plt.title("CG-RMSD vs RMSD")
    plt.xlabel("CG-RMSD")
    plt.ylabel("RMSD")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")

    # Plot RSSD vs MCQ
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_mcq.png")
    plt.figure()
    plt.scatter(cg_rmsd, mcq, alpha=0.7)
    plt.title("CG-RMSD vs MCQ")
    plt.xlabel("CG-RMSD")
    plt.ylabel("MCQ")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")

    # Plot RSSD vs TM-Score
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_tm_score.png")
    plt.figure()
    plt.scatter(cg_rmsd, tm_score, alpha=0.7)
    plt.title("CG-RMSD vs TM-score")
    plt.xlabel("CG-RMSD")
    plt.ylabel("TM-score")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")


if __name__ == "__main__":
    # Base directories
    merged_folder = "project/MERGING"  # Folder containing merged CSV files
    corr_results_base_folder = "project/CORR_results"  # Base folder for correlation results
    plots_base_folder = "project/corr IMG"  # Base folder for plots

    # Ensure the base directories exist
    ensure_dir_exists(corr_results_base_folder)
    ensure_dir_exists(plots_base_folder)

    # Process each merged file in the MERGING folder
    for merged_file in os.listdir(merged_folder):
        if merged_file.endswith(".csv"):
            structure_id = os.path.splitext(merged_file)[0].replace("merged_", "")
            merged_file_path = os.path.join(merged_folder, merged_file)

            # Define output paths
            corr_results_file = os.path.join(corr_results_base_folder, f"corr_{structure_id}.txt")
            plots_folder = os.path.join(plots_base_folder, f"CORR_IMG_{structure_id}")

            # Ensure directories exist
            ensure_dir_exists(corr_results_file)
            ensure_dir_exists(os.path.join(plots_folder, "dummy_file"))

            # Compute correlations
            correlations = compute_correlations(merged_file_path)

            # Save correlations to a text file
            with open(corr_results_file, "w") as f:
                for metric, corr in correlations.items():
                    f.write(f"{metric}:\n")
                    f.write(f"  Pearson Correlation: r = {corr['pearson'][0]:.3f}, p = {corr['pearson'][1]:.3e}\n")
                    f.write(f"  Spearman Correlation: r = {corr['spearman'][0]:.3f}, p = {corr['spearman'][1]:.3e}\n\n")

            print(f"Correlation results saved to {corr_results_file}")

            # Plot and save correlations
            plot_correlations(merged_file_path, plots_folder)
