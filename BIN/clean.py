import os
import pandas as pd

def process_files_in_directory(scores_directory , clean_scores_directory):
    """
    Process all CSV files in the input directory by renaming the first column to 'Model'
    and removing the 'normalized_' prefix from the entries in that column.

    :param scores_directory: Path to the scores directory containing CSV files.
    :param clean_scores_directory: Path to the same scores directory where scores files will be cleaned and saved.
    """
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(clean_scores_directory):
        os.makedirs(clean_scores_directory)

    # Parcourir tous les fichiers dans le répertoire d'entrée
    for filename in os.listdir(scores_directory ):
        if filename.endswith(".csv"):
            file_path = os.path.join(scores_directory, filename)
            
            # Charger le fichier CSV
            try:
                df = pd.read_csv(file_path, header=0)
                
                # Renommer la première colonne en 'Model'
                df.rename(columns={df.columns[0]: "Model"}, inplace=True)
                
                # Supprimer 'normalized_' dans la colonne 'Model'
                df["Model"] = df["Model"].str.replace("normalized_", "", regex=False)
                
                # Enregistrer le fichier modifié dans le répertoire de sortie
                output_file_path = os.path.join(clean_scores_directory, filename)
                df.to_csv(output_file_path, index=False)
                print(f"Processed: {filename} -> {output_file_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    # Répertoire contenant les fichiers à traiter
    scores_directory = input("Please enter the path of your scores directory:")
    clean_scores_directory =  input("Please enter the same path as before:") 

    # Traiter les fichiers
    process_files_in_directory(scores_directory, clean_scores_directory)