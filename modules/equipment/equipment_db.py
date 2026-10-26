import pathlib

import pandas as pd

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
EQUIPMENT_PATH = DATA_DIR / "equipment.csv"


def ensure_equipment_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if EQUIPMENT_PATH.exists():
        return

    default_equipment = pd.DataFrame(
        [
            {"asset_id": "EQP-01", "category": "LHD Loader", "assigned_location": "Level 3 - North Block", "status": "Operational", "operating_time": 1420, "downtime": 200, "temperature_c": 46, "vibration_mm_s": 6.4},
            {"asset_id": "EQP-02", "category": "Truck", "assigned_location": "Level 2 - East Pit", "status": "Under Maintenance", "operating_time": 2890, "downtime": 1100, "temperature_c": 62, "vibration_mm_s": 8.9},
            {"asset_id": "EQP-03", "category": "Drill Rig", "assigned_location": "Level 1 - South Shaft", "status": "Operational", "operating_time": 1760, "downtime": 340, "temperature_c": 49, "vibration_mm_s": 7.2},
        ]
    )
    default_equipment.to_csv(EQUIPMENT_PATH, index=False)


def load_equipment() -> pd.DataFrame:
    ensure_equipment_file()
    return pd.read_csv(EQUIPMENT_PATH)


def save_equipment(equipment_df: pd.DataFrame) -> None:
    ensure_equipment_file()
    equipment_df.to_csv(EQUIPMENT_PATH, index=False)


def compute_availability(operating_time: float, downtime: float) -> float:
    """Calculate equipment availability percentage."""
    total_time = operating_time + downtime
    if total_time <= 0:
        return 0.0
    return (operating_time / total_time) * 100


def availability_status(availability: float, threshold: float = 85.0) -> str:
    if availability < threshold:
        return "Low Availability"
    return "Available"
