import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLE_DIR = os.path.join(DATA_DIR, "sample")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

STUDY_CORRIDORS = {
    "Lagos_Ibadan": {"lat_start": 6.5244, "lon_start": 3.3792, "lat_end": 7.3775, "lon_end": 3.9470},
    "Abuja_Kaduna": {"lat_start": 9.0579, "lon_start": 7.4951, "lat_end": 10.5105, "lon_end": 7.4165},
    "Benin_Ore": {"lat_start": 6.3350, "lon_start": 5.6037, "lat_end": 6.7408, "lon_end": 4.8613},
    "Kano_Zaria": {"lat_start": 12.0022, "lon_start": 8.5920, "lat_end": 11.1116, "lon_end": 7.7227},
    "Enugu_9th_Mile": {"lat_start": 6.4584, "lon_start": 7.5464, "lat_end": 6.8800, "lon_end": 7.4100},
}

FEATURE_COLS = [
    "road_curvature", "speed_limit_kmh", "road_width_m", "surface_condition",
    "n_junctions_nearby", "visibility_m", "rainfall_mm", "hour_of_day",
    "is_night", "is_weekend", "vehicle_count", "pedestrian_density",
]
TARGET_COL = "severity"  # 0=minor, 1=serious, 2=fatal

KDE_BANDWIDTH = 0.05
HOTSPOT_PERCENTILE = 85
