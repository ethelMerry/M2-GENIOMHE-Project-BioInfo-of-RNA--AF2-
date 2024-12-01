import os
import csv
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt


def ensure_dir_exists(file_path):
    """
    Ensure the directory for a given file path exists. Create it if it doesn't.
    :param file_path: The file path or directory path.
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def parse_pdb(pdb_file, atom_names=None, all_atoms=False):
    """
    Parse a PDB file to extract atomic coordinates for specific atom types or all atoms.
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

def compute_cgRMSD(true_atoms, predicted_atoms):
    """
    Compute the coarse-grained RMSD (CG-RMSD) between native and predicted atoms.

    :param true_atoms: Numpy array of native structure atom coordinates.
    :param predicted_atoms: Numpy array of predicted structure atom coordinates.
    :return: Rotation object, normalized CG-RMSD value.
    """
    if true_atoms.shape != predicted_atoms.shape:
        raise ValueError(f"Shape mismatch: {true_atoms.shape} vs {predicted_atoms.shape}")
    
    # Align vectors and calculate raw CG-RMSD
    rotation, raw_cgRMSD = R.align_vectors(true_atoms, predicted_atoms, return_sensitivity=False)
    
   # Normalize CG-RMSD by dividing by the number of atoms
    normalized_cgRMSD = raw_cgRMSD / len(true_atoms)
    
    return rotation, normalized_cgRMSD  # Return both values

def process_pdb_folder(native_pdb, predicted_folder, output_file, plots_folder, atom_names, all_atoms=False):
    """
    Process a folder of predicted PDB files, compute normalized CG-RMSD for each file, and save results and plots.

    :param native_pdb: Path to the native PDB file.
    :param predicted_folder: Path to the folder containing predicted PDB files.
    :param output_file: Path to the CSV file to save results.
    :param plots_folder: Path to the folder to save plot images.
    :param atom_names: List of atom names to consider for computation.
    :param all_atoms: Boolean, if True, include all atoms in computation.
    """
    ensure_dir_exists(os.path.dirname(output_file))
    ensure_dir_exists(plots_folder)  # Ensure base plots directory exists

    # Parse the native PDB file
    true_atoms = parse_pdb(native_pdb, atom_names, all_atoms)
    if true_atoms.size == 0:
        print(f"No atoms found in {native_pdb}. Skipping.")
        return

    # Process each predicted file
    predicted_files = [f for f in os.listdir(predicted_folder) if f.endswith(".pdb")]
    results = []

    for pdb_file in predicted_files:
        predicted_path = os.path.join(predicted_folder, pdb_file)
        try:
            predicted_atoms = parse_pdb(predicted_path, atom_names, all_atoms)
            if true_atoms.shape != predicted_atoms.shape:
                print(f"Skipping {pdb_file}: Shape mismatch.")
                continue

            # Compute normalized CG-RMSD and generate plot
            rotation, normalized_cgRMSD = compute_cgRMSD(true_atoms, predicted_atoms)

            # Ensure subdirectory exists for saving the plot
            structure_subfolder = os.path.dirname(os.path.join(plots_folder, pdb_file))
            ensure_dir_exists(structure_subfolder)

            plot_file = os.path.join(plots_folder, f"{os.path.splitext(pdb_file)[0]}.png")
            plot_points(true_atoms, predicted_atoms, rotation, plot_file)

            # Append model and calculated CG-RMSD to results
            results.append({"Model": pdb_file, "CG-RMSD": normalized_cgRMSD})

        except Exception as e:
            print(f"Error processing {pdb_file}: {e}")
            results.append({"Model": pdb_file, "CG-RMSD": "Error"})

    # Save results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Model", "CG-RMSD"])
        writer.writeheader()
        writer.writerows(results)

def plot_points(true_atoms, p_atoms, rotation, plot_file):
    """
    Plot the native, predicted, rotated, and translated atomic coordinates, and save to a file.
    """
    rot_atoms = rotation.apply(p_atoms)
    translation = true_atoms.mean(axis=0) - rot_atoms.mean(axis=0)
    trans_atoms = rot_atoms + translation

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(true_atoms[:, 0], true_atoms[:, 1], true_atoms[:, 2], label="Native atoms")
    ax.scatter(p_atoms[:, 0], p_atoms[:, 1], p_atoms[:, 2], label="Predicted atoms")
    ax.scatter(rot_atoms[:, 0], rot_atoms[:, 1], rot_atoms[:, 2], label="Rotated atoms")
    ax.scatter(
        trans_atoms[:, 0], trans_atoms[:, 1], trans_atoms[:, 2], label="Translated atoms"
    )
    plt.legend()
    plt.savefig(plot_file)  # Save the plot
    plt.close()  # Close the plot to avoid memory leaks
    print(f"Plot saved: {plot_file}")  # Log plot save
