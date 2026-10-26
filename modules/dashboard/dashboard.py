import pandas as pd
import plotly.express as px
import streamlit as st

from modules.auth.login import load_users, save_users, hash_password
from modules.auth.rbac import get_allowed_tabs
from modules.equipment.equipment_db import compute_availability, availability_status, load_equipment
from modules.safety.risk_assessment import calculate_risk_score, classify_risk, risk_warning_required
from modules.safety.safety_db import load_incidents, load_workers, save_incidents


def render_dashboard() -> None:
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

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Workers Registered", len(workers_df))
        with col2:
            st.metric("Incidents Logged", len(incidents_df))
        with col3:
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
        csv_bytes = report_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {report_type} CSV",
            data=csv_bytes,
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
