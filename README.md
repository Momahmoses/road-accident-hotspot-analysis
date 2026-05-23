# Road Accident Hotspot Analysis & Traffic Safety

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

GIS + spatial statistics system for mapping road accident hotspots on Nigerian highways, supporting FRSC (Federal Road Safety Corps) and state governments in targeting high-risk corridors for intervention.

---

## Problem Statement

Nigeria records over 10,000 road fatalities annually. Without data-driven hotspot maps, FRSC resources are deployed reactively. This system identifies accident concentration zones, severity patterns, and actionable intervention points.

---

## Features

| Feature | Description |
|---------|-------------|
| KDE Hotspot Mapping | Kernel Density Estimation for accident concentration |
| DBSCAN Spatial Clustering | High-frequency accident zone identification |
| Severity Analysis | Minor / Serious / Fatal breakdown per corridor |
| Temporal Patterns | Hour-of-day, night/day, weekday/weekend breakdowns |
| Interactive Maps | Folium heatmap with clustered accident markers |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Geospatial | GeoPandas, Folium, Shapely |
| Machine Learning | scikit-learn (KDE, DBSCAN) |
| Data | pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |

---

## Project Structure

```
road-accident-hotspot-analysis/
├── src/
│   ├── data_loader.py     # Accident record ingestion & preprocessing
│   ├── analysis.py        # KDE hotspot detection, DBSCAN clustering
│   └── visualize.py       # Hotspot maps and severity charts
├── data/raw/              # FRSC accident logs, road network, weather data
├── models/                # Saved severity classifier
├── config.py              # Bandwidth, threshold, model parameters
├── main.py                # Pipeline entry point
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/Momahmoses/road-accident-hotspot-analysis.git
cd road-accident-hotspot-analysis
pip install -r requirements.txt
python main.py
```

---

## Data Sources

- FRSC accident reports (GPS, severity, road type, weather)
- Nigerian federal and state road network shapefiles
- NIMET weather station data
- FERMA road condition surveys

---

## Author

**Momah Moses**, Geospatial AI Engineer & Data Scientist
[GitHub](https://github.com/Momahmoses) · [Portfolio](https://momahmoses-ng-gis-portfolio.hf.space)
