import os
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Prompt user for input and output directories
input_dir = input("Please enter the path to the input directory containing correlation files: ")
output_dir = input("Please enter the path to the output directory to save the correlation data: ")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Step 1: Parse correlation files and extract data
correlation_data = []

for filename in os.listdir(input_dir):
    if filename.startswith("corr_") and filename.endswith(".txt"):
        filepath = os.path.join(input_dir, filename)
        protein_id = filename.replace("corr_", "").replace(".txt", "")
        corr_dict = {"Protein": protein_id}
        
        with open(filepath, 'r') as file:
            content = file.read()
            pearson_matches = re.findall(r'Pearson Correlation: r = ([\d\.\-]+)', content)
            spearman_matches = re.findall(r'Spearman Correlation: r = ([\d\.\-]+)', content)
            if len(pearson_matches) == 3 and len(spearman_matches) == 3:
                corr_dict.update({
                    "Pearson RMSD": float(pearson_matches[0]),
                    "Pearson MCQ": float(pearson_matches[1]),
                    "Pearson TM-score": float(pearson_matches[2]),
                    "Spearman RMSD": float(spearman_matches[0]),
                    "Spearman MCQ": float(spearman_matches[1]),
                    "Spearman TM-score": float(spearman_matches[2])
                })
            else:
                print(f"Warning: Incomplete data in file {filename}")
        
        correlation_data.append(corr_dict)

# Convert to DataFrame
corr_df = pd.DataFrame(correlation_data)
corr_df.set_index("Protein", inplace=True)

# Save to Excel
output_file = os.path.join(output_dir, "cgRMSD_correlations_summary.xlsx")
corr_df.to_excel(output_file)
print(f"Correlation summary saved to {output_file}")

# Step 2: Heatmap of Correlation Data
sns.heatmap(corr_df, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
plt.show()

# Step 3: Line Plot of Correlation Scores
df_melted = corr_df.reset_index().melt(id_vars=["Protein"], var_name="Score_Type", value_name="Score")
sns.lineplot(data=df_melted, x="Protein", y="Score", hue="Score_Type", markers=True)
plt.title("Correlation Scores by Method")
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, "correlation_scores.png"))
plt.show()
