import hashlib
import pathlib

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================
# App config
# ============================
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_PATH = DATA_DIR / "users.csv"
WORKERS_PATH = DATA_DIR / "workers.csv"
INCIDENTS_PATH = DATA_DIR / "incidents.csv"
EQUIPMENT_PATH = DATA_DIR / "equipment.csv"

# ============================
# Helper functions
# ============================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def default_users_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"username": "admin", "password": hash_password("admin123"), "role": "Administrator", "status": "Active"},
            {"username": "safety1", "password": hash_password("safety123"), "role": "Safety Officer", "status": "Active"},
            {"username": "eng1", "password": hash_password("eng123"), "role": "Mining Engineer", "status": "Active"},
        ]
    )


def default_workers_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"worker_id": "KWM-001", "full_name": "Thabo Dlamini", "department": "Production", "role": "Drill Operator", "induction_status": "Passed", "medical_clearance": "Fit"},
            {"worker_id": "KWM-002", "full_name": "Aphiwe Nkosi", "department": "Maintenance", "role": "Technician", "induction_status": "Passed", "medical_clearance": "Fit"},
            {"worker_id": "KWM-003", "full_name": "Lerato Moloi", "department": "Safety", "role": "Safety Auditor", "induction_status": "Passed", "medical_clearance": "Fit"},
        ]
    )


def default_incidents_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"incident_id": "INC-001", "date_logged": "2026-08-15 08:30:00", "classification": "Equipment Scrape", "likelihood": 2, "consequence": 3, "risk_rating": "Medium", "logged_by": "safety1", "status": "Resolved"},
            {"incident_id": "INC-002", "date_logged": "2026-08-17 10:45:00", "classification": "Unsafe Behaviour", "likelihood": 3, "consequence": 4, "risk_rating": "High", "logged_by": "safety1", "status": "Investigating"},
            {"incident_id": "INC-003", "date_logged": "2026-08-19 14:20:00", "classification": "Ventilation Concern", "likelihood": 4, "consequence": 5, "risk_rating": "Critical", "logged_by": "safety1", "status": "Open"},
        ]
    )


def default_equipment_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"asset_id": "EQP-01", "category": "LHD Loader", "assigned_location": "Level 3 - North Block", "status": "Operational", "operating_time": 1420, "downtime": 200, "temperature_c": 46, "vibration_mm_s": 6.4},
            {"asset_id": "EQP-02", "category": "Truck", "assigned_location": "Level 2 - East Pit", "status": "Under Maintenance", "operating_time": 2890, "downtime": 1100, "temperature_c": 62, "vibration_mm_s": 8.9},
            {"asset_id": "EQP-03", "category": "Drill Rig", "assigned_location": "Level 1 - South Shaft", "status": "Operational", "operating_time": 1760, "downtime": 340, "temperature_c": 49, "vibration_mm_s": 7.2},
        ]
    )


def ensure_data_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_PATH.exists():
        default_users_df().to_csv(USERS_PATH, index=False)

    if not WORKERS_PATH.exists():
        default_workers_df().to_csv(WORKERS_PATH, index=False)

    if not INCIDENTS_PATH.exists():
        default_incidents_df().to_csv(INCIDENTS_PATH, index=False)

    if not EQUIPMENT_PATH.exists():
        default_equipment_df().to_csv(EQUIPMENT_PATH, index=False)


def load_users() -> pd.DataFrame:
    ensure_data_files()
    try:
        df = pd.read_csv(USERS_PATH)
        if {"username", "password", "role", "status"}.issubset(df.columns):
            return df
    except Exception:
        pass

    default_users_df().to_csv(USERS_PATH, index=False)
    return default_users_df()


def save_users(df: pd.DataFrame):
    df.to_csv(USERS_PATH, index=False)


def load_workers() -> pd.DataFrame:
    ensure_data_files()
    try:
        return pd.read_csv(WORKERS_PATH)
    except Exception:
        default_workers_df().to_csv(WORKERS_PATH, index=False)
        return default_workers_df()


