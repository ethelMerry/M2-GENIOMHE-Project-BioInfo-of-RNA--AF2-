import numpy as np
from scipy.spatial.transform import Rotation as R
from compute_cgRMSD import parse_pdb, compute_cgRMSD  # Import functions from the existing script

class CustomCGRMSD:
    def __init__(self, atom_names=None, all_atoms=False):
        """
        Initialize the CustomCGRMSD class with options for atom names.

        :param atom_names: List of atom names to consider for CG-RMSD computation (e.g., ['C5', 'P'])
        :param all_atoms: Boolean, if True, include all atoms in the computation
        """
        self.atom_names = set(atom_names) if atom_names else None
        self.all_atoms = all_atoms

    def predict(self, native_path: str, predicted_path: str) -> float:
        """
        Predict CG-RMSD between a native and a predicted PDB structure.

        :param native_path: Path to a `.pdb` native file.
        :param predicted_path: Path to a `.pdb` predicted file.
        :return: The computed CG-RMSD metric as a float.
        """
        # Use the imported parse_pdb function
        true_atoms = parse_pdb(native_path, atom_names=self.atom_names, all_atoms=self.all_atoms)
        predicted_atoms = parse_pdb(predicted_path, atom_names=self.atom_names, all_atoms=self.all_atoms)

        if true_atoms.size == 0 or predicted_atoms.size == 0:
            raise ValueError("No atoms found in one or both PDB files.")
        
        # Use the imported compute_cgRMSD function
        # The function now returns both rotation and normalized CG-RMSD
        _, cgRMSD_value = compute_cgRMSD(true_atoms, predicted_atoms)  # Unpack and get only the CG-RMSD value
        
        return cgRMSD_value  # Return the CG-RMSD value only

# Main execution for user input
if __name__ == "__main__":
    # Prompt the user to enter atom types to consider
    atom_types_input = input("Enter the atom types to calculate CG-RMSD for (comma-separated, e.g., 'P,C5',O5'): ")
    atom_names = [atom.strip() for atom in atom_types_input.split(",")]

    # Prompt the user to enter the native PDB file path
    native_path = input("Enter the path to the native PDB file: ")

    # Prompt the user to enter the predicted PDB file path
    predicted_path = input("Enter the path to the predicted PDB file: ")

    # Instantiate the CG-RMSD calculator
    cgrmsd_calculator = CustomCGRMSD(atom_names=atom_names)

    # Predict CG-RMSD
    try:
        cg_rmsd = cgrmsd_calculator.predict(native_path, predicted_path)
        print(f"Computed CG-RMSD: {cg_rmsd:.4f}")
    except Exception as e:
        print(f"Error: {e}")
