import hashlib
import pathlib

import pandas as pd
import streamlit as st

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
USERS_PATH = DATA_DIR / "users.csv"


def hash_password(password: str) -> str:
    """Return SHA-256 digest for a password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def default_users_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"username": "admin", "password": hash_password("admin123"), "role": "Administrator", "status": "Active"},
            {"username": "safety1", "password": hash_password("safety123"), "role": "Safety Officer", "status": "Active"},
            {"username": "eng1", "password": hash_password("eng123"), "role": "Mining Engineer", "status": "Active"},
        ]
    )


def ensure_users_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_PATH.exists():
        default_users_df().to_csv(USERS_PATH, index=False)
        return

    try:
        df = pd.read_csv(USERS_PATH)
        required_columns = {"username", "password", "role", "status"}
        if set(df.columns).issuperset(required_columns):
            return
    except Exception:
        pass

    default_users_df().to_csv(USERS_PATH, index=False)


def load_users() -> pd.DataFrame:
    ensure_users_file()
    return pd.read_csv(USERS_PATH)


def save_users(users_df: pd.DataFrame) -> None:
    ensure_users_file()
    users_df.to_csv(USERS_PATH, index=False)


def login_page() -> None:
    ensure_users_file()
    st.title("⛏️ Khwezi Mining Health, Safety & Equipment System")
    st.write("Wits MINN2020A Project - Access Control & Security Prototype")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        users_db = load_users()
        match = users_db[users_db["username"].astype(str).str.lower() == username.strip().lower()]

        if match.empty:
            st.error("Invalid username or password.")
            return

        stored_hash = match.iloc[0]["password"]
        if hash_password(password) == stored_hash:
            st.session_state.logged_in = True
            st.session_state.username = match.iloc[0]["username"]
            st.session_state.role = match.iloc[0]["role"]
            st.success(f"Welcome, {st.session_state.username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
