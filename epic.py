import pandas as pd
import geopandas as gpd

# --- Load SA3 boundaries (from shapefile or GeoJSON) ---
# If you only have TopoJSON, first convert it (mapshaper.org works, or use geopandas+topojson plugin).
# Let's assume you already have SA3 boundaries as GeoJSON:
sa3 = gpd.read_file("SA3_2021_AUST.json")  # Or .shp if you still have shapefile

# --- Load FIRMS fire detections ---
fires = pd.read_csv("modis_Australia.csv")  # Your cleaned/combined file

# Turn fire detections into GeoDataFrame
fires_gdf = gpd.GeoDataFrame(
    fires,
    geometry=gpd.points_from_xy(fires.longitude, fires.latitude),
    crs="EPSG:4326"   # FIRMS lat/lon is WGS84
)

# Make sure SA3 boundaries are also in WGS84
sa3 = sa3.to_crs("EPSG:4326")

# --- Spatial join: assign each fire to an SA3 polygon ---
fires_with_sa3 = gpd.sjoin(fires_gdf, sa3, how="inner", predicate="within")

# --- Count fires per SA3 ---
fires_by_sa3 = (
    fires_with_sa3.groupby("SA3_CODE21")
    .size()
    .reset_index(name="fire_count")
)

# --- Save to CSV ---
fires_by_sa3.to_csv("fires_by_SA3.csv", index=False)

print("✅ Saved fires_by_SA3.csv with fire counts per SA3")
