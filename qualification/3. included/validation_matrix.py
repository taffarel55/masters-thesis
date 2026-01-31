import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def normalize_scenario(text):
    text = str(text).lower()
    if "simulation" in text:
        return "Simulation"
    if "indoor" in text:
        return "Indoor"
    if "outdoor" in text or "urban" in text:
        return "Outdoor"
    return "Other"


def normalize_obstacle(text):
    text = str(text).lower()
    if "human" in text:
        return "Humans"
    if "fixed-wing" in text or "ga" in text:
        return "Fixed-wing Aircraft"
    if "dji" in text or "drone" in text:
        return "Multirotor/Drone"
    if (
        "generic" in text
        or "static" in text
        or "cylindrical" in text
        or "zones" in text
    ):
        return "Generic/Static Obstacles"
    return "Other"


try:
    df = pd.read_csv("data_table.csv")
except FileNotFoundError:
    print("Error: 'data_table.csv' not found.")
    print("Please ensure the .csv file is in the same folder as the script.")
    exit()

df["Scenario_Normalized"] = df["Scenario"].apply(normalize_scenario)
df["Obstacle_Normalized"] = df["Target/Obstacle type"].apply(normalize_obstacle)

matrix = pd.crosstab(df["Scenario_Normalized"], df["Obstacle_Normalized"])

plt.figure(figsize=(12, 7))
sns.heatmap(matrix, annot=True, fmt="d", cmap="Greens", linewidths=0.5)

plt.title("Scenario vs. Obstacle Type Co-occurrence", fontsize=16)
plt.xlabel("Obstacle Type", fontsize=12)
plt.ylabel("Validation Scenario", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()

# plt.savefig("validation_matrix.png", dpi=300)
# print("Validation matrix saved as 'validation_matrix.png'")

plt.show()
