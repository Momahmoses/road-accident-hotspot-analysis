"""KDE-based hotspot detection and spatial clustering."""

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.stats import gaussian_kde
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import OUTPUTS_DIR, KDE_BANDWIDTH, HOTSPOT_PERCENTILE


def compute_kde(gdf: gpd.GeoDataFrame, bandwidth: float = KDE_BANDWIDTH) -> np.ndarray:
    coords = gdf[["longitude", "latitude"]].values.T
    kde = gaussian_kde(coords, bw_method=bandwidth)
    density = kde(coords)
    return density


def identify_hotspots(gdf: gpd.GeoDataFrame, density: np.ndarray) -> gpd.GeoDataFrame:
    threshold = np.percentile(density, HOTSPOT_PERCENTILE)
    gdf = gdf.copy()
    gdf["kde_density"] = density
    gdf["is_hotspot"] = (density >= threshold).astype(int)
    return gdf


def dbscan_clusters(gdf: gpd.GeoDataFrame, eps_deg: float = 0.05, min_samples: int = 5) -> gpd.GeoDataFrame:
    coords = gdf[["latitude", "longitude"]].values
    labels = DBSCAN(eps=eps_deg, min_samples=min_samples).fit_predict(coords)
    gdf = gdf.copy()
    gdf["cluster_id"] = labels
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"  DBSCAN clusters found: {n_clusters}")
    return gdf


def severity_analysis(gdf: gpd.GeoDataFrame):
    severity_map = {0: "minor", 1: "serious", 2: "fatal"}
    gdf = gdf.copy()
    gdf["severity_label"] = gdf["severity"].map(severity_map)

    print("\n  Accident Severity Breakdown:")
    counts = gdf["severity_label"].value_counts()
    for label, count in counts.items():
        print(f"    {label.upper()}: {count:,} ({count/len(gdf):.1%})")

    corridor_severity = gdf.groupby("corridor")["severity"].agg(["mean", "sum", "count"])
    corridor_severity.columns = ["avg_severity", "total_severity_score", "n_accidents"]
    corridor_severity = corridor_severity.sort_values("avg_severity", ascending=False)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    corridor_severity.to_csv(os.path.join(OUTPUTS_DIR, "corridor_severity.csv"))

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(corridor_severity.index, corridor_severity["n_accidents"],
                  color=["#e74c3c" if s > 0.8 else "#f39c12" if s > 0.5 else "#2ecc71"
                         for s in corridor_severity["avg_severity"]])
    ax.set_ylabel("Number of Accidents")
    ax.set_title("Accident Count by Road Corridor — Nigeria")
    ax.tick_params(axis="x", rotation=20)
    for bar, (_, row) in zip(bars, corridor_severity.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"Avg: {row['avg_severity']:.2f}", ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUTS_DIR, "corridor_analysis.png"), dpi=150)
    plt.close()
    print("  Corridor analysis chart saved.")
    return corridor_severity
