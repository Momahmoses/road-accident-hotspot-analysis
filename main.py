"""Main pipeline: Road Accident Hotspot Analysis & Traffic Safety."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.data_ingestion import load_or_generate
from src.hotspot_analysis import compute_kde, identify_hotspots, dbscan_clusters, severity_analysis
from src.visualization import create_hotspot_map, temporal_analysis


def main():
    print("=" * 60)
    print("  Road Accident Hotspot Analysis & Traffic Safety")
    print("  Corridors: Lagos-Ibadan, Abuja-Kaduna, Benin-Ore,")
    print("             Kano-Zaria, Enugu-9th Mile")
    print("=" * 60)

    print("\n[1/5] Loading accident data...")
    gdf = load_or_generate()
    print(f"  {len(gdf):,} accidents | Fatal: {(gdf['severity']==2).sum():,} | Serious: {(gdf['severity']==1).sum():,}")

    print("\n[2/5] Computing KDE density...")
    density = compute_kde(gdf)
    gdf = identify_hotspots(gdf, density)
    hotspot_count = gdf["is_hotspot"].sum()
    print(f"  Hotspot points identified: {hotspot_count:,} ({hotspot_count/len(gdf):.1%})")

    print("\n[3/5] DBSCAN spatial clustering...")
    gdf = dbscan_clusters(gdf)

    print("\n[4/5] Severity analysis by corridor...")
    corridor_df = severity_analysis(gdf)
    print(f"\n  Most dangerous corridor: {corridor_df.index[0]}")

    print("\n[5/5] Generating hotspot maps...")
    create_hotspot_map(gdf)
    temporal_analysis(gdf)

    print("\n✓ Pipeline complete. Outputs saved to ./outputs/")


if __name__ == "__main__":
    main()
