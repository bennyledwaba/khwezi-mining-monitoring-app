from pathlib import Path
import os

import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SafeMine360 - Health, Safety and Equipment Monitoring",
    page_icon="⛏️",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

WORKERS_FILE = DATA_DIR / "workers.csv"
INCIDENTS_FILE = DATA_DIR / "incidents.csv"
EQUIPMENT_FILE = DATA_DIR / "equipment.csv"
MAINTENANCE_FILE = DATA_DIR / "maintenance.csv"
RISK_FILE = DATA_DIR / "risk_assessments.csv"
ACCOUNTS_FILE = DATA_DIR / "user_accounts.csv"

# -----------------------------------------------------------------------------
# Defaults and fallback datasets
# -----------------------------------------------------------------------------
def make_default_workers():
    data = [
        {
            "Name": "Sipho Sithole (1)",
            "Worker ID": "W-001",
            "Department": "Mining",
            "Training Status": "Completed",
            "Job Role": "Operator",
            "Shift": "Day",
            "PPE Compliance": "Compliant",
            "Fatigue Level": "Low",
            "Safety Observations": "Routine checks passed.",
            "Near Misses": 0,
            "Previous Incidents": 0,
            "Risk Level": "Low",
        },
        {
            "Name": "Thabo Dlamini (2)",
            "Worker ID": "W-002",
            "Department": "Safety",
            "Training Status": "Completed",
            "Job Role": "Safety Officer",
            "Shift": "Night",
            "PPE Compliance": "Compliant",
            "Fatigue Level": "Medium",
            "Safety Observations": "Routine checks passed.",
            "Near Misses": 1,
            "Previous Incidents": 0,
            "Risk Level": "Medium",
        },
        {
            "Name": "Aphiwe Nkosi (3)",
            "Worker ID": "W-003",
            "Department": "Engineering",
            "Training Status": "Pending",
            "Job Role": "Technician",
            "Shift": "Day",
            "PPE Compliance": "Non-compliant",
            "Fatigue Level": "High",
            "Safety Observations": "PPE issue flagged.",
            "Near Misses": 2,
            "Previous Incidents": 1,
            "Risk Level": "High",
        },
    ]
    return pd.DataFrame(data)


def make_default_incidents():
    return pd.DataFrame(
        [
            {
                "Incident ID": 1,
                "Date": "2026-08-01",
                "Time": "08:15",
                "Shift": "Day",
                "Location": "Pit A",
                "Department": "Mining",
                "Incident Type": "Near Miss",
                "Severity": "Medium",
                "Injury Status": "No",
                "Lost-Time Injury": "No",
                "Description": "Near miss on haul road.",
                "Cause": "Limited visibility.",
                "Corrective Action": "Barricades installed.",
                "Incident Status": "Resolved",
            },
            {
                "Incident ID": 2,
                "Date": "2026-08-02",
                "Time": "21:05",
                "Shift": "Night",
                "Location": "South Shaft",
                "Department": "Safety",
                "Incident Type": "Unsafe Condition",
                "Severity": "High",
                "Injury Status": "No",
                "Lost-Time Injury": "No",
                "Description": "Loose rock reported in shaft.",
                "Cause": "Poor area inspection.",
                "Corrective Action": "Area isolated and inspected.",
                "Incident Status": "Open",
            },
        ]
    )


def make_default_equipment():
    return pd.DataFrame(
        [
            {
                "Equipment Name": "Truck Model X",
                "Equipment ID": "EQ-101",
                "Equipment Type": "Truck",
                "Manufacturer": "CAT",
                "Operating Hours": 1500.0,
                "Temperature": 78.0,
                "Vibration": 3.8,
                "Fuel Level": 70,
                "Brakes": "Good",
                "Tyres": "Good",
                "Engine": "Good",
                "Downtime": 4.5,
                "Maintenance Status": "Up to date",
            },
            {
                "Equipment Name": "Excavator Model Y",
                "Equipment ID": "EQ-102",
                "Equipment Type": "Excavator",
                "Manufacturer": "CAT",
                "Operating Hours": 1800.0,
                "Temperature": 102.0,
                "Vibration": 8.4,
                "Fuel Level": 45,
                "Brakes": "Good",
                "Tyres": "Needs Repair",
                "Engine": "Needs Repair",
                "Downtime": 8.0,
                "Maintenance Status": "Overdue",
            },
        ]
    )


def make_default_maintenance():
    return pd.DataFrame(
        [
            {
                "Equipment Name": "Truck Model X",
                "Equipment ID": "EQ-101",
                "Maintenance Type": "Routine Inspection",
                "Maintenance Date": "2026-08-01",
                "Maintenance Status": "Completed",
                "Maintenance Notes": "Filters cleaned and checked.",
                "Operating Hours": 1500.0,
                "Downtime": 4.5,
                "Availability (%)": 95.2,
                "Next Maintenance Date": "2026-09-15",
            }
        ]
    )


