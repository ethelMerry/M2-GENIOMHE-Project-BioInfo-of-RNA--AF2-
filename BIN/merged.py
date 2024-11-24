import os
import pandas as pd

def clean_column_names(df):
    """
    Strip and clean column names of a DataFrame.
    """
    df.columns = df.columns.str.strip() 
    return df

def merge_files_in_directories(dir1, dir2, output_dir):
    """
    Automatically merge files with matching names from two directories based on the 'Model' column.
    
    :param dir_SCORES: Path to the directory where the scores files are located 
    :param dir_RSSD: Path to the directory were the RSSD scores files are located
    :param output_dir: Path to "MERGED" folder where the merged files will be saved
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dir1_files = {f for f in os.listdir(dir1) if f.endswith(".csv")}
    dir2_files = {f for f in os.listdir(dir2) if f.endswith(".csv")}
    matching_files = dir1_files.intersection(dir2_files)

    if not matching_files:
        print("No matching files found between the two directories.")

        return

    for file_name in matching_files:
        try:
            # Load and clean first file 
            file1_path = os.path.join(dir1, file_name)
            file1_df = pd.read_csv(file1_path, sep=",")
            file1_df = clean_column_names(file1_df)  # Clean column names

            # Load and clean second file
            file2_path = os.path.join(dir2, file_name)
            file2_df = pd.read_csv(file2_path, sep=",")
            file2_df = clean_column_names(file2_df)  # Clean column names

            # Check for 'Model' column
            if "Model" not in file1_df.columns or "Model" not in file2_df.columns:
                print(f"Error: Column 'Model' is missing in one of the files : {file_name}")
                continue

            # Keep only the 'Model' and 'rssd' column from the second file
            if "RSSD" in file2_df.columns:  # Ensure 'rssd' exists
                file2_df = file2_df[["Model", "RSSD"]]
            else:
                print(f"Error: Missing column 'RSSD' in file {file_name}")
                continue

            # Merge and save the result
            merged_df = pd.merge(file1_df, file2_df, on="Model", how="left")
            output_file_path = os.path.join(output_dir, file_name)
            merged_df.to_csv(output_file_path, sep=",", index=False)
            print(f"Merged files saved to : {output_file_path}")

        except Exception as e:
            print(f"Error processing file{file_name} : {e}")


if __name__ == "__main__":
    # Define directories
    dir_SCORES = input("Please enter the path of your SCORES folder:")  
    dir_RSSD = input("please enter the path of your RSSD folder:") 
    output_dir = input("Please enter the path of your 'MERGED' output folder:") 

    # Run the merge function
    merge_files_in_directories(dir_SCORES, dir_RSSD, output_dir)