import pathlib

import pandas as pd

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
WORKERS_PATH = DATA_DIR / "workers.csv"
INCIDENTS_PATH = DATA_DIR / "incidents.csv"


def ensure_safety_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not WORKERS_PATH.exists():
        default_workers = pd.DataFrame(
            [
                {"worker_id": "KWM-001", "full_name": "Thabo Dlamini", "department": "Production", "role": "Drill Operator", "induction_status": "Passed", "medical_clearance": "Fit"},
                {"worker_id": "KWM-002", "full_name": "Aphiwe Nkosi", "department": "Maintenance", "role": "Technician", "induction_status": "Passed", "medical_clearance": "Fit"},
                {"worker_id": "KWM-003", "full_name": "Lerato Moloi", "department": "Safety", "role": "Safety Auditor", "induction_status": "Passed", "medical_clearance": "Fit"},
            ]
        )
        default_workers.to_csv(WORKERS_PATH, index=False)

    if not INCIDENTS_PATH.exists():
        default_incidents = pd.DataFrame(
            [
                {"incident_id": "INC-001", "date_logged": "2026-08-15 08:30:00", "classification": "Equipment Scrape", "likelihood": 2, "consequence": 3, "risk_rating": "Medium", "logged_by": "safety1", "status": "Resolved"},
                {"incident_id": "INC-002", "date_logged": "2026-08-17 10:45:00", "classification": "Unsafe Behaviour", "likelihood": 3, "consequence": 4, "risk_rating": "High", "logged_by": "safety1", "status": "Investigating"},
                {"incident_id": "INC-003", "date_logged": "2026-08-19 14:20:00", "classification": "Ventilation Concern", "likelihood": 4, "consequence": 5, "risk_rating": "Critical", "logged_by": "safety1", "status": "Open"},
            ]
        )
        default_incidents.to_csv(INCIDENTS_PATH, index=False)


def load_workers() -> pd.DataFrame:
    ensure_safety_files()
    return pd.read_csv(WORKERS_PATH)


def save_workers(workers_df: pd.DataFrame) -> None:
    ensure_safety_files()
    workers_df.to_csv(WORKERS_PATH, index=False)


def load_incidents() -> pd.DataFrame:
    ensure_safety_files()
    return pd.read_csv(INCIDENTS_PATH)


def save_incidents(incidents_df: pd.DataFrame) -> None:
    ensure_safety_files()
    incidents_df.to_csv(INCIDENTS_PATH, index=False)