def make_default_risk():
    return pd.DataFrame(
        [
            {
                "Hazard": "Loose ground in pit wall",
                "Location": "Pit A",
                "Likelihood": 4,
                "Consequence": 4,
                "Risk Score": 16,
                "Risk Level": "High",
            }
        ]
    )


def make_default_accounts():
    return pd.DataFrame(
        [
            {"Username": "admin", "Password": "admin@khwezi", "Role": "Administrator"},
            {"Username": "safety", "Password": "safety@khwezi", "Role": "Safety Officer"},
            {"Username": "engineer", "Password": "engineer@khwezi", "Role": "Mining Engineer"},
            {"Username": "maintenance", "Password": "maintenance@khwezi", "Role": "Maintenance Engineer"},
            {"Username": "manager", "Password": "manager@khwezi", "Role": "Manager"},
        ]
    )


def ensure_default_data_files():
    defaults = {
        WORKERS_FILE: make_default_workers,
        INCIDENTS_FILE: make_default_incidents,
        EQUIPMENT_FILE: make_default_equipment,
        MAINTENANCE_FILE: make_default_maintenance,
        RISK_FILE: make_default_risk,
        ACCOUNTS_FILE: make_default_accounts,
    }

    for path, factory in defaults.items():
        if not path.exists():
            df = factory()
            df.to_csv(path, index=False)


ensure_default_data_files()

