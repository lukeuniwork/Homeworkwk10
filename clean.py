import pandas as pd

# Load CSV
df = pd.read_csv("modis_Australia.csv")

# Ensure acq_date is parsed as a datetime
df["acq_date"] = pd.to_datetime(df["acq_date"], format="%Y-%m-%d", errors="coerce")

# Create year_month column (YYYY-MM)
df["year_month"] = df["acq_date"].dt.strftime("%Y-%m")

# Save processed file
df.to_csv("modis_Australia_processed.csv", index=False)

print("✅ Preprocessing complete: modis_Australia_processed.csv written.")
