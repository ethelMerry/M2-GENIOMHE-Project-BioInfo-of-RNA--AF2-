import os
from compute_cgRMSD import process_pdb_folder
from merge_and_corr import merge_metrics_and_cgRMSD, compute_correlations, plot_correlations

def main():
    # Step 1: Compute CG-RMSD and Save Plots
    print("\nStep 1: Compute CG-RMSD and Generate Plots")
    native_folder = input("Enter the path to the native PDB folder: ")
    predicted_base_folder = input("Enter the path to the predicted PDB folder: ")
    output_base_folder = input("Enter the path to the CG-RMSD output folder (create one): ")
    plots_base_folder = input("Enter the path to save CG-RMSD plots (create one): ")

    # Atom selection for CG-RMSD computation
    atom_names_input = input("Enter atom names (comma-separated, e.g., 'C5',P' or 'all' for all atoms): ")
    all_atoms = atom_names_input.lower() == "all"
    atom_names = None if all_atoms else atom_names_input.split(",")

    # Process each native PDB file
    for native_file in os.listdir(native_folder):
        if native_file.endswith(".pdb"):
            native_pdb = os.path.join(native_folder, native_file)
            structure_id = os.path.splitext(native_file)[0]
            predicted_folder = os.path.join(predicted_base_folder, structure_id)
            output_file = os.path.join(output_base_folder, f"{structure_id}.csv")
            plots_folder = os.path.join(plots_base_folder, structure_id)

            if not os.path.exists(predicted_folder):
                print(f"Skipping {native_pdb}: Predicted folder not found.")
                continue

            # Compute CG-RMSD and Save Plot
            process_pdb_folder(native_pdb, predicted_folder, output_file, plots_folder, atom_names, all_atoms)

    # Step 2: Merge CG-RMSD and Metrics
    print("\nStep 2: Merge CG-RMSD and scores files")
    cgRMSD_folder = input("Enter the folder containing CG-RMSD output files: ")
    metrics_folder = input("Enter the folder containing scores files: ")
    merged_folder = input("Enter the folder to save merged files (create one): ")

    os.makedirs(merged_folder, exist_ok=True)

    for cgRMSD_file in os.listdir(cgRMSD_folder):
        if cgRMSD_file.endswith(".csv"):
            structure_id = os.path.splitext(cgRMSD_file)[0]
            cgRMSD_path = os.path.join(cgRMSD_folder, cgRMSD_file)
            metrics_path = os.path.join(metrics_folder, f"{structure_id}.csv")
            merged_file = os.path.join(merged_folder, f"merged_{structure_id}.csv")

            if not os.path.exists(metrics_path):
                print(f"Skipping {cgRMSD_file}: score file {metrics_path} not found.")
                continue

            print(f"Merging: {cgRMSD_path} with {metrics_path}")
            merge_metrics_and_cgRMSD(cgRMSD_path, metrics_path, merged_file)

    # Step 3: Compute Correlations and Generate Plots
    print("\nStep 3: Compute Correlations and Generate Plots")
    plots_base_folder = input("Enter the folder to save correlation plots (create one): ")
    corr_results_base_folder = input("Enter the folder to save correlation results (create one): ")

    os.makedirs(corr_results_base_folder, exist_ok=True)
    os.makedirs(plots_base_folder, exist_ok=True)

    for merged_file in os.listdir(merged_folder):
        if merged_file.endswith(".csv"):
            structure_id = os.path.splitext(merged_file)[0].replace("merged_", "")
            merged_file_path = os.path.join(merged_folder, merged_file)

            corr_results_file = os.path.join(corr_results_base_folder, f"corr_{structure_id}.txt")
            plots_folder = os.path.join(plots_base_folder, f"CORR_IMG_{structure_id}")
            os.makedirs(plots_folder, exist_ok=True)

            # Compute correlations
            print(f"Computing correlations for {merged_file}...")
            correlations = compute_correlations(merged_file_path)

            # Save correlations to a text file
            with open(corr_results_file, "w") as f:
                for metric, corr in correlations.items():
                    f.write(f"{metric}:\n")
                    f.write(f"  Pearson Correlation: r = {corr['pearson'][0]:.3f}, p = {corr['pearson'][1]:.3e}\n")
                    f.write(f"  Spearman Correlation: r = {corr['spearman'][0]:.3f}, p = {corr['spearman'][1]:.3e}\n\n")
            print(f"Correlations saved for {structure_id}.")

            # Generate and save correlation plots
            plot_correlations(merged_file_path, plots_folder)

    print("\nWorkflow completed successfully!")

if __name__ == "__main__":
    main()