def load_incidents() -> pd.DataFrame:
    ensure_data_files()
    try:
        return pd.read_csv(INCIDENTS_PATH)
    except Exception:
        default_incidents_df().to_csv(INCIDENTS_PATH, index=False)
        return default_incidents_df()


def load_equipment() -> pd.DataFrame:
    ensure_data_files()
    try:
        return pd.read_csv(EQUIPMENT_PATH)
    except Exception:
        default_equipment_df().to_csv(EQUIPMENT_PATH, index=False)
        return default_equipment_df()


def save_incidents(df: pd.DataFrame):
    df.to_csv(INCIDENTS_PATH, index=False)


def calculate_risk_score(likelihood, consequence):
    return float(likelihood) * float(consequence)


def classify_risk(score):
    if 1 <= score <= 4:
        return "Low"
    if 5 <= score <= 9:
        return "Medium"
    if 10 <= score <= 16:
        return "High"
    if 17 <= score <= 25:
        return "Critical"
    return "Low"


def risk_warning_required(score):
    return score >= 10


def compute_availability(operating_time, downtime):
    total = operating_time + downtime
    if total <= 0:
        return 0.0
    return (operating_time / total) * 100


def availability_status(availability, threshold=85.0):
    if availability < threshold:
        return "Low Availability"
    return "Available"


def get_allowed_tabs(role):
    role_map = {
        "Administrator": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Equipment Data",
            "Maintenance Data",
            "Generate Reports",
            "Manage Users Console",
        ],
        "Safety Officer": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Generate Reports",
        ],
        "Mining Engineer": [
            "View Dashboard",
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment",
            "Equipment Data",
            "Maintenance Data",
            "Generate Reports",
        ],
    }
    return role_map.get(role, ["View Dashboard"])


