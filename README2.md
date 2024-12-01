This is a group project for the course- Bioinformatics of RNA and non-coding world.

Member of the team : 
[Stephaniefouteau](https://github.com/stephaniefouteau) - 
[13Aigrie](https://github.com/13Aigrie) - 
[Ethelmerry](https://github.com/skyethel)

The goal of the project is to compute a custom coarse-grained RMSD and to compare its correlation with three main metrics: RMSD, MCQ and TM-Score.

The question we want to answer is : **Which coarse-grained representation has the highest correlation to current metrics?**

This repository contains Python scripts and resources for calculating coarse-grained root mean square deviation (CG-RMSD or RSSD) and analyzing its correlation with structural metrics (RMSD, MCQ, TM-score). The project emphasizes clean code, structured workflows, and a detailed analysis pipeline.

---

## Table of Contents

- [Overview](#overview)
- [Features](#Features)
- [Quality of the code](#quality-of-the-code)
- [Dataset](#Dataset)
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Usage](#Usage)
  - [Step 1: Compute CG-RMSD](##step-1:-compute-cg-rmsd)
  - [Step 2: Merge CG-RMSD and scores](##step-2:-merge-cg-rmsd-and-scores)
  - [Step 3: Compute Correlations and Visualizations](##step-3:-compute-correlations-and-visualizations)
- [Project Structure](#project-structure)
- [Example Outputs](#example-outputs)
- [Contributing](#contributing)
- [Project Structure](#project-structure)


---

## Overview

This project automates the process of evaluating predicted molecular structures against native structures. The key functionalities include:
1. Compute Coarse-Grained RMSD (CG-RMSD) between native and predicted structures.
2. Merging CG-RMSD results with RMSD, MCQ, and TM-score scores.
3. Analyzing with Pearson and Spearman correlations between these metrics and visualizase the relationships through scatter plots.  

---

## Features 

- **Custom CG-RMSD Calculation**: Includes a class-based implementation for modularity.
- **Correlation Analysis**: Computes Spearman and Pearson correlations between CG-RMSD and RMSD, MCQ, TM-Score.
- **Visualization**: Generates scatter plots of CG-RMSD vs. other metrics.
- **Documentation**: Detailed explanations of code structure and usage in this README.

---

## Quality of the code

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
- **Separation of Concerns**: Each script serves a distinct purpose and is well-documented::
  - `compute_cgRMSD.py`: Responsible for parsing PDB files, extracting atomic coordinates, and computing CG-RMSD
  - `merge_and_corr.py`: Handles the merging of CG-RMSD results with external metrics and computes correlations.
  - `main_all.py`: Acts as the main driver script to execute the entire workflow sequentially.
  - `CustomCGRMSD.py: Provides a reusable class-based implementation for custom CG-RMSD computation.
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

---

## Dataset  
The dataset consists of three components:

	-	NATIVE: Native PDB structures from the RNA-Puzzles dataset (Cruz et al., 2012).
	-	PREDS: Predicted PDB structures from various models.
	-	SCORES: Precomputed metrics (RMSD, MCQ, TM-Score) comparing native and predicted structures.

Dataset Link  

https://github.com/clementbernardd/custom_rmsd_m2_geniomhe/tree/main/data

---

## Requirements

### Software 

  - Python 3.7+

### Software Libraries

  - numpy
  - scipy
  - pandas
  - matplotlib

### Created folders  

  - CG-RMSD 
  - CG_RMSD_PLOTS 
  - MERGED
  - CORR_PLOTS 
  - CORR_RES


## Installation 
 - Clone the repository:  
`git clone https://github.com/ethelMerry/M2-GENIOMHE-Project-BioInfo-of-RNA--AF2-.git`  
`cd RNA`

## Usage 
### Step 1: Compute CG-RMSD

This script handles the calculation of CG-RMSD for native and predicted RNA structures.  
It:
	•	Parses native and predicted PDB files to extract atomic coordinates.
	•	Aligns the predicted structures to the native structure using scipy’s Rotation.align_vectors.
	•	Computes normalized CG-RMSD values for selected atoms or all atoms.
	•	Saves results in a .csv file.
	•	Generates 3D scatter plots visualizing the alignment results.

Input:

	•	Native PDB File: A .pdb file containing the native structure (e.g., native_rp05.pdb).
	•	Predicted PDB Folder: A directory containing predicted .pdb files (e.g., predicted_rp05/).

Output:

	•	A .csv file containing CG-RMSD values for each predicted structure (e.g., cg_rmsd_rp05.csv).
	•	A folder of 3D scatter plots visualizing alignments (e.g., plots_rp05/).


### Step 2: Merge CG-RMSD and Metrics

merge_and_corr.py (merge_metrics_and_cgRMSD function)

This script merges CG-RMSD results with precomputed metrics (RMSD, MCQ, and TM-Score). It:
	•	Loads CG-RMSD .csv files and metrics .csv files.
	•	Joins the two datasets on the structure IDs (e.g., filenames).
	•	Saves the merged results as a new .csv file for further analysis.

Input:

	•	CG-RMSD .csv File: Contains CG-RMSD values (e.g., cg_rmsd_rp05.csv).
	•	Metrics .csv File: Contains metrics like RMSD, MCQ, and TM-Score (e.g., metrics_rp05.csv).

Output:

	•	A merged .csv file combining CG-RMSD and metrics (e.g., merged_rp05.csv).


### Step 3: Compute Correlations and Visualizations

compute_corr.py

This script computes Pearson and Spearman correlations between CG-RMSD and other metrics. It:
	•	Computes correlation coefficients for CG-RMSD vs. RMSD, MCQ, and TM-Score.
	•	Generates scatter plots to visualize relationships between CG-RMSD and the metrics.
	•	Saves the correlation results to a .txt file.

Input:

	•	Merged .csv files (e.g., merged_rp05.csv).

Output:

	•	Correlation Results: A .txt file summarizing correlations for each metric (e.g., corr_results/corr_rp05.txt).
	•	Scatter Plots: A folder containing visualizations of CG-RMSD vs. RMSD, MCQ, and TM-Score (e.g., CORR_IMG_rp05/).



### Main Workflow: main_all.py

The main_all.py script orchestrates the entire workflow:  

	Step 1: Prompts the user to calculate CG-RMSD for native and predicted PDB files.  
	Step 2: Merges CG-RMSD results with precomputed metrics.  
	Step 3: Computes correlations and generates visualizations.  

### How to Run:
python main_all.py

Follow the prompt : 

`1.Provide the paths to native and predicted PDB files.  

2.Specify atom types to include (e.g., C5, P, or all). 

3.Merge the CG-RMSD results with precomputed scores.  

4.Generate and save correlation results and visualizations.`

Example Output:

	•	CG-RMSD Results: output/cg_rmsd_rp05.csv
	•	Merged Metrics: output/merged_rp05.csv
	•	Correlation Results: results/corr_rp05.txt
	•	Scatter Plots: plots/CORR_IMG_rp05/


## Project Structure

1. main_all.py: Orchestrates CG-RMSD computation, merging, and correlation analysis for all files.
2. compute_cgRMSD.py: Defines functions for CG-RMSD computation.
3. merge_and_corr.py: Handles file merging and correlation computations.
4. CustomCGRMSD.py: Implements a customizable class for CG-RMSD computation for one native and one predicted pdb file.

## Output Directories:
- **CG-RMSD**: Contains CG-RMSD results.
- **CG_RMSD_PLOTS**: Contains 3D scatter plots visualizing the alignment results.
- **MERGED**: Contains merged results with metrics.
- **CORR_RES**: Contains correlation results.
- **CORR_PLOTS**: Stores scatter plots.  



### License

This project is licensed under the [MIT License](https://opensource.org/license/mit).


