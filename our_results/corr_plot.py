import os
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Parse correlation files and extract data
correlation_folder = "Corr Results"
correlation_data = []

for filename in os.listdir(correlation_folder):
    if filename.startswith("corr_") and filename.endswith(".txt"):
        filepath = os.path.join(correlation_folder, filename)
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
output_file = "cgRMSD_correlations_summary.xlsx"
corr_df.to_excel(output_file)
print(f"Correlation summary saved to {output_file}")

# Step 2: Heatmap of Correlation Data
plt.figure(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, cmap="coolwarm", center=0, linewidths=0.5, fmt=".2f", 
            cbar_kws={"label": "Correlation Coefficient"})
plt.title("Correlation Heatmap (Pearson and Spearman)", fontsize=16)
plt.tight_layout()
heatmap_output_file = "C5'_correlation_heatmap.png"
plt.savefig(heatmap_output_file)
plt.show()
print(f"Heatmap saved to {heatmap_output_file}")

# Step 3: Line Plot of Correlation Scores
df_melted = corr_df.reset_index().melt(id_vars=["Protein"], var_name="Score_Type", value_name="Score")
df_melted["Method"] = df_melted["Score_Type"].apply(lambda x: "Pearson" if "Pearson" in x else "Spearman")
df_melted["Score_Name"] = df_melted["Score_Type"].apply(lambda x: x.split()[1])

plt.figure(figsize=(12, 8))
sns.lineplot(data=df_melted, x="Protein", y="Score", hue="Score_Name", style="Method", markers=True,
             dashes={"Pearson": "", "Spearman": (2, 2)}, palette="Set1")
plt.title("C5' Correlation Scores (RMSD, TM-score, MCQ) by Method", fontsize=16)
plt.xlabel("RNA Structure", fontsize=12)
plt.ylabel("Correlation Score", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Score Type", loc="best")
plt.tight_layout()
lineplot_output_file = "C5'_correlation_scores.png"
plt.savefig(lineplot_output_file)
plt.show()
print(f"Line plot saved to {lineplot_output_file}")

