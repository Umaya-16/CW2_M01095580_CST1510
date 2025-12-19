import streamlit as st
import pandas as pd
from app.incidents import get_all_cyber_incidents
from app.db import get_db_connection

# connect to the database
conn = get_db_connection()

# page setup
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# check login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
    st.warning("Please log in to continue")
    st.stop()

# get data
data = get_all_cyber_incidents(conn)
data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

# precompute choices and defaults
severity_choices = list(pd.Series(data["severity"]).dropna().unique())
category_choices = list(pd.Series(data["category"]).dropna().unique())
min_ts = data["timestamp"].dropna().min()
max_ts = data["timestamp"].dropna().max()
default_start = min_ts.date() if pd.notna(min_ts) else pd.Timestamp.today().date()
default_end = max_ts.date() if pd.notna(max_ts) else pd.Timestamp.today().date()

# initialize defaults in session_state once
st.session_state.setdefault("severity", severity_choices[0] if severity_choices else "")
st.session_state.setdefault("category", category_choices[0] if category_choices else "")
st.session_state.setdefault("start_date", default_start)
st.session_state.setdefault("end_date", default_end)

# define a reset function
def reset_filters():
    st.session_state["severity"] = severity_choices[0] if severity_choices else ""
    st.session_state["category"] = category_choices[0] if category_choices else ""
    st.session_state["start_date"] = default_start
    st.session_state["end_date"] = default_end

# sidebar filters
with st.sidebar:
    st.header("Filters")
    st.selectbox("Severity", severity_choices, key="severity")
    st.selectbox("Category", category_choices, key="category")
    st.date_input("Start date", value=st.session_state["start_date"], key="start_date")
    st.date_input("End date", value=st.session_state["end_date"], key="end_date")

    # reset button uses callback
    st.button("Reset Filters", on_click=reset_filters)

    # logout
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.success("You have been logged out.")
        st.rerun()

# ensure valid date range
start_ts = pd.Timestamp(st.session_state["start_date"])
end_ts = pd.Timestamp(st.session_state["end_date"])
if start_ts > end_ts:
    start_ts, end_ts = end_ts, start_ts
    st.session_state["start_date"] = start_ts.date()
    st.session_state["end_date"] = end_ts.date()

# filter data using session_state values
filtered_data = data[
    (data["severity"] == st.session_state["severity"]) &
    (data["category"] == st.session_state["category"]) &
    (data["timestamp"].between(start_ts, end_ts))
]

# personalized welcome
username = st.session_state.get("username", "User")
st.subheader(f"Welcome, {username.capitalize()} 👋")

# handle empty filters
if filtered_data.empty:
    st.warning("No incidents found for this selection.")
else:
    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Incidents", len(filtered_data))
    k2.metric("Unique Categories", filtered_data["category"].nunique())
    k3.metric("Latest Incident ID", filtered_data["incident_id"].max())

    # charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Number of categories")
        st.bar_chart(filtered_data["category"].value_counts())
    with c2:
        st.subheader("Incidents over time")
        st.line_chart(filtered_data.sort_values("timestamp"), x="timestamp", y="incident_id")

    # table
    st.subheader("Filtered incidents data")
    st.dataframe(filtered_data)

    # download button
    csv = filtered_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_incidents.csv",
        mime="text/csv"
    )