from scipy.spatial.transform import Rotation as R


def compute_rmsd(true_atoms, predicted_atoms):
    """
    Compute the root mean square deviation (RMSD) between native and predicted atoms.

    :param true_atoms: Numpy array of native structure atom coordinates.
    :param predicted_atoms: Numpy array of predicted structure atom coordinates.
    :return: Rotation object and RMSD value.
    """
    if true_atoms.shape != predicted_atoms.shape:
        raise ValueError(f"Shape mismatch: {true_atoms.shape} vs {predicted_atoms.shape}")
    rotation, rssd = R.align_vectors(true_atoms, predicted_atoms, return_sensitivity=False)
    rmsd = rssd/len(true_atoms)
    return rotation, rmsd

