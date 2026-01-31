import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv("data_table.csv")
except FileNotFoundError:
    print("Error: The file 'data_table.csv' was not found.")
    print("Please ensure that the .csv file is in the same folder as the script.")
    exit()


def normalize_sensor(text):
    text = str(text).lower()
    if "fmcw" in text:
        return "RADAR FMCW"
    elif "mmwave" in text:
        return "RADAR mmWave"
    elif "doppler" in text:
        return "RADAR Doppler"
    elif "simulated" in text:
        return "Simulated"
    elif "lidar" in text:
        return "LiDAR"
    elif "conventional" in text:
        return "RADAR Conventional"
    else:
        return "Other"


df["Sensor_Normalized"] = df["Radar Type"].apply(normalize_sensor)

matrix = pd.crosstab(df["Sensor_Normalized"], df["Category"])

plt.figure(figsize=(12, 8))
sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", linewidths=0.5)
plt.title("Sensor Type vs. Contribution Category Co-occurrence", fontsize=16)
plt.xlabel("Contribution Category", fontsize=12)
plt.ylabel("Sensor Type", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()

# plt.savefig("ai_radar_distribution.png", dpi=300)
# print("Sensor Matrix vs. Category saved as 'ai_radar_distribution.png'")

plt.show()
