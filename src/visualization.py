"""Folium hotspot maps and temporal analysis charts."""

import folium
from folium.plugins import HeatMap, MarkerCluster
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import OUTPUTS_DIR

SEVERITY_COLORS = {0: "#f39c12", 1: "#e67e22", 2: "#c0392b"}
SEVERITY_LABELS = {0: "Minor", 1: "Serious", 2: "Fatal"}


def create_hotspot_map(gdf: gpd.GeoDataFrame):
    center = [gdf["latitude"].mean(), gdf["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=7, tiles="CartoDB positron")

    heat_data = [[row["latitude"], row["longitude"], row["kde_density"]]
                 for _, row in gdf.iterrows()]
    HeatMap(heat_data, radius=20, blur=25, name="Accident Density Heatmap").add_to(m)

    hotspot_cluster = MarkerCluster(name="Hotspot Accidents").add_to(m)
    for _, row in gdf[gdf["is_hotspot"] == 1].iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5 + row["severity"],
            color=SEVERITY_COLORS[row["severity"]],
            fill=True, fill_opacity=0.75,
            popup=folium.Popup(
                f"Corridor: {row['corridor']}<br>Severity: {SEVERITY_LABELS[row['severity']]}<br>"
                f"Date: {row['date']}<br>Speed limit: {row['speed_limit_kmh']} km/h<br>"
                f"Surface: {'Good' if row['surface_condition']==0 else 'Fair' if row['surface_condition']==1 else 'Poor'}",
                max_width=220,
            ),
        ).add_to(hotspot_cluster)

    legend_html = """<div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
    padding:12px;border-radius:8px;box-shadow:2px 2px 6px rgba(0,0,0,0.3);font-size:12px;">
    <b>Accident Severity</b><br>
    <span style="color:#f39c12;">&#9632;</span> Minor<br>
    <span style="color:#e67e22;">&#9632;</span> Serious<br>
    <span style="color:#c0392b;">&#9632;</span> Fatal</div>"""
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl().add_to(m)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, "accident_hotspot_map.html")
    m.save(out)
    print(f"Hotspot map saved → {out}")


def temporal_analysis(gdf: gpd.GeoDataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    hour_counts = gdf.groupby("hour_of_day").size()
    axes[0, 0].bar(hour_counts.index, hour_counts.values, color="steelblue", edgecolor="white")
    axes[0, 0].set_xlabel("Hour of Day")
    axes[0, 0].set_ylabel("Accidents")
    axes[0, 0].set_title("Accidents by Hour")

    sev_counts = gdf["severity"].value_counts().sort_index()
    axes[0, 1].bar([SEVERITY_LABELS[i] for i in sev_counts.index],
                   sev_counts.values, color=["#f39c12", "#e67e22", "#c0392b"])
    axes[0, 1].set_title("Severity Distribution")
    axes[0, 1].set_ylabel("Count")

    night_day = gdf.groupby(["is_night", "severity"]).size().unstack(fill_value=0)
    night_day.index = ["Day", "Night"]
    night_day.rename(columns=SEVERITY_LABELS, inplace=True)
    night_day.plot(kind="bar", ax=axes[1, 0], color=["#f39c12", "#e67e22", "#c0392b"])
    axes[1, 0].set_title("Day vs Night Accidents by Severity")
    axes[1, 0].tick_params(axis="x", rotation=0)

    axes[1, 1].scatter(gdf["speed_limit_kmh"], gdf["severity"],
                       alpha=0.3, color="coral", s=20)
    axes[1, 1].set_xlabel("Speed Limit (km/h)")
    axes[1, 1].set_ylabel("Severity")
    axes[1, 1].set_title("Speed Limit vs Severity")

    plt.suptitle("Road Accident Analysis — Nigerian Corridors", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUTS_DIR, "temporal_analysis.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("Temporal analysis chart saved.")