# ============================
# Login and signup UI
# ============================
def login_page():
    ensure_data_files()

    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f3f4f6;
            color: #1f2937;
        }

        .big-title {
            font-size: 4.2rem;
            font-weight: 800;
            line-height: 1.0;
            color: #1f2937;
            margin-top: 18px;
            margin-bottom: 8px;
        }

        .subtext {
            color: #4a90e2;
            font-size: 1.8rem;
            font-weight: 500;
            margin-bottom: 26px;
        }

        .auth-toggle {
            background: #0f172a;
            border-radius: 999px;
            padding: 6px 8px;
            width: fit-content;
            margin-bottom: 22px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        }

        .panel {
            background: #eef1f4;
            color: #1f2937;
            border-radius: 12px;
            padding: 18px 18px 22px 18px;
            border: 1px solid #cfd8e3;
            box-shadow: none;
            max-width: 100%;
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input {
            background: #f8fafc;
            color: #111827;
            border: 1px solid #cfd8e3;
            border-radius: 10px;
            min-height: 52px;
            font-size: 1.05rem;
        }

        label {
            color: #1f2937 !important;
            font-weight: 600;
            font-size: 1.0rem;
        }

        .stButton > button {
            background: #dfe7ee;
            color: #1f2937;
            border-radius: 10px;
            border: 1px solid #d0d7df;
            font-weight: 700;
            min-height: 48px;
            width: 120px;
            float: right;
        }

        .stButton > button:hover {
            background: #d4dde6;
            border-color: #c1ccd7;
        }

        .stRadio > div {
            background: #0f172a;
            border-radius: 999px;
            padding: 5px 8px;
            width: fit-content;
            border: 1px solid #0f172a;
        }

        .stRadio label {
            color: white !important;
            font-weight: 600;
        }

        .stRadio [data-baseweb="radio"] {
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="big-title">Login</div>', unsafe_allow_html=True)

    st.markdown('<div class="auth-toggle">', unsafe_allow_html=True)
    auth_mode = st.radio("", ["Login", "Sign Up"], horizontal=True, index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    if auth_mode == "Login":
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("", anchor=False)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            users_db = load_users()
            match = users_db[users_db["username"].astype(str).str.lower() == username.strip().lower()]

            if match.empty:
                st.error("Invalid username or password.")
            else:
                stored_hash = match.iloc[0]["password"]
                if hash_password(password) == stored_hash:
                    st.session_state.logged_in = True
                    st.session_state.username = match.iloc[0]["username"]
                    st.session_state.role = match.iloc[0]["role"]
                    st.success(f"Welcome, {st.session_state.username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Create Account")

        with st.form("signup_form", clear_on_submit=True):
            new_username = st.text_input("New Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_role = st.selectbox("Role", ["Administrator", "Safety Officer", "Mining Engineer"])
            signup_submit = st.form_submit_button("Sign Up", use_container_width=True)

        if signup_submit:
            if not new_username.strip():
                st.warning("Please enter a username.")
            elif new_password != confirm_password:
                st.warning("Passwords do not match.")
            else:
                users_db = load_users()
                if new_username.strip().lower() in users_db["username"].astype(str).str.lower().values:
                    st.warning("This username already exists.")
                else:
                    new_row = {
                        "username": new_username.strip(),
                        "password": hash_password(new_password),
                        "role": new_role,
                        "status": "Active",
                    }
                    users_db = pd.concat([users_db, pd.DataFrame([new_row])], ignore_index=True)
                    save_users(users_db)
                    st.success(f"Account created for {new_username.strip()}! You can now log in.")
                    st.balloons()

        st.markdown("</div>", unsafe_allow_html=True)


# ============================
# Dashboard
# ============================
def render_dashboard():
    st.title("📈 Main Monitoring Dashboard")
    st.write("Khwezi Mining Health, Safety & Equipment Monitoring")

    st.sidebar.header("🛡️ Current User Session")
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    st.sidebar.write(f"Role: **{st.session_state.role}**")

    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    allowed_tabs = get_allowed_tabs(st.session_state.role)
    st.sidebar.subheader("Navigation Menu")
    selected_tab = st.sidebar.radio("Authorized Modules:", allowed_tabs)

    if selected_tab == "View Dashboard":
        workers_df = load_workers()
        incidents_df = load_incidents()
        equipment_df = load_equipment()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Workers Registered", len(workers_df))
        with c2:
            st.metric("Incidents Logged", len(incidents_df))
        with c3:
            st.metric("Assets Monitored", len(equipment_df))

        st.markdown("---")
        st.subheader("Operational Overview")

        incident_status = incidents_df["status"].value_counts()
        st.bar_chart(incident_status)

        dept_counts = workers_df["department"].value_counts()
        st.bar_chart(dept_counts)

    elif selected_tab == "Worker Safety Data":
        workers_df = load_workers()
        st.header("👷 Worker Safety Data")
        st.dataframe(workers_df, use_container_width=True)

    elif selected_tab == "Safety Incidents":
        incidents_df = load_incidents()
        st.header("🚨 Safety Incidents")

        with st.form("new_incident_form"):
            incident_id = st.text_input("Incident ID")
            date_logged = st.date_input("Date Logged")
            classification = st.text_input("Classification")
            likelihood = st.number_input("Likelihood (1–5)", min_value=1, max_value=5, value=3)
            consequence = st.number_input("Consequence (1–5)", min_value=1, max_value=5, value=3)
            logged_by = st.text_input("Logged By")
            status = st.selectbox("Status", ["Open", "Investigating", "Resolved"])
            submitted = st.form_submit_button("Save Incident")

        if submitted:
            score = calculate_risk_score(likelihood, consequence)
            new_row = {
                "incident_id": incident_id,
                "date_logged": str(date_logged),
                "classification": classification,
                "likelihood": float(likelihood),
                "consequence": float(consequence),
                "risk_rating": classify_risk(score),
                "logged_by": logged_by,
                "status": status,
            }
            incidents_df = pd.concat([incidents_df, pd.DataFrame([new_row])], ignore_index=True)
            save_incidents(incidents_df)
            st.success(f"Incident {incident_id} added successfully.")
            st.rerun()

        st.dataframe(incidents_df, use_container_width=True)

    elif selected_tab == "Risk Assessment":
        incidents_df = load_incidents()
        st.header("⚠️ Risk Assessment")

        if incidents_df.empty:
            st.info("No incident data available.")
        else:
            risk_rows = []
            for _, row in incidents_df.iterrows():
                score = calculate_risk_score(row.get("likelihood", 0), row.get("consequence", 0))
                risk_rows.append(
                    {
                        "incident_id": row["incident_id"],
                        "classification": row["classification"],
                        "likelihood": row.get("likelihood", 0),
                        "consequence": row.get("consequence", 0),
                        "risk_score": score,
                        "risk_category": classify_risk(score),
                        "warning_required": risk_warning_required(score),
                    }
                )

            risk_df = pd.DataFrame(risk_rows)
            st.dataframe(risk_df, use_container_width=True)

            fig = px.bar(
                risk_df,
                x="incident_id",
                y="risk_score",
                color="risk_category",
                title="Risk score by incident",
            )
            st.plotly_chart(fig, use_container_width=True)

    elif selected_tab == "Equipment Data":
        equipment_df = load_equipment()
        st.header("🛠️ Equipment Data")

        equipment_df["availability_percent"] = equipment_df.apply(
            lambda row: compute_availability(row["operating_time"], row["downtime"]),
            axis=1,
        )
        equipment_df["availability_status"] = equipment_df["availability_percent"].apply(availability_status)

        st.dataframe(equipment_df, use_container_width=True)

        fig = px.bar(
            equipment_df,
            x="asset_id",
            y="availability_percent",
            color="availability_status",
            title="Equipment Availability %",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_tab == "Maintenance Data":
        equipment_df = load_equipment()
        st.header("🔧 Maintenance Data")

        equipment_df["availability_percent"] = equipment_df.apply(
            lambda row: compute_availability(row["operating_time"], row["downtime"]),
            axis=1,
        )
        equipment_df["maintenance_priority"] = equipment_df["availability_percent"].apply(
            lambda value: "High Priority" if value < 85 else "Standard"
        )

        st.dataframe(equipment_df, use_container_width=True)

    elif selected_tab == "Generate Reports":
        st.header("📄 Generate Reports")
        report_type = st.selectbox("Select report type", ["Worker Summary", "Incident Summary", "Equipment Summary"])

        if report_type == "Worker Summary":
            report_df = load_workers()
        elif report_type == "Incident Summary":
            report_df = load_incidents()
        else:
            report_df = load_equipment()

        st.dataframe(report_df, use_container_width=True)
        csv_data = report_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {report_type} CSV",
            data=csv_data,
            file_name=f"{report_type.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

    elif selected_tab == "Manage Users Console":
        st.header("🧑‍💼 Manage Users Console")
        users_df = load_users()
        st.dataframe(users_df, use_container_width=True)

        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["Administrator", "Safety Officer", "Mining Engineer"])
            submitted = st.form_submit_button("Add User")

        if submitted and new_username.strip():
            if new_username in users_df["username"].astype(str).values:
                st.warning("Username already exists.")
            else:
                new_row = {
                    "username": new_username,
                    "password": hash_password(new_password),
                    "role": new_role,
                    "status": "Active",
                }
                users_df = pd.concat([users_df, pd.DataFrame([new_row])], ignore_index=True)
                save_users(users_df)
                st.success(f"User '{new_username}' added successfully.")
                st.rerun()


# ============================
# App startup
# ============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    login_page()
else:
    render_dashboard()


# Default logins:
# admin / admin123
# safety1 / safety123
# eng1 / eng123
