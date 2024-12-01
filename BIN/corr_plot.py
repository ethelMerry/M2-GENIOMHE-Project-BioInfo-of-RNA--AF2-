import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file (replace with your actual file path)
file_path = "cgRMSD_correlations_summary.xlsx"
df = pd.read_excel(file_path)

# Melt the DataFrame to have a long format for easier plotting
df_melted = df.melt(id_vars=["Protein"], var_name="Score_Type", value_name="Score")

# Extract Pearson or Spearman from Score_Type for plotting style
df_melted["Method"] = df_melted["Score_Type"].apply(lambda x: "Pearson" if "Pearson" in x else "Spearman")
df_melted["Score_Name"] = df_melted["Score_Type"].apply(lambda x: x.split()[1])  # RMSD, TM-score, MCQ

# Create the plot
plt.figure(figsize=(12, 8))

# Plot each score type with different line styles and colors
sns.lineplot(data=df_melted, x="Protein", y="Score", hue="Score_Name", style="Method", markers=True,
             dashes={"Pearson": "", "Spearman": (2, 2)}, palette="Set1")

plt.title("C5' Correlation Scores (RMSD, TM-score, MCQ) by Method", fontsize=16)
plt.xlabel("RNA Structure", fontsize=12)
plt.ylabel("Correlation Score", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Score Type", loc="best")
plt.tight_layout()

# Show the plot
plt.show()

# Optionally, save the plot
#plt.savefig("C5'_correlation_scores.png")

# Create a correlation matrix for the Pearson and Spearman scores
correlation_matrix = df.drop(columns=["Protein"]).corr()

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Pearson and Spearman Scores", fontsize=16)
plt.tight_layout()
plt.show()