# -----------------------------------------------------------------------------
# Theme / Styling
# -----------------------------------------------------------------------------
def inject_custom_css():
    st.markdown(
        """
        <style>
        :root {
            --bg: #101820;
            --panel: #1d2a35;
            --card: #2a3a46;
            --soft-card: #313f4d;
            --muted: #a7b6c2;
            --text: #f3f7fb;
            --text-strong: #ffffff;
            --primary: #7dd3fc;
            --secondary: #34d399;
            --warning: #fbbf24;
            --danger: #f87171;
            --shadow: rgba(0,0,0,0.28);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0b1220 0%, #142331 100%);
            color: var(--text);
        }

        .stApp { color: var(--text); }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .main-header {
            background: rgba(30, 42, 51, 0.9);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 10px 30px var(--shadow);
            margin-bottom: 1.25rem;
        }

        .title-badge {
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            color: var(--text-strong);
        }

        .welcome-card {
            background: linear-gradient(135deg, rgba(41,63,78,0.95), rgba(25,37,47,0.95));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.5rem 1.5rem 1.1rem 1.5rem;
            box-shadow: 0 12px 30px var(--shadow);
            margin-bottom: 1.2rem;
        }

        .welcome-title {
            font-size: 2.6rem;
            font-weight: 800;
            color: #f5fafc;
            margin: 0;
        }

        .welcome-subtitle {
            font-size: 1.08rem;
            color: #d7e1ea;
            margin-top: 0.5rem;
        }

        .info-panel {
            background: rgba(26, 39, 49, 0.95);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1.3rem 1.4rem;
            box-shadow: 0 8px 25px var(--shadow);
            margin-bottom: 1rem;
        }

        .status-text {
            color: var(--text-strong);
            font-size: 1.2rem;
            font-weight: 700;
        }

        .role-text {
            color: var(--text);
            font-size: 1.08rem;
            font-weight: 600;
            margin-top: 0.6rem;
        }

        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input,
        .stSelectbox > div > div > div,
        .stTextArea > div > textarea {
            background: rgba(255,255,255,0.04);
            color: var(--text-strong);
            border: 1px solid rgba(255,255,255,0.12);
        }

        .stTextInput label, .stSelectbox label, .stNumberInput label,
        .stDateInput label, .stTimeInput label, .stTextArea label {
            color: var(--text-strong) !important;
            font-weight: 600;
        }

        ::placeholder {
            color: #dfeaf4 !important;
            opacity: 0.9;
        }

        .stButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            background: linear-gradient(180deg, #e7edf5, #dfe8f3);
            color: #1d2a35;
            font-weight: 800;
            padding: 0.7rem 1rem;
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, #f4f8ff, #dfeaf3);
            border-color: rgba(255,255,255,0.3);
        }

        .stSidebar {
            background: #101e2a;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        .stSidebar .block-container { padding-top: 1rem; }

        .sidebar-title {
            color: #f4f8fb !important;
            font-size: 1.8rem;
            font-weight: 800;
        }

        .stSidebar .stSelectbox label, .stSidebar .stRadio label {
            color: var(--text) !important;
            font-weight: 600;
        }

        .stSelectbox > div > div > div > div { color: var(--text-strong) !important; }
        .stDataFrame {
            background: rgba(17, 24, 39, 0.55);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .stMetric {
            background: rgba(32, 46, 58, 0.85);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }

        .css-1d391kg, .css-1h6fyg7, .css-1pqrn0e { color: var(--text) !important; }
        .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
            border-radius: 12px;
            font-weight: 600;
        }

        .stTabs [role="tablist"] { gap: 0.5rem; }
        .stTabs [role="tab"] {
            color: var(--text) !important;
            background: rgba(255,255,255,0.04);
            border-radius: 10px 10px 0 0;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background: rgba(125, 211, 252, 0.12);
            color: #dff7ff !important;
        }

        .nav-card {
            background: rgba(32, 46, 58, 0.88);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            border: 1px solid rgba(255,255,255,0.08);
            margin-top: 0.5rem;
        }

        .section-title {
            color: var(--text-strong);
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .muted-text { color: var(--muted); }

        @media (max-width: 768px) {
            .welcome-title { font-size: 2rem; }
            .title-badge { font-size: 1.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_custom_css()

# -----------------------------------------------------------------------------
# Session data helpers
# -----------------------------------------------------------------------------
def path_exists(p):
    return p.exists()


def read_csv_safe(path, fallback_factory=None):
    if path_exists(path):
        return pd.read_csv(path)
    if fallback_factory is not None:
        df = fallback_factory()
        df.to_csv(path, index=False)
        return df
    return pd.DataFrame()


if "equipment" not in st.session_state:
    st.session_state.equipment = read_csv_safe(EQUIPMENT_FILE, make_default_equipment).to_dict("records")

if "workers" not in st.session_state:
    st.session_state.workers = read_csv_safe(WORKERS_FILE, make_default_workers).to_dict("records")

if "maintenance_records" not in st.session_state:
    st.session_state.maintenance_records = read_csv_safe(MAINTENANCE_FILE, make_default_maintenance).to_dict("records")

if "risk_records" not in st.session_state:
    st.session_state.risk_records = read_csv_safe(RISK_FILE, make_default_risk).to_dict("records")

# -----------------------------------------------------------------------------
# Access control
# -----------------------------------------------------------------------------
users = {
    "admin": {"password": "admin@khwezi", "role": "Administrator"},
    "safety": {"password": "safety@khwezi", "role": "Safety Officer"},
    "engineer": {"password": "engineer@khwezi", "role": "Mining Engineer"},
    "maintenance": {"password": "maintenance@khwezi", "role": "Maintenance Engineer"},
    "manager": {"password": "manager@khwezi", "role": "Manager"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------------------------------------------------------
# Sidebar / logout
# -----------------------------------------------------------------------------
def render_logged_in_topbar():
    st.sidebar.markdown(
        """
        <div class="nav-card">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom: 12px;">
                <div style="font-size:1.8rem;">⛏️</div>
                <div style="font-size:1.6rem; font-weight:800; color:#f5f9ff;">SAFEMINE360</div>
            </div>
            <div class="status-text">Logged in as: {username}</div>
            <div class="role-text">Role: {role}</div>
        </div>
        """.format(username=st.session_state.username, role=st.session_state.role),
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.session_state.pop("role", None)
        st.rerun()


# -----------------------------------------------------------------------------
# Login screen
# -----------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="welcome-card">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom: 0.5rem;">
                <div style="font-size:2.5rem;">🛡️</div>
                <div class="title-badge">SAFEMINE360</div>
            </div>
            <div class="welcome-subtitle">Health, Safety and Equipment Monitoring for Mining Operations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="max-width: 700px; margin: 1.5rem auto 0.5rem auto;">
            <div class="info-panel">
                <div style="font-size: 1.1rem; color: #dfeaf3; margin-bottom: 0.4rem;">Welcome back</div>
                <div style="font-size: 2.3rem; font-weight: 800; color: #ffffff;">Mine Safety Access Portal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_col1, login_col2 = st.columns([1.2, 1.5])
    with login_col2:
        st.markdown(
            """
            <div class="info-panel">
                <div style="font-size: 1.5rem; font-weight: 700; color: #f5faff; margin-bottom: 1rem;">Login</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            if username in users and password == users[username]["password"]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = users[username]["role"]
                st.rerun()
            else:
                st.error("Invalid username and/or password")

        st.markdown(
            """
            <div style="margin-top: 1rem; color: #d7e1ea; font-size: 0.95rem;">
                Use one of the default accounts:<br>
                <b>admin</b> / admin@khwezi<br>
                <b>safety</b> / safety@khwezi<br>
                <b>engineer</b> / engineer@khwezi<br>
                <b>maintenance</b> / maintenance@khwezi<br>
                <b>manager</b> / manager@khwezi
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()

# -----------------------------------------------------------------------------
# Logged-in app
# -----------------------------------------------------------------------------
render_logged_in_topbar()

st.title("MineGuard")
st.subheader("Health, Safety and Equipment Monitoring")
st.sidebar.title("Navigation")

role_pages = {
    "Administrator": [
        "Dashboard",
        "Worker Safety",
        "Safety Incidents",
        "Equipment Monitoring",
        "Maintenance",
        "Risk Assessment",
        "Alerts",
        "Data Analysis",
    ],
    "Safety Officer": ["Dashboard", "Worker Safety", "Safety Incidents", "Risk Assessment", "Alerts"],
    "Mining Engineer": ["Dashboard", "Worker Safety", "Safety Incidents", "Equipment Monitoring", "Maintenance", "Risk Assessment", "Alerts"],
    "Maintenance Engineer": ["Dashboard", "Equipment Monitoring", "Maintenance", "Alerts"],
    "Manager": ["Dashboard", "Worker Safety", "Safety Incidents", "Equipment Monitoring", "Maintenance", "Risk Assessment", "Alerts", "Data Analysis"],
}

page = st.sidebar.selectbox("Choose a page", role_pages[st.session_state.role])

if page == "Dashboard":
    st.header("Mining Dashboard")
    st.write("Overview of Worker Safety, Incidents and Equipment.")

    workers_df = pd.DataFrame(st.session_state.workers)
    incidents_df = read_csv_safe(INCIDENTS_FILE, make_default_incidents)
    equipment_df = pd.DataFrame(st.session_state.equipment)

    total_workers = len(workers_df)
    total_incidents = len(incidents_df)
    open_incidents = len(incidents_df[incidents_df["Incident Status"].astype(str).str.lower().ne("resolved")]) if not incidents_df.empty and "Incident Status" in incidents_df.columns else 0
    total_equipment = len(equipment_df)
    total_near_misses = 0
    if not incidents_df.empty and "Incident Type" in incidents_df.columns:
        total_near_misses = incidents_df[incidents_df["Incident Type"].astype(str).str.contains("near miss", case=False, na=False)].shape[0]

    ppe_compliance = 0
    if not workers_df.empty and "PPE Compliance" in workers_df.columns:
        ppe_compliance = workers_df["PPE Compliance"].astype(str).str.lower().isin(["yes", "compliant", "true", "complies"]).sum()
    ppe_compliance_percentage = (ppe_compliance / len(workers_df) * 100) if len(workers_df) else 0

    equipment_alerts = 0
    critical_equipment_alerts = 0
    if not equipment_df.empty:
        for _, row in equipment_df.iterrows():
            has_issue = False
            if row.get("Temperature", 0) >= 80:
                has_issue = True
            if row.get("Vibration", 0) >= 5:
                has_issue = True
            if str(row.get("Brakes", "")).lower() == "needs repair":
                has_issue = True
            if str(row.get("Tyres", "")).lower() == "needs repair":
                has_issue = True
            if str(row.get("Engine", "")).lower() == "needs repair":
                has_issue = True
            if str(row.get("Maintenance Status", "")).lower() == "overdue":
                has_issue = True
            if has_issue:
                equipment_alerts += 1
            if row.get("Temperature", 0) > 100 or row.get("Vibration", 0) > 8:
                critical_equipment_alerts += 1

    maintenance_df = read_csv_safe(MAINTENANCE_FILE, make_default_maintenance)
    average_availability = 0
    if not maintenance_df.empty and "Availability (%)" in maintenance_df.columns:
        availability_values = pd.to_numeric(maintenance_df["Availability (%)"], errors="coerce").dropna()
        if not availability_values.empty:
            average_availability = availability_values.mean()

    risk_df = read_csv_safe(RISK_FILE, make_default_risk)
    high_risk_observations = 0
    if not risk_df.empty and "Risk Level" in risk_df.columns:
        high_risk_observations = risk_df["Risk Level"].astype(str).str.lower().isin(["high", "critical"]).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Registered Workers", total_workers)
    c2.metric("Safety Incidents", total_incidents)
    c3.metric("Near Misses", total_near_misses)

    c4, c5, c6 = st.columns(3)
    c4.metric("Open Incidents", open_incidents)
    c5.metric("Equipment Records", total_equipment)
    c6.metric("Equipment Alerts", equipment_alerts)

    c7, c8, c9 = st.columns(3)
    c7.metric("Workers Complying with PPE", int(ppe_compliance))
    c8.metric("PPE Compliance", f"{ppe_compliance_percentage:.1f}%")
    c9.metric("Average Equipment Availability", f"{average_availability:.1f}%")

    st.metric("High-Risk Observations", int(high_risk_observations))
    st.metric("Critical Equipment Alerts", int(critical_equipment_alerts))

    st.divider()
    st.subheader("Safety Incident Overview")
    if not incidents_df.empty and "Severity" in incidents_df.columns:
        st.bar_chart(incidents_df["Severity"].value_counts())
    else:
        st.info("No safety incident data is available for the chart.")

elif page == "Worker Safety":
    st.header("Worker Safety")
    st.subheader("Register a Worker")

    worker_name = st.text_input("Worker Name")
    worker_id = st.text_input("Worker ID")
    department = st.selectbox("Department", ["Mining", "Engineering", "Geology", "Safety"])
    training = st.selectbox("Safety Training Status", ["Completed", "Pending"])
    job_role = st.text_input("Job Role")
    shift = st.selectbox("Shift", ["Day", "Night"])
    ppe_compliance = st.selectbox("PPE Compliance", ["Compliant", "Non-compliant"])
    fatigue_level = st.selectbox("Fatigue Level", ["Low", "Medium", "High"])
    safety_observations = st.text_area("Safety Observations")
    near_misses = st.number_input("Number of Near Misses", min_value=0, step=1)
    previous_incidents = st.number_input("Previous Incidents", min_value=0, step=1)

    if st.button("Register Worker"):
        if not worker_name.strip() or not worker_id.strip():
            st.error("Please enter the worker's name and ID.")
        elif any(str(worker.get("Worker ID", "")) == worker_id.strip() for worker in st.session_state.workers):
            st.error("This Worker ID is already registered.")
        else:
            worker_risk_score = 0
            if ppe_compliance == "Non-compliant":
                worker_risk_score += 2
            if fatigue_level == "High":
                worker_risk_score += 2
            if near_misses > 0:
                worker_risk_score += 1
            if previous_incidents > 0:
                worker_risk_score += 1

            if worker_risk_score >= 4:
                risk_level = "High"
            elif worker_risk_score >= 2:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            worker = {
                "Name": worker_name.strip(),
                "Worker ID": worker_id.strip(),
                "Department": department,
                "Training Status": training,
                "Job Role": job_role,
                "Shift": shift,
                "PPE Compliance": ppe_compliance,
                "Fatigue Level": fatigue_level,
                "Safety Observations": safety_observations,
                "Near Misses": near_misses,
                "Previous Incidents": previous_incidents,
                "Risk Level": risk_level,
            }

            st.session_state.workers.append(worker)
            pd.DataFrame(st.session_state.workers).to_csv(WORKERS_FILE, index=False)
            st.success("Worker registered and saved successfully!")

            if risk_level == "High":
                st.error("HIGH RISK: Investigate this worker's safety conditions.")
            elif risk_level == "Medium":
                st.warning("MEDIUM RISK: Review this worker's safety conditions.")
            else:
                st.success("LOW RISK: No immediate warning from these indicators.")

    if st.session_state.workers:
        st.subheader("Registered Workers")
        st.dataframe(pd.DataFrame(st.session_state.workers), use_container_width=True)

elif page == "Safety Incidents":
    st.header("Safety Incidents")
    st.subheader("Record a Safety Incident")

    incident_date = st.date_input("Incident Date")
    incident_time = st.time_input("Incident Time")
    shift = st.selectbox("Shift", ["Day", "Night"])
    location = st.text_input("Incident Location")
    department = st.selectbox("Department", ["Mining", "Engineering", "Geology", "Safety"])
    incident_type = st.selectbox("Incident Type", ["Near Miss", "Unsafe Condition", "Injury", "Equipment Incident", "Other"])
    severity = st.selectbox("Incident Severity", ["Low", "Medium", "High", "Critical"])
    injury_status = st.selectbox("Was anyone injured?", ["No", "Yes"])
    lost_time_injury = st.selectbox("Lost-Time Injury?", ["No", "Yes"])
    description = st.text_area("Incident Description")
    cause = st.text_area("Incident Cause")
    corrective_action = st.text_area("Corrective Action")
    incident_status = st.selectbox("Incident Status", ["Open", "Under Investigation", "Resolved"])

    if st.button("Submit Incident"):
        if not location.strip() or not description.strip():
            st.error("Please enter the incident location and description.")
        else:
            incidents_df = read_csv_safe(INCIDENTS_FILE, make_default_incidents)
            if not incidents_df.empty and "Incident ID" in incidents_df.columns:
                max_id = pd.to_numeric(incidents_df["Incident ID"], errors="coerce").max()
                incident_id = int(max_id) + 1 if pd.notna(max_id) else 1
            else:
                incident_id = 1

            incident = {
                "Incident ID": incident_id,
                "Date": str(incident_date),
                "Time": str(incident_time),
                "Shift": shift,
                "Location": location.strip(),
                "Department": department,
                "Incident Type": incident_type,
                "Severity": severity,
                "Injury Status": injury_status,
                "Lost-Time Injury": lost_time_injury,
                "Description": description.strip(),
                "Cause": cause,
                "Corrective Action": corrective_action,
                "Incident Status": incident_status,
            }

            new_df = pd.concat([incidents_df, pd.DataFrame([incident])], ignore_index=True)
            new_df.to_csv(INCIDENTS_FILE, index=False)
            st.success("Incident recorded and saved successfully!")

    st.divider()
    st.subheader("Saved Safety Incidents")
    incidents_df = read_csv_safe(INCIDENTS_FILE, make_default_incidents)
    if not incidents_df.empty:
        st.metric("Total Recorded Incidents", len(incidents_df))
        search_text = st.text_input("Search by ID, location, cause or description")
        col1, col2 = st.columns(2)
        severity_options = ["All"] + sorted(incidents_df["Severity"].dropna().astype(str).unique().tolist())
        status_options = ["All"] + sorted(incidents_df["Incident Status"].dropna().astype(str).unique().tolist())

        with col1:
            selected_severity = st.selectbox("Filter by Severity", severity_options)
        with col2:
            selected_status = st.selectbox("Filter by Status", status_options)

        filtered = incidents_df.copy()
        if search_text.strip():
            matches = filtered.astype(str).apply(lambda col: col.str.contains(search_text.strip(), case=False, na=False)).any(axis=1)
            filtered = filtered[matches]
        if selected_severity != "All":
            filtered = filtered[filtered["Severity"].astype(str) == selected_severity]
        if selected_status != "All":
            filtered = filtered[filtered["Incident Status"].astype(str) == selected_status]

        st.write(f"Matching incidents: {len(filtered)}")
        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("No safety incidents have been recorded yet.")

elif page == "Equipment Monitoring":
    st.header("Equipment Monitoring")
    st.subheader("Equipment Condition Report")

    equipment_name = st.text_input("Equipment Name")
    equipment_id = st.text_input("Equipment ID")
    equipment_type = st.selectbox("Equipment Type", ["Truck", "Excavator", "Drill", "Loader", "Other"])
    manufacturer = st.text_input("Manufacturer")
    operating_hours = st.number_input("Operating Hours", min_value=0.0, step=1.0)
    temperature = st.number_input("Engine Temperature (°C)", min_value=0.0, step=1.0)
    vibration = st.number_input("Vibration (mm/s)", min_value=0.0, step=0.1)
    fuel_level = st.slider("Fuel Level (%)", 0, 100, 50)
    brakes = st.selectbox("Brakes", ["Good", "Needs Repair"])
    tyres = st.selectbox("Tyres", ["Good", "Needs Repair"])
    engine = st.selectbox("Engine", ["Good", "Needs Repair"])
    downtime = st.number_input("Downtime (hours)", min_value=0.0, step=1.0)
    maintenance_status = st.selectbox("Maintenance Status", ["Up to date", "Due", "Overdue", "Under maintenance"])

    if temperature > 100:
        st.error("CRITICAL ALERT: Engine temperature is too high!")
    elif temperature >= 80:
        st.warning("WARNING: Engine temperature is elevated.")
    else:
        st.success("Engine temperature is in the normal range.")

    if vibration > 8:
        st.error("CRITICAL ALERT: Vibration is too high!")
    elif vibration >= 5:
        st.warning("WARNING: Vibration is elevated.")
    else:
        st.success("Vibration is in the normal range.")

    if st.button("Submit Equipment Report"):
        if equipment_name.strip() and equipment_id.strip():
            equipment = {
                "Equipment Name": equipment_name.strip(),
                "Equipment ID": equipment_id.strip(),
                "Equipment Type": equipment_type,
                "Manufacturer": manufacturer,
                "Operating Hours": operating_hours,
                "Temperature": temperature,
                "Vibration": vibration,
                "Fuel Level": fuel_level,
                "Brakes": brakes,
                "Tyres": tyres,
                "Engine": engine,
                "Downtime": downtime,
                "Maintenance Status": maintenance_status,
            }

            existing_df = read_csv_safe(EQUIPMENT_FILE, make_default_equipment)
            updated_df = pd.concat([existing_df, pd.DataFrame([equipment])], ignore_index=True)
            updated_df.to_csv(EQUIPMENT_FILE, index=False)
            st.session_state["equipment"] = updated_df.to_dict("records")
            st.success("Equipment report submitted and saved successfully!")
        else:
            st.error("Please enter the equipment name and ID.")

    st.subheader("Equipment Reports")
    st.dataframe(pd.DataFrame(st.session_state.equipment), use_container_width=True)

elif page == "Maintenance":
    st.header("Equipment Maintenance")
    st.write("Record and manage mining equipment maintenance.")
    st.subheader("Record Maintenance")

    equipment_name = st.text_input("Equipment Name", key="maintenance_equipment_name")
    equipment_id = st.text_input("Equipment ID", key="maintenance_equipment_id")
    maintenance_type = st.selectbox("Maintenance Type", ["Routine Inspection", "Preventive Maintenance", "Repair"], key="maintenance_type")
    maintenance_date = st.date_input("Maintenance Date", key="maintenance_date")
    status = st.selectbox("Maintenance Status", ["Scheduled", "In Progress", "Completed"], key="maintenance_status")
    notes = st.text_area("Maintenance Notes", key="maintenance_notes")
    operating_hours = st.number_input("Operating Hours", min_value=0.0, step=1.0, key="maintenance_operating_hours")
    downtime = st.number_input("Downtime (hours)", min_value=0.0, step=1.0, key="maintenance_downtime")
    next_maintenance_date = st.date_input("Next Maintenance Date", key="next_maintenance_date")

    availability = ((operating_hours / (operating_hours + downtime)) * 100) if (operating_hours + downtime) > 0 else 0
    st.metric("Equipment Availability", f"{availability:.1f}%")

    if status == "Scheduled" and next_maintenance_date < pd.Timestamp.today().date():
        st.error("ALERT: Scheduled maintenance is overdue.")
    if downtime > 10:
        st.warning("ALERT: Equipment has excessive downtime.")
    if availability < 70 and (operating_hours + downtime) > 0:
        st.warning("WARNING: Equipment availability is low.")

    if st.button("Submit Maintenance Record"):
        if equipment_name.strip() and equipment_id.strip():
            maintenance_record = {
                "Equipment Name": equipment_name.strip(),
                "Equipment ID": equipment_id.strip(),
                "Maintenance Type": maintenance_type,
                "Maintenance Date": str(maintenance_date),
                "Maintenance Status": status,
                "Maintenance Notes": notes,
                "Operating Hours": operating_hours,
                "Downtime": downtime,
                "Availability (%)": round(availability, 1),
                "Next Maintenance Date": str(next_maintenance_date),
                "Overdue": next_maintenance_date < pd.Timestamp.today().date() and status != "Completed",
            }

            existing_df = read_csv_safe(MAINTENANCE_FILE, make_default_maintenance)
            updated_df = pd.concat([existing_df, pd.DataFrame([maintenance_record])], ignore_index=True)
            updated_df.to_csv(MAINTENANCE_FILE, index=False)
            st.session_state["maintenance_records"] = updated_df.to_dict("records")
            st.success("Maintenance record submitted and saved successfully!")
        else:
            st.error("Please enter the equipment name and equipment ID.")

    st.subheader("Saved Maintenance Records")
    st.dataframe(read_csv_safe(MAINTENANCE_FILE, make_default_maintenance), use_container_width=True)

elif page == "Risk Assessment":
    st.header("Mining Risk Assessment")
    st.write("Assess a hazard by multiplying its likelihood score by its consequence score.")

    hazard = st.text_input("Hazard Description")
    location = st.text_input("Hazard Location")
    likelihood = st.selectbox("Likelihood (1 = Rare, 5 = Almost Certain)", [1, 2, 3, 4, 5])
    consequence = st.selectbox("Consequence (1 = Insignificant, 5 = Catastrophic)", [1, 2, 3, 4, 5])

    risk_score = likelihood * consequence
    if risk_score <= 4:
        risk_level = "Low"
    elif risk_score <= 9:
        risk_level = "Medium"
    elif risk_score <= 16:
        risk_level = "High"
    else:
        risk_level = "Critical"

    st.divider()
    st.metric("Risk Score", f"{risk_score}/25")
    st.write("**Risk Level:**", risk_level)

    if risk_level == "Low":
        st.success("Maintain existing safety controls and monitor the hazard.")
    elif risk_level == "Medium":
        st.info("Review the hazard and improve controls where necessary.")
    elif risk_level == "High":
        st.warning("Take action to reduce the risk as soon as possible.")
    else:
        st.error("Critical risk: urgent action is required.")

    if st.button("Save Risk Assessment"):
        if hazard.strip() and location.strip():
            risk_record = {
                "Hazard": hazard.strip(),
                "Location": location.strip(),
                "Likelihood": likelihood,
                "Consequence": consequence,
                "Risk Score": risk_score,
                "Risk Level": risk_level,
            }

            existing_df = read_csv_safe(RISK_FILE, make_default_risk)
            updated_df = pd.concat([existing_df, pd.DataFrame([risk_record])], ignore_index=True)
            updated_df.to_csv(RISK_FILE, index=False)
            st.session_state["risk_records"] = updated_df.to_dict("records")
            st.success("Risk assessment saved successfully!")
        else:
            st.error("Please enter the hazard description and location.")

    st.subheader("Saved Risk Assessments")
    st.dataframe(read_csv_safe(RISK_FILE, make_default_risk), use_container_width=True)

elif page == "Alerts":
    st.header("Mining Alerts")
    st.write("Review worker safety, equipment and maintenance warnings.")

    st.subheader("Equipment Alerts")
    equipment_df = pd.DataFrame(st.session_state.equipment)
    if not equipment_df.empty:
        for _, equipment in equipment_df.iterrows():
            st.write("Equipment:", equipment["Equipment Name"])
            if equipment.get("Temperature", 0) > 100:
                st.error("CRITICAL: Engine temperature is too high.")
            elif equipment.get("Temperature", 0) >= 80:
                st.warning("WARNING: Engine temperature is elevated.")
            if equipment.get("Vibration", 0) > 8:
                st.error("CRITICAL: Vibration is too high.")
            elif equipment.get("Vibration", 0) >= 5:
                st.warning("WARNING: Vibration is elevated.")
            if str(equipment.get("Brakes", "")).lower() == "needs repair":
                st.error("ALERT: Brakes need repair.")
            if str(equipment.get("Tyres", "")).lower() == "needs repair":
                st.warning("ALERT: Tyres need repair.")
            if str(equipment.get("Engine", "")).lower() == "needs repair":
                st.error("ALERT: Engine needs repair.")
            if str(equipment.get("Maintenance Status", "")).lower() == "overdue":
                st.error("ALERT: Equipment maintenance is overdue.")
    else:
        st.info("No equipment reports recorded in this session.")

    st.divider()
    st.subheader("Worker Safety Alerts")
    workers_df = pd.DataFrame(st.session_state.workers)
    if not workers_df.empty:
        for _, worker in workers_df.iterrows():
            st.write("Worker:", worker["Name"])
            if str(worker.get("PPE Compliance", "")).lower() == "non-compliant":
                st.error("ALERT: Worker PPE compliance is inadequate.")
            if str(worker.get("Fatigue Level", "")).lower() == "high":
                st.error("ALERT: Worker fatigue is high.")
            if str(worker.get("Training Status", "")).lower() == "pending":
                st.warning("ALERT: Safety training is pending.")
            if str(worker.get("Risk Level", "")).lower() == "high":
                st.error("HIGH RISK: Review this worker's safety conditions.")
    else:
        st.info("No worker records available.")

    st.divider()
    st.subheader("Safety Incident Alerts")
    incidents_df = read_csv_safe(INCIDENTS_FILE, make_default_incidents)
    if not incidents_df.empty:
        critical_incidents = incidents_df[incidents_df["Severity"].astype(str).str.lower() == "critical"]
        if not critical_incidents.empty:
            st.error(f"CRITICAL ALERT: {len(critical_incidents)} critical incident(s) recorded.")
        open_incidents = incidents_df[incidents_df["Incident Status"].astype(str).str.lower() != "resolved"]
        if not open_incidents.empty:
            st.warning(f"{len(open_incidents)} incident(s) still need attention.")
    else:
        st.success("No safety incidents recorded.")

    st.divider()
    st.subheader("Maintenance Alerts")
    maintenance_df = read_csv_safe(MAINTENANCE_FILE, make_default_maintenance)
    if not maintenance_df.empty:
        if "Availability (%)" in maintenance_df.columns:
            low_availability = maintenance_df[pd.to_numeric(maintenance_df["Availability (%)"], errors="coerce") < 80]
            if not low_availability.empty:
                st.warning(f"AVAILABILITY ALERT: {len(low_availability)} equipment record(s) have availability below 80%.")
        if "Overdue" in maintenance_df.columns:
            overdue = maintenance_df[maintenance_df["Overdue"].astype(str).str.lower().isin(["true", "1", "yes"]) ]
            if not overdue.empty:
                st.error(f"MAINTENANCE ALERT: {len(overdue)} equipment record(s) are overdue.")
        else:
            st.success("No overdue maintenance records found.")

elif page == "Data Analysis":
    st.header("Mining Data Analysis")
    st.write("Review and filter recorded mining data.")

    analysis_type = st.selectbox("Choose data to analyse", ["Worker Safety", "Safety Incidents", "Equipment Monitoring", "Risk Assessments"])

    st.divider()
    st.subheader("Import Many Records from CSV")

    data_category = st.selectbox("Choose the type of data to import", ["Workers", "Safety Incidents", "Equipment", "Maintenance", "Risk Assessments"], key="bulk_import_category")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="bulk_import_file")

    if st.button("Import CSV Data"):
        if uploaded_file is None:
            st.error("Please upload a CSV file first.")
        else:
            file_map = {
                "Workers": WORKERS_FILE,
                "Safety Incidents": INCIDENTS_FILE,
                "Equipment": EQUIPMENT_FILE,
                "Maintenance": MAINTENANCE_FILE,
                "Risk Assessments": RISK_FILE,
            }

            try:
                uploaded_df = pd.read_csv(uploaded_file)
                uploaded_df.columns = uploaded_df.columns.astype(str).str.strip()
                if uploaded_df.empty:
                    st.error("The uploaded file contains no records.")
                elif uploaded_df.columns.duplicated().any():
                    st.error("The CSV contains duplicate column names.")
                else:
                    target_file = file_map[data_category]
                    existing_df = read_csv_safe(target_file, None)
                    combined_df = pd.concat([existing_df, uploaded_df], ignore_index=True, sort=False)
                    combined_df.to_csv(target_file, index=False)

                    if data_category == "Workers":
                        st.session_state.workers = combined_df.to_dict(orient="records")
                    elif data_category == "Equipment":
                        st.session_state.equipment = combined_df.to_dict(orient="records")

                    st.success(f"Imported {len(uploaded_df)} records into {target_file.name}.")
            except Exception as exc:
                st.error(f"Import failed: {exc}")

# End of page routing
