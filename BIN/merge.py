import os
import pandas as pd


def ensure_dir_exists(file_path):
    """
    Ensure the directory for a given file path exists. Create it if it doesn't.
    :param file_path: The file path for which the directory needs to be ensured.
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def merge_metrics_and_rssd(rssd_file, metrics_file, output_file):
    """
    Merge the RSSD CSV file with the metrics CSV file by considering only the portion
    of the 'file' name in the metrics file after 'normalized_'.
    :param rssd_file: Path to the RSSD CSV file.
    :param metrics_file: Path to the metrics CSV file.
    :param output_file: Path to save the merged CSV file.
    """
    # Ensure the output directory exists
    ensure_dir_exists(output_file)

    # Load RSSD data
    rssd_df = pd.read_csv(rssd_file)

    # Load metrics data and rename the first column if it doesn't have a header
    metrics_df = pd.read_csv(metrics_file, header=None)
    metrics_df.columns = ["file", "RMSD", "MCQ", "TM-score"]  # Set column names

    # Extract the portion after 'normalized_' in the metrics file
    metrics_df["file"] = metrics_df["file"].str.split("normalized_").str[-1]

    # Merge the two dataframes on the 'file' column
    merged_df = pd.merge(rssd_df, metrics_df, on="file", how="inner")

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to {output_file}")


if __name__ == "__main__":
    # Base folders
    rssd_folder = "project/RSSD"  # Folder containing RSSD CSV files
    metrics_folder = "data/SCORES"  # Folder containing metrics CSV files
    output_folder = "project/MERGING"  # Folder to save merged files

    # Ensure the output folder exists
    ensure_dir_exists(output_folder)

    # Iterate over RSSD files
    for rssd_file in os.listdir(rssd_folder):
        if rssd_file.endswith(".csv"):
            # Determine structure ID (e.g., rp09 from rssd_rp09.csv)
            structure_id = os.path.splitext(rssd_file)[0].replace("rssd_", "")

            # Construct corresponding file paths
            rssd_path = os.path.join(rssd_folder, rssd_file)
            metrics_file = f"{structure_id}.csv"  # Assuming metrics files are named like rp09.csv
            metrics_path = os.path.join(metrics_folder, metrics_file)
            output_file = os.path.join(output_folder, f"merged_{structure_id}.csv")

            # Check if the metrics file exists
            if not os.path.exists(metrics_path):
                print(f"Skipping {rssd_file}: Metrics file {metrics_path} not found.")
                continue

            # Merge the RSSD and metrics files
            print(f"Merging: {rssd_path} with {metrics_path}")
            merge_metrics_and_rssd(rssd_path, metrics_path, output_file)
