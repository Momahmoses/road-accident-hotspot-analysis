"""Generate synthetic road accident data for Nigerian corridors."""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import SAMPLE_DIR, STUDY_CORRIDORS, FEATURE_COLS, TARGET_COL


def generate_accident_data(n_accidents: int = 4000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    corridors = list(STUDY_CORRIDORS.keys())
    corridor_labels = rng.choice(corridors, size=n_accidents)

    lats, lons = [], []
    for c in corridor_labels:
        info = STUDY_CORRIDORS[c]
        t = rng.uniform(0, 1)
        lat = info["lat_start"] + t * (info["lat_end"] - info["lat_start"])
        lon = info["lon_start"] + t * (info["lon_end"] - info["lon_start"])
        lat += rng.normal(0, 0.02)
        lon += rng.normal(0, 0.02)
        lats.append(lat)
        lons.append(lon)

    road_curvature = rng.uniform(0, 1, n_accidents)
    speed_limit = rng.choice([60, 80, 100, 120], size=n_accidents, p=[0.2, 0.3, 0.35, 0.15])
    road_width = rng.uniform(3.5, 14, n_accidents)
    surface_condition = rng.choice([0, 1, 2], size=n_accidents, p=[0.6, 0.25, 0.15])  # 0=good,1=fair,2=poor
    junctions = rng.poisson(2, n_accidents)
    visibility = rng.uniform(20, 500, n_accidents)
    rainfall = rng.exponential(20, n_accidents).clip(0, 150)
    hour = rng.integers(0, 24, n_accidents)
    is_night = ((hour < 6) | (hour > 20)).astype(int)
    is_weekend = rng.choice([0, 1], size=n_accidents, p=[0.71, 0.29])
    vehicle_count = rng.poisson(40, n_accidents)
    pedestrian_density = rng.exponential(5, n_accidents).clip(0, 50)

    # Severity scoring
    risk = (
        road_curvature * 0.20 +
        (speed_limit / 120) * 0.25 +
        (2 - road_width / 14) * 0.10 +
        (surface_condition / 2) * 0.15 +
        (1 - visibility / 500) * 0.10 +
        (rainfall / 150) * 0.08 +
        is_night * 0.12
    )
    severity = np.where(risk < 0.35, 0, np.where(risk < 0.60, 1, 2))
    severity = np.clip(severity + rng.integers(-1, 2, n_accidents), 0, 2)

    # Random dates 2020-2025
    years = rng.integers(2020, 2026, n_accidents)
    months = rng.integers(1, 13, n_accidents)
    days = rng.integers(1, 29, n_accidents)
    dates = [f"{y}-{m:02d}-{d:02d}" for y, m, d in zip(years, months, days)]

    df = pd.DataFrame({
        "date": dates, "latitude": lats, "longitude": lons, "corridor": corridor_labels,
        "road_curvature": road_curvature, "speed_limit_kmh": speed_limit,
        "road_width_m": road_width, "surface_condition": surface_condition,
        "n_junctions_nearby": junctions, "visibility_m": visibility,
        "rainfall_mm": rainfall, "hour_of_day": hour, "is_night": is_night,
        "is_weekend": is_weekend, "vehicle_count": vehicle_count,
        "pedestrian_density": pedestrian_density,
        TARGET_COL: severity,
    })
    return df


def load_or_generate():
    path = os.path.join(SAMPLE_DIR, "accident_data.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = generate_accident_data()
        os.makedirs(SAMPLE_DIR, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Generated {len(df):,} accident records")
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
