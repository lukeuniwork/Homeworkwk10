import pandas as pd

# Load the CSV
df = pd.read_csv("modis_Australia.csv")

# Convert acq_date to datetime
df["acq_date"] = pd.to_datetime(df["acq_date"])

# Create year-month column
df["month"] = df["acq_date"].dt.month_name()

# Define FRP bins and labels
bins = [0,1000,2000,3000,4000,5000,10000]
labels = bins[1:]

# Assign each row to a bucket
df["frp_bucket"] = pd.cut(df["frp"], bins=bins, labels=labels, right=False)


# Count number of fires per month per bucket
monthly_counts = (
    df.groupby(["month", "frp_bucket"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]
monthly_counts["month"] = pd.Categorical(monthly_counts["month"], categories=month_order, ordered=True)
monthly_counts = monthly_counts.sort_values("month")

# Save to new CSV
monthly_counts.to_csv("stacked-bar.csv", index=False)

print("Saved monthly_frp_counts.csv")
