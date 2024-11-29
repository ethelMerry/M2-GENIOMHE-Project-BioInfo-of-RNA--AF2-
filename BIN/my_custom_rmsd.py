#!/usr/bin/python3

import os
import argparse
from compute_rmsd import compute_rmsd
import parse_pdb as ppdb


        
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
    true_atoms = ppdb.parse_pdb(native_pdb, atom_names, all_atoms)

    print("Parsing predicted PDB file...")
    predicted_atoms = ppdb.parse_pdb(predicted_pdb, atom_names, all_atoms)

    print("Computing custom MRSD...")
    rotation, rmsd = compute_rmsd(true_atoms, predicted_atoms)

    # Save the result
    output_file = os.path.join(args.out, "cg_rmsd_result.txt")
    with open(output_file, "w") as f:
        f.write(f"My custom RMSD for the native {native_pdb} and predicted {predicted_pdb} is: {rmsd}\n")

    print(f"Results saved to {output_file}")
