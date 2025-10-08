import pandas as pd

# Load CSV
df = pd.read_csv("modis_Australia_processed.csv")

# Keep only relevant columns
df = df[["latitude", "longitude", "brightness", "frp", "acq_date", "year_month"]]

# Drop rows with missing FRP
df = df.dropna(subset=["frp"])

# Filter out bottom 20% of FRP
threshold = df["frp"].quantile(0.2)
df = df[df["frp"] > threshold]

# Save processed file
df.to_csv("modis_Australia_filtered.csv", index=False)

print("✅ Reduced file saved as modis_Australia_filtered.csv")
