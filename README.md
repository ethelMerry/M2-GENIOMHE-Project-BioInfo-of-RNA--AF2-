This is a group project for the course- Bioinformatics of RNA and non-coding world.

Member of the team : 
[Stephaniefouteau](https://github.com/stephaniefouteau) - 
[13Aigrie](https://github.com/13Aigrie) - 
[Ethelmerry](https://github.com/skyethel)

The goal of the project is to compute a custom coarse-grained RMSD and to compare its correlation with three main metrics: RMSD, MCQ and TM-Score.
The question to answer is : **Which coarse-grained representation has the highest correlation to current metrics?**

This repository contains Python scripts and resources for calculating coarse-grained root mean square deviation (CG-RMSD or RSSD) and analyzing its correlation with structural metrics (RMSD, MCQ, TM-score). The project emphasizes clean code, structured workflows, and a detailed analysis pipeline.

---

## Table of Contents

- [Overview](#overview)
- [Quality of Code](#quality-of-code)
  - [Documentation](#documentation)
  - [Structure](#structure)
- [Repository Overview](#repository-overview)
  - [Scripts](#scripts)
- [Functionality: Custom RMSD Computation](#functionality-custom-rmsd-computation)
- [Setup](#setup)

---

## Overview

This project automates the process of evaluating predicted molecular structures against native structures. The key functionalities include:
1. **Cleaning datas*** : cleaning primary datas by standardizes CSV files : renaming the first column to “Model” and removing the “normalized_” prefix from its entries
2. **Computing CG-RMSD  for predicted and native structures**: Measure the structural deviation of predicted structures from the native structure.
3. **Merging Results with Metrics (RMSD, MCQ, TM-score)**: Combine CG-RMSD values with additional metrics (RMSD, MCQ, TM-score).
4. **Correlation Analysis**: Determine the relationships between CG-RMSD and the metrics using Pearson and Spearman correlations and generating scatter plots for visualization..

---

## Quality of Code

### documentation
### 1. **Code Readability**
- **Readable Variable and Function Names**: 
  All variable and function names are descriptive and follow Python's naming conventions (PEP 8).
- **Consistent Formatting**: 
  The code uses consistent indentation and avoids overly long lines, ensuring readability.
- **Commenting and Documentation**: 
  - Each function is documented with **docstrings** explaining its purpose, input parameters, and output.
  - Inline comments are used to clarify complex logic.

### 2. **Modular Structure**
- **Separation of Concerns**: Each script is designed for a specific task:
  - `clean.py`: Clean scores files
  - `compute_rssd.py`: Handles CG-RMSD computation.
  - `merge.py`: Merges CG-RMSD results with external metrics.
  - `compute_corr.py`: Computes correlations and visualizes results.
- **Reusable Functions**: Functions like `ensure_dir_exists` and `parse_pdb` are modular and shared across scripts.

### 3. **Error Handling**
- **Descriptive Errors**: The scripts provide meaningful error messages for common issues like:
  - Shape mismatches between native and predicted structures.
  - Missing or invalid data (`NaN`/`inf` values).
- **Graceful Skipping**: Files with errors are skipped, and the processing continues for the remaining files.

### 4. **Performance Optimizations**
- **Batch Processing**: The scripts are designed to process all files in a folder, reducing manual effort.
- **Efficient Computations**: Uses `numpy` for vectorized numerical operations to ensure speed and efficiency.

### 5. **Testing and Debugging**
- **Debugging Outputs**: Intermediate results (e.g., RSSD values, processed file names) are printed for easier debugging.
- **Validation Checks**: Scripts check for the existence of inputs and directories before processing.


### Structure

The repository is logically structured:
- `compute_rssd.py`: Computes CG-RMSD and visualizes structural alignments.
- `merge.py`: Merges CG-RMSD results with additional metrics.
- `compute_corr.py`: Computes correlations between CG-RMSD and metrics, generating scatter plots.

---

## Repository Overview

### Scripts

#### 1. clean.py 
This script processes and cleans primary data files for downstream analysis. It:
- Renames the first column of `.csv` files to “Model” for consistency.
- Removes the “normalized_” prefix from entries in the “Model” column to simplify identifiers.
- Processes all CSV files in the specified directory, ensuring uniform formatting.
- Saves the cleaned files to a specified output directory.

#### Input:

-Directory containing raw CSV files with structural data (e.g., `scores/`).

#### Output:

-Cleaned `.csv` files and saved them in the same output directory with standardized column names and identifiers.

#### 2. **`compute_rssd.py`**

This script calculates CG-RMSD for native and predicted structures. It:
- Extracts atomic coordinates for a specific atom type (default: `"C5'"`).
- Aligns the predicted structures to the native structure using **scipy's `Rotation.align_vectors`**.
- Computes CG-RMSD values.
- Saves results in a `.csv` file.
- Generates 3D scatter plots visualizing alignment.

##### Input:
- Native PDB file (e.g., `rp05.pdb`).
- Directory of predicted PDB files (e.g., `rp05/`).

##### Output:
- `.csv` file with CG-RMSD values for each predicted structure.
- A folder of plots visualizing the alignment.

---

#### 3. **`merge.py`**

This script merges the CG-RMSD results with a metrics file containing RMSD, MCQ, and TM-score values. It:
- Loads the CG-RMSD and metrics files.
- Joins the datasets on the file names.
- Saves the merged results for further analysis.

##### Input:
- CG-RMSD `.csv` file (e.g., `rssd_rp05.csv`).
- Metrics `.csv` file (e.g., `metrics_rp05.csv`).

##### Output:
- Merged `.csv` file combining CG-RMSD and metrics.

---

#### 4. **`compute_corr.py`**

This script computes Pearson and Spearman correlations between CG-RMSD and metrics. It:
- Computes correlations between CG-RMSD and RMSD, MCQ, TM-score.
- Generates scatter plots visualizing the relationships.
- Saves correlation results in a `.txt` file.

##### Input:
- Merged `.csv` files (e.g., `MERGING/merged_rp05.csv`).

##### Output:
- `.txt` file summarizing correlations (e.g., `CORR_results/corr_rp05.txt`).
- A folder of scatter plots (e.g., `corr IMG/CORR_IMG_rp05`).

---

## Functionality: Custom RMSD Computation

The CG-RMSD computation is fully functional. It:
1. Parses native and predicted PDB files to extract atomic coordinates.
2. Aligns predicted structures to the native structure using a rotation matrix.
3. Handles cases where atomic counts mismatch, providing descriptive errors by skippping mismatched files and loggging the issue.
4. Saves CG-RMSD results and 3D alignment plots.


## Setup

To run the scripts, you may need to install numpy, scipy, matplotlib and biopython

