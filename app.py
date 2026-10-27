import os
import random
import datetime
import pandas as pd
import streamlit as st

# ==============================================================================
# App Configuration
# ==============================================================================
st.set_page_config(
    page_title="SafeMine360 - Khwezi Mining",
    page_icon="⚒️",
    layout="wide",
)

WORKERS_FILE = "workers.csv"
INCIDENTS_FILE = "safety_incidents.csv"
EQUIPMENT_FILE = "equipment.csv"
MAINTENANCE_FILE = "maintenance.csv"
RISK_FILE = "risk_assessments.csv"
ACCOUNTS_FILE = "user_accounts.csv"

# ==============================================================================
# Styling & Theme Customizations
# ==============================================================================
def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://googleapis.com');

        html, body, [data-testid="stAppViewContainer"], .stApp, .stMain {
            background: linear-gradient(180deg, rgba(6, 18, 27, 0.96) 0%, rgba(15, 23, 42, 0.98) 42%, rgba(3, 7, 18, 1) 100%);
            font-family: 'Inter', sans-serif;
            color: #f8fafc !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .stSidebar > div {
            background: rgba(15, 23, 42, 0.86);
            border-right: 1px solid rgba(148, 163, 184, 0.25);
        }

        .stSidebar *, .stSidebar p, .stSidebar label, .stSidebar div,
        .stSidebar span, .stSidebar li, .stSidebar a {
            color: #f8fafc !important;
        }

        .hero {
            padding: 2rem 1.5rem;
            border-radius: 22px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148,163,184,0.25);
            box-shadow: 0 12px 30px rgba(0,0,0,0.18);
            backdrop-filter: blur(5px);
        }

        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 0.3rem;
            line-height: 1.1;
        }

        .hero p {
            font-size: 1.08rem;
            color: #e2e8f0;
            margin-bottom: 0;
        }

        .small-label {
            color: #dbeafe;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .glass-card {
            background: rgba(15, 23, 42, 0.68);
            border: 1px solid rgba(148,163,184,0.20);
            border-radius: 18px;
            padding: 1rem 1rem 1.2rem;
            box-shadow: 0 10px 20px rgba(0,0,0,0.12);
        }

        .section-title {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        h1, h2, h3, h4, h5, h6, p, div, span, label, li, a, strong, b, em, code {
            color: #f8fafc !important;
        }

        .stMetric > div {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148,163,184,0.20);
            border-radius: 16px;
            padding: 0.7rem 0.9rem;
            box-shadow: 0 10px 18px rgba(0,0,0,0.10);
        }

        .stMetric label {
            color: #e2e8f0 !important;
            font-size: 0.8rem !important;
            font-weight: 600;
        }

        .stMetric [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #f8fafc 0%, #dfe7f5 100%);
            color: #0f172a;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.75rem 1.2rem;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 18px rgba(0,0,0,0.10);
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input,
        .stDateInput > div > div,
        .stTimeInput > div > div,
        .stFileUploader > div,
        .stRadio > div,
        .stCheckbox > div {
            background: rgba(255,255,255,0.96) !important;
            color: #0f172a !important;
            border-radius: 10px;
            border: 1px solid rgba(148,163,184,0.60);
        }

        .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label,
        .stDateInput label, .stTimeInput label, .stFileUploader label, .stCheckbox label, .stRadio label {
            color: #f8fafc !important;
            font-weight: 600;
        }

        .info-box {
            background: rgba(14,165,233,0.12);
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            color: #e0f2fe;
            margin-bottom: 0.8rem;
        }

        .success-box {
            background: rgba(34,197,94,0.10);
            border: 1px solid rgba(34,197,94,0.35);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            color: #dcfce7;
            margin-bottom: 0.8rem;
        }

        .warning-box {
            background: rgba(251,191,36,0.10);
            border: 1px solid rgba(251,191,36,0.35);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            color: #fef3c7;
            margin-bottom: 0.8rem;
        }

        .danger-box {
            background: rgba(239,68,68,0.12);
            border: 1px solid rgba(239,68,68,0.35);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            color: #fee2e2;
            margin-bottom: 0.8rem;
        }

        .alert-card-raw {
            background-color: #111827;
            border: 2px solid #ef4444;
            color: #f3f4f6 !important;
            font-family: 'Courier New', Courier, monospace;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            white-space: pre-wrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_custom_css()

# ==============================================================================
# Combined Synthetic Core Data Engine Lookups
# ==============================================================================
DEPARTMENTS = ["Mining", "Engineering", "Geology", "Safety"]
SHIFTS = ["Day", "Night"]
LOCATIONS = ["Pit A", "Pit B", "South Shaft", "North Shaft", "Crusher Plant", "Haul Road 3"]
SA_NAMES = ["Sipho Sithole", "Thabo Dlamini", "Aphiwe Nkosi", "Lerato Moloi", "Zama Khumalo", "Mpho Ncube", "Kagiso Mokoena"]

def make_default_workers():
    workers_data = []
    for i in range(1, 21):
        name = SA_NAMES[i % len(SA_NAMES)]
        ppe = random.choices(["Compliant", "Non-compliant"], weights=[0.9, 0.1])[0]
        fatigue = random.choices(["Low", "Medium", "High"], weights=[0.7, 0.2, 0.1])[0]
        nm = random.choices([0, 1, 2], weights=[0.8, 0.15, 0.05])[0]
        pi = random.choices([0, 1], weights=[0.9, 0.1])[0]
        score = (2 if ppe == "Non-compliant" else 0) + (2 if fatigue == "High" else 0) + (1 if nm > 0 else 0)
        level = "High" if score >= 4 else ("Medium" if score >= 2 else "Low")
        
        workers_data.append({
            "Name": f"{name} ({i})", "Worker ID": f"W-{i:03d}", "Department": random.choice(DEPARTMENTS),
            "Training Status": "Completed" if i % 4 != 0 else "Pending", "Job Role": "Operator",
            "Shift": random.choice(SHIFTS), "PPE Compliance": ppe, "Fatigue Level": fatigue,
            "Safety Observations": "Routine lookups valid.", "Near Misses": nm, "Previous Incidents": pi, "Risk Level": level
        })
    return pd.DataFrame(workers_data)

def make_default_incidents():
    inc_data = []
    for i in range(1, 11):
        inc_data.append({
            "Incident ID": i, "Date": str(datetime.date(2026, 8, i)), "Time": f"1{i}:15", "Shift": random.choice(SHIFTS),
            "Location": random.choice(LOCATIONS), "Department": random.choice(DEPARTMENTS),
            "Incident Type": random.choice(["Near Miss", "Unsafe Condition", "Injury"]), "Severity": random.choice(["Medium", "High", "Critical"]),
            "Injury Status": "No", "Lost-Time Injury": "No", "Description": "Dynamic area shift variance recorded.",
            "Cause": "Visibility limits.", "Corrective Action": "Barricades established.", "Incident Status": "Open" if i % 3 == 0 else "Resolved"
        })
    return pd.DataFrame(inc_data)

def make_default_equipment():
    eq_data = []
    types = ["Truck", "Excavator", "Drill"]
    for i in range(1, 11):
        eq_data.append({
            "Equipment Name": f"{random.choice(types)} Model X", "Equipment ID": f"EQ-{100+i}", "Equipment Type": random.choice(types),
            "Manufacturer": "CAT", "Operating Hours": float(i * 500), "Temperature": float(70 + (i * 4)), "Vibration": float(3.0 + (i * 0.6)),
            "Fuel Level": 85 - (i * 3), "Brakes": "Good", "Tyres": "Good", "Engine": "Good" if i % 5 != 0 else "Needs Repair",
            "Downtime": float(i * 1.5), "Maintenance Status": "Up to date" if i % 3 != 0 else "Overdue"
        })
    return pd.DataFrame(eq_data)

def make_default_maintenance():
    return pd.DataFrame([
        {"Equipment Name": "Truck Model X", "Equipment ID": "EQ-101", "Maintenance Type": "Routine Inspection", "Maintenance Date": "2026-08-01", "Maintenance Status": "Completed", "Maintenance Notes": "Filters re-cleared.", "Operating Hours": 1500.0, "Downtime": 4.5, "Availability (%)": 95.2, "Next Maintenance Date": "2026-09-15"},
