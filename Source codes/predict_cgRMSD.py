import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr


def analyze_correlation():
    # Ask for the folder path
    folder_path = input("Enter the path to your folder containing the CSV file(s): ").strip()

    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        print("The specified path is not a directory. Please provide a valid folder path.")
        return

    # Look for CSV files in the folder
    files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
    if not files:
        print("No CSV files found in the specified folder.")
        return

    # Load the first CSV file
    file_path = os.path.join(folder_path, files[0])
    print(f"Processing file: {file_path}")
    df = pd.read_csv(file_path)

    # Debugging: Print available columns
    print("Columns in the file:", df.columns.tolist())

    # Remove extra spaces in column names (if any)
    df.columns = df.columns.str.strip()

    # Check for required columns
    required_columns = ["CG-RMSD", "RMSD", "MCQ", "TM-score"]
    if not all(col in df.columns for col in required_columns):
        print(f"The file does not contain all required columns: {required_columns}")
        return

    # Ask for the correlation type
    correlation_type = input("Which correlation would you like to plot? (pearson/spearman/both): ").strip().lower()
    if correlation_type not in ["pearson", "spearman", "both"]:
        print("Invalid choice. Please enter 'pearson', 'spearman', or 'both'.")
        return

    # Ask for the folder name to save plots
    save_folder = input("Enter the name of the folder to save plots: ").strip()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Calculate correlations
    correlation_results = {}
    metrics = ["RMSD", "MCQ", "TM-score"]

    if correlation_type in ["pearson", "both"]:
        correlation_results["Pearson"] = {metric: pearsonr(df["CG-RMSD"], df[metric])[0] for metric in metrics}
    if correlation_type in ["spearman", "both"]:
        correlation_results["Spearman"] = {metric: spearmanr(df["CG-RMSD"], df[metric])[0] for metric in metrics}

    # Plot correlation scatterplots
    for metric in metrics:
        if correlation_type in ["pearson", "both"]:
            plt.figure(figsize=(12, 6))
            sns.lmplot(x="CG-RMSD", y=metric, data=df, height=6, aspect=1.5)
            plt.title(f"Pearson Correlation between CG-RMSD and {metric}")
            plt.xlabel("CG-RMSD")
            plt.ylabel(metric)
            plt.savefig(os.path.join(save_folder, f"pearson_{metric}.png"))
            plt.close()

        if correlation_type in ["spearman", "both"]:
            sns.scatterplot(x="CG-RMSD", y=metric, data=df)
            plt.title(f"Spearman Correlation between CG-RMSD and {metric}")
            plt.xlabel("CG-RMSD")
            plt.ylabel(metric)
            plt.savefig(os.path.join(save_folder, f"spearman_{metric}.png"))
            plt.close()

        if correlation_type == "both":
            # Side-by-side plots
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            sns.regplot(x="CG-RMSD", y=metric, data=df, ax=axes[0])
            axes[0].set_title(f"Pearson Correlation: {metric}")
            sns.scatterplot(x="CG-RMSD", y=metric, data=df, ax=axes[1])
            axes[1].set_title(f"Spearman Correlation: {metric}")
            plt.tight_layout()
            plt.savefig(os.path.join(save_folder, f"side_by_side_{metric}.png"))
            plt.close()

    # Create a heatmap for correlations
    if correlation_type in ["pearson", "both"]:
        pearson_heatmap = pd.DataFrame(correlation_results["Pearson"], index=["Pearson"]).T
        sns.heatmap(pearson_heatmap, annot=True, cmap="coolwarm", cbar=True)
        plt.title("Pearson Correlation Heatmap")
        plt.savefig(os.path.join(save_folder, "pearson_heatmap.png"))
        plt.close()

    if correlation_type in ["spearman", "both"]:
        spearman_heatmap = pd.DataFrame(correlation_results["Spearman"], index=["Spearman"]).T
        sns.heatmap(spearman_heatmap, annot=True, cmap="coolwarm", cbar=True)
        plt.title("Spearman Correlation Heatmap")
        plt.savefig(os.path.join(save_folder, "spearman_heatmap.png"))
        plt.close()

    print(f"Plots have been saved in the folder: {save_folder}")


# Run the function
if __name__ == "__main__":
    analyze_correlation()