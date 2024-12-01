import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt


# Ensure directory exists
def ensure_dir_exists(directory):
    """
    Ensure the directory exists, create it if not.
    :param directory: Path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def merge_metrics_and_cgRMSD(cgRMSD_file, metrics_file, output_file):
    """
    Merge the CG-RMSD CSV file with the metrics CSV file by aligning on the 'Model' column.

    :param cgRMSD_file: Path to the CG-RMSD CSV file.
    :param metrics_file: Path to the metrics CSV file.
    :param output_file: Path to save the merged CSV file.
    """
    # Ensure the output directory exists
    ensure_dir_exists(os.path.dirname(output_file))

    # Load CG-RMSD data
    cgRMSD_df = pd.read_csv(cgRMSD_file)

    # Load metrics data and rename the first column to 'Model' if it doesn't have a header
    metrics_df = pd.read_csv(metrics_file, header=None)
    metrics_df.columns = ["Model", "RMSD", "MCQ", "TM-score"]  # Set column names

    # Extract the portion after 'normalized_' in the 'Model' column of the metrics file
    metrics_df["Model"] = metrics_df["Model"].str.split("normalized_").str[-1]

    # Merge the two dataframes on the 'Model' column
    merged_df = pd.merge(cgRMSD_df, metrics_df, on="Model", how="inner")

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to {output_file}")


# Compute Correlations
def compute_correlations(data_file):
    """
    Compute Pearson and Spearman correlations between CG-RMSD and other metrics (RMSD, MCQ, TM-score).

    :param data_file: Path to the CSV file containing CG-RMSD and metrics.
    :return: Dictionary of correlation results for each metric.
    """
    # Load the merged CSV file
    data = pd.read_csv(data_file)

    # Extract relevant columns
    cgRMSD = data["CG-RMSD"]
    rmsd = data["RMSD"]
    mcq = data["MCQ"]
    tm_score = data["TM-score"]

    # Filter out rows with NaN or inf values to avoid errors during correlation computation
    valid_data = data[np.isfinite(cgRMSD) & np.isfinite(rmsd) & np.isfinite(mcq) & np.isfinite(tm_score)]

    if valid_data.empty:
        raise ValueError("Data contains only NaN or inf values after filtering. Cannot compute correlations.")

    # Extract cleaned columns
    cgRMSD = valid_data["CG-RMSD"]
    rmsd = valid_data["RMSD"]
    mcq = valid_data["MCQ"]
    tm_score = valid_data["TM-score"]

    # Compute Pearson and Spearman correlations for each metric
    correlations = {
        "RMSD": {
            "pearson": pearsonr(cgRMSD, rmsd),
            "spearman": spearmanr(cgRMSD, rmsd),
        },
        "MCQ": {
            "pearson": pearsonr(cgRMSD, mcq),
            "spearman": spearmanr(cgRMSD, mcq),
        },
        "TM-score": {
            "pearson": pearsonr(cgRMSD, tm_score),
            "spearman": spearmanr(cgRMSD, tm_score),
        },
    }

    return correlations


# Plot Correlations
def plot_correlations(data_file, output_folder):
    """
    Plot scatter plots of CG-RMSD vs other metrics and save them to the specified folder.

    :param data_file: Path to the CSV file containing CG-RMSD and metrics.
    :param output_folder: Folder to save the scatter plot images.
    """
    # Ensure the output folder exists
    ensure_dir_exists(output_folder)

    # Load the merged CSV file
    data = pd.read_csv(data_file)

    # Extract relevant columns
    cgRMSD = data["CG-RMSD"]
    rmsd = data["RMSD"]
    mcq = data["MCQ"]
    tm_score = data["TM-score"]

    # Plot CG-RMSD vs RMSD
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_rmsd.png")
    plt.figure()
    plt.scatter(cgRMSD, rmsd, alpha=0.7)
    plt.title("CG-RMSD vs RMSD")
    plt.xlabel("CG-RMSD")
    plt.ylabel("RMSD")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")

    # Plot CG-RMSD vs MCQ
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_mcq.png")
    plt.figure()
    plt.scatter(cgRMSD, mcq, alpha=0.7)
    plt.title("CG-RMSD vs MCQ")
    plt.xlabel("CG-RMSD")
    plt.ylabel("MCQ")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")

    # Plot CG-RMSD vs TM-Score
    plot_path = os.path.join(output_folder, "cg_rmsd_vs_tm_score.png")
    plt.figure()
    plt.scatter(cgRMSD, tm_score, alpha=0.7)
    plt.title("CG-RMSD vs TM-score")
    plt.xlabel("CG-RMSD")
    plt.ylabel("TM-score")
    plt.grid()
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved: {plot_path}")
