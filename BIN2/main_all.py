import os
from compute_cgRMSD import process_pdb_folder
from merge_and_corr import merge_metrics_and_cgRMSD, compute_correlations, plot_correlations

def main():
    # Ask the user to select the starting step
    print("\nAvailable steps:")
    print("1: Compute CG-RMSD and generate plots")
    print("2: Merge CG-RMSD files and scores")
    print("3: Compute correlations and generate plots")
    start_step = int(input("Choose the step number to start from (1, 2, or 3): "))

    # Step 1: Compute CG-RMSD and save plots
    if start_step <= 1:
        print("\nStep 1: Compute CG-RMSD and generate plots")
        native_folder = input("Enter the path to the folder containing native PDB files: ")
        predicted_base_folder = input("Enter the path to the folder containing predicted PDB files: ")
        output_base_folder = input("Enter the path to save CG-RMSD files (create this folder): ")
        plots_base_folder = input("Enter the path to save CG-RMSD plots (create this folder): ")

        # Atom selection for CG-RMSD computation
        atom_names_input = input("Enter the atom names (comma-separated, e.g., 'C5',P' or 'all' for all atoms): ")
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

                # Compute CG-RMSD and generate the plot
                process_pdb_folder(native_pdb, predicted_folder, output_file, plots_folder, atom_names, all_atoms)

    # Step 2: Merge CG-RMSD and scores
    if start_step <= 2:
        print("\nStep 2: Merge CG-RMSD files and scores")
        cgRMSD_folder = input("Enter the folder containing CG-RMSD files: ")
        metrics_folder = input("Enter the folder containing score files: ")
        merged_folder = input("Enter the folder to save merged files (create this folder): ")

        os.makedirs(merged_folder, exist_ok=True)

        for cgRMSD_file in os.listdir(cgRMSD_folder):
            if cgRMSD_file.endswith(".csv"):
                structure_id = os.path.splitext(cgRMSD_file)[0]
                cgRMSD_path = os.path.join(cgRMSD_folder, cgRMSD_file)
                metrics_path = os.path.join(metrics_folder, f"{structure_id}.csv")
                merged_file = os.path.join(merged_folder, f"merged_{structure_id}.csv")

                if not os.path.exists(metrics_path):
                    print(f"Skipping {cgRMSD_file}: Score file {metrics_path} not found.")
                    continue

                print(f"Merging: {cgRMSD_path} with {metrics_path}")
                merge_metrics_and_cgRMSD(cgRMSD_path, metrics_path, merged_file)

    # Step 3: Compute correlations and save plots
    if start_step <= 3:
        print("\nStep 3: Compute correlations and generate plots")
        plots_base_folder = input("Enter the folder to save correlation plots (create this folder): ")
        corr_results_base_folder = input("Enter the folder to save correlation results (create this folder): ")

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