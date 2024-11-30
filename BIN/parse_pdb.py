import csv
import numpy as np

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

