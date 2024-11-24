import os
import csv
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt


def ensure_dir_exists(directory):
    """
    Ensure the directory exists; create it if it doesn't.
    :param directory: The directory path to check or create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def parse_pdb(pdb_file, atom_names=None, all_atoms=False):
    """
    Parse a PDB file to extract atomic coordinates for specific atom types or all atoms.

    :param pdb_file: Path to the PDB file to parse.
    :param atom_names: List of atom names to extract coordinates for.
    :param all_atoms: Boolean, if True, extract coordinates for all atoms.
    :return: Numpy array containing the coordinates of the selected atoms.
    """
    atoms = []
    with open(pdb_file, 'r') as pdb:
        for line in pdb:
            if line.startswith("ATOM"):
                current_atom = line[12:16].strip()
                if all_atoms or (atom_names and current_atom in atom_names):
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    atoms.append([x, y, z])
    return np.array(atoms)


def compute_rssd(true_atoms, predicted_atoms):
    """
    Compute the root sum square deviation (RSSD) between native and predicted atoms.

    :param true_atoms: Numpy array of native structure atom coordinates.
    :param predicted_atoms: Numpy array of predicted structure atom coordinates.
    :return: Rotation object and RSSD value.
    """
    if true_atoms.shape != predicted_atoms.shape:
        raise ValueError(f"Shape mismatch: {true_atoms.shape} vs {predicted_atoms.shape}")
    rotation, rssd = R.align_vectors(true_atoms, predicted_atoms, return_sensitivity=False)
    return rotation, rssd


def plot_points(true_atoms, predicted_atoms, rotation, plot_file):
    """
    Generate a 3D plot of the native, predicted, rotated, and translated atom positions,
    and save it to a file.

    :param true_atoms: Numpy array of native structure atom coordinates.
    :param predicted_atoms: Numpy array of predicted structure atom coordinates.
    :param rotation: Rotation object used for aligning the atoms.
    :param plot_file: Path to save the plot image.
    """
    rotated_atoms = rotation.apply(predicted_atoms)
    translation = true_atoms.mean(axis=0) - rotated_atoms.mean(axis=0)
    translated_atoms = rotated_atoms + translation

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(true_atoms[:, 0], true_atoms[:, 1], true_atoms[:, 2], label="Native atoms")
    ax.scatter(predicted_atoms[:, 0], predicted_atoms[:, 1], predicted_atoms[:, 2], label="Predicted atoms")
    ax.scatter(rotated_atoms[:, 0], rotated_atoms[:, 1], rotated_atoms[:, 2], label="Rotated atoms")
    ax.scatter(translated_atoms[:, 0], translated_atoms[:, 1], translated_atoms[:, 2], label="Translated atoms")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.legend()
    plt.savefig(plot_file)
    plt.close()


def process_pdb_folder(native_pdb, predicted_folder, output_file, plots_folder, atom_names, all_atoms=False):
    """
    Process a folder of predicted PDB files, compute RSSD for each file, and save results and plots.

    :param native_pdb: Path to the native PDB file.
    :param predicted_folder: Path to the folder containing predicted PDB files.
    :param output_file: Path to the CSV file to save RSSD results.
    :param plots_folder: Path to the folder to save plot images.
    :param atom_names: List of atom names to consider for RSSD computation.
    :param all_atoms: Boolean, if True, include all atoms in RSSD computation.
    """
    # Ensure necessary directories exist
    ensure_dir_exists(os.path.dirname(output_file))
    ensure_dir_exists(plots_folder)

    # Parse the native PDB file
    true_atoms = parse_pdb(native_pdb, atom_names, all_atoms)
    if true_atoms.size == 0:
        print(f"No atoms found in {native_pdb}. Skipping.")
        return

    # List all predicted PDB files
    predicted_files = [f for f in os.listdir(predicted_folder) if f.endswith(".pdb")]
    results = []

    for pdb_file in predicted_files:
        predicted_path = os.path.join(predicted_folder, pdb_file)
        print(f"Processing: {predicted_path}")

        try:
            # Parse the predicted PDB file
            predicted_atoms = parse_pdb(predicted_path, atom_names, all_atoms)

            # Check for shape mismatches
            if true_atoms.shape != predicted_atoms.shape:
                print(f"Skipping {pdb_file}: Shape mismatch {true_atoms.shape} vs {predicted_atoms.shape}")
                continue

            # Compute RSSD and generate a plot
            rotation, rssd = compute_rssd(true_atoms, predicted_atoms)
            print(f"RSSD for {pdb_file}: {rssd:.4f}")

            plot_file = os.path.join(plots_folder, f"{os.path.splitext(pdb_file)[0]}.png")
            plot_points(true_atoms, predicted_atoms, rotation, plot_file)

            # Append results
            results.append({"Model": pdb_file, "RSSD": rssd})

        except Exception as e:
            print(f"Error processing {pdb_file}: {e}")
            results.append({"Model": pdb_file, "RSSD": "Error"})

    # Save results to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Model", "RSSD"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to {output_file}")
    print(f"Plots saved to {plots_folder}")


if __name__ == "__main__":
    # Input directories
    native_folder = input("Enter the path of your native folder: ")
    predicted_base_folder = input("Enter the path of your preds folder: ")
    output_base_folder = input("Enter the path of your output folder: ")
    plots_base_folder = input("Enter the path of your plots folder: ")

    # Select atom representation
    atom_names_input = input("Enter atom names (comma-separated, e.g., C5',P or 'all' for all atoms): ")
    all_atoms = atom_names_input.lower() == "all"
    atom_names = None if all_atoms else atom_names_input.split(",")

    # Process each native PDB file
    for native_file in os.listdir(native_folder):
        if native_file.endswith(".pdb"):
            native_pdb = os.path.join(native_folder, native_file)
            structure_id = os.path.splitext(native_file)[0]  # Extract the structure ID
            predicted_folder = os.path.join(predicted_base_folder, structure_id)
            output_file = os.path.join(output_base_folder, f"{structure_id}.csv")
            plots_folder = os.path.join(plots_base_folder, structure_id)

            # Check if the predicted folder exists
            if not os.path.exists(predicted_folder):
                print(f"Skipping {native_pdb}: Predicted folder {predicted_folder} not found.")
                continue

            print(f"Processing structure: {structure_id}")
            process_pdb_folder(native_pdb, predicted_folder, output_file, plots_folder, atom_names, all_atoms)