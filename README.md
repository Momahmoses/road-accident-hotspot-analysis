# Road Accident Hotspot Analysis & Traffic Safety

A GIS + spatial statistics system for mapping road accident hotspots on Nigerian highways — supporting FRSC (Federal Road Safety Corps) and state governments in targeting high-risk corridors for intervention.

## Overview

Combines GPS accident reports, road geometry, and weather data to:
- Compute KDE-based accident density heatmaps
- Identify hotspot zones above the 85th percentile
- Cluster accidents using DBSCAN spatial clustering
- Analyze severity patterns by corridor, hour, and weather condition

## Features

- **KDE Hotspot Mapping**: Kernel Density Estimation for accident concentration
- **DBSCAN Clustering**: Spatial clusters of high-frequency accident zones
- **Severity Analysis**: Minor / Serious / Fatal breakdown per corridor
- **Temporal Patterns**: Hourly distribution, night vs day, weekday vs weekend
- **Interactive Maps**: Folium heatmap with clustered accident markers

## Project Structure

```
road-accident-hotspot-analysis/
├── src/
│   ├── data_ingestion.py    # Synthetic accident data generation
│   ├── hotspot_analysis.py  # KDE, DBSCAN, severity analysis
│   └── visualization.py     # Folium maps and temporal charts
├── data/sample/
├── outputs/
├── config.py
├── main.py
└── requirements.txt
```

## Installation & Usage

```bash
pip install -r requirements.txt
python main.py
```

## Target Corridors

| Corridor | States | Known Risk |
|----------|--------|-----------|
| Lagos–Ibadan | Lagos/Oyo | High traffic volume |
| Abuja–Kaduna | FCT/Kaduna | Armed robbery, speeding |
| Benin–Ore | Edo/Ondo | Poor surface, curves |
| Kano–Zaria | Kano/Kaduna | Heavy trucks |
| Enugu–9th Mile | Enugu | Fog, sharp bends |

## Data Sources (Production)

- Accident records: FRSC accident database
- Road geometry: OpenStreetMap, OSGOF Nigeria
- Weather: NIMET, ERA5 historical
- Traffic counts: State Ministry of Works

## Author

**MOMAH MOSES .C.**  
Data Scientist & ML Engineer | [GitHub](https://github.com/Momahmoses)
