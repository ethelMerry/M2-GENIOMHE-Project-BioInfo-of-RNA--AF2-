#!/usr/bin/python3

import os
import argparse
# import numpy as np
# from scipy.spatial.transform import Rotation as R
import compute_rmsd
import parse_pdb


"""
def parse_pdb(pdb_file, atom_names=None, all_atoms=False):
    
    Parse a PDB file to extract atomic coordinates for specific atom types or all atoms.

    :param pdb_file: Path to the PDB file to parse.
    :param atom_names: List of atom names to extract coordinates for.
    :param all_atoms: Boolean, if True, extract coordinates for all atoms.
    :return: Numpy array containing the coordinates of the selected atoms.
    
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


def compute_rmsd(true_atoms, predicted_atoms):
    
    Compute the root mean square deviation (RMSD) between native and predicted atoms.

    :param true_atoms: Numpy array of native structure atom coordinates.
    :param predicted_atoms: Numpy array of predicted structure atom coordinates.
    :return: RMSD value.
    
    if true_atoms.shape != predicted_atoms.shape:
        raise ValueError(f"Shape mismatch: {true_atoms.shape} vs {predicted_atoms.shape}")
    rotation, rssd = R.align_vectors(true_atoms, predicted_atoms, return_sensitivity=False)
    rmsd = rssd/len(true_atoms)
    return rotation, rmsd
"""
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute custom RMSD for one RNA and one Prediction')
    parser.add_argument('-native', required=True, help='Path to the native PDB file')
    parser.add_argument('-predicted', required=True, help='Path to the predicted PDB file')
    parser.add_argument('-atoms', type=str, default='all_atoms', help='Comma-separated atom names (e.g., "C5,P")')
    parser.add_argument('-out', type=str, default='cg_rmsd_output', help='Output directory name')
    args = parser.parse_args()

    # Validate arguments
    native_pdb = args.native
    predicted_pdb = args.predicted
    atom_names = args.atoms.split(",") if args.atoms != 'all_atoms' else None
    all_atoms = args.atoms == 'all_atoms'

    if os.path.exists(args.out):
        print(f"Error: Output directory {args.out} already exists. Please choose another name.")
        exit(1)
    else:
        os.mkdir(args.out)

    print(f"Processing custom RMSD for native structure {native_pdb} and predicted structure {predicted_pdb}")

    print("Parsing native PDB file...")
    true_atoms = parse_pdb(native_pdb, atom_names, all_atoms)

    print("Parsing predicted PDB file...")
    predicted_atoms = parse_pdb(predicted_pdb, atom_names, all_atoms)

    print("Computing custom MRSD...")
    rotation, rmsd = compute_rmsd(true_atoms, predicted_atoms)

    # Save the result
    output_file = os.path.join(args.out, "cg_rmsd_result.txt")
    with open(output_file, "w") as f:
        f.write(f"My custom RMSD for the native {native_pdb} and predicted {predicted_pdb} is: {rmsd}\n")

    print(f"Results saved to {output_file}")
