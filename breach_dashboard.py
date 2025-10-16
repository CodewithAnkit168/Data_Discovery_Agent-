import streamlit as st
import pandas as pd

st.set_page_config(page_title="Breach Detection Agent – India", layout="wide")

st.title("Breach Detection Dashboard (India PII)")

# Load datasets
df_logs = pd.read_csv('pii_access_logs_india.csv')
df_incidents = pd.read_csv('breach_incidents_india.csv')

st.sidebar.header("Filters & Search")

# Filter by anomaly type
anomaly_types = df_incidents['anomaly'].dropna().unique().tolist()
selected_anomaly = st.sidebar.multiselect('Anomaly Type:', anomaly_types, default=anomaly_types)

# Filter by data type
data_types = df_incidents['data_type'].unique().tolist()
selected_data_type = st.sidebar.multiselect('Data Type:', data_types, default=data_types)

# Filter by user/email
user_query = st.sidebar.text_input("Search by Name/Email:")

filtered = df_incidents[
    df_incidents['anomaly'].isin(selected_anomaly) &
    df_incidents['data_type'].isin(selected_data_type)
]

if user_query:
    filtered = filtered[
        filtered['name'].str.contains(user_query, case=False) |
        filtered['email'].str.contains(user_query, case=False)
    ]

st.subheader("Incident Tickets (Detected Breaches/Alerts)")
st.dataframe(filtered, use_container_width=True)

# Download filtered tickets
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download Incident Report CSV", csv, "filtered_breach_incidents.csv", "text/csv")

# Visual summary
st.subheader("Incident Type Distribution")
chart_data = filtered['anomaly'].value_counts()
st.bar_chart(chart_data)

st.subheader("Recently Flagged Incidents")
for idx, row in filtered.head(5).iterrows():
    st.warning(
        f"🛑 {row['anomaly']}: {row['name']} ({row['email']}), Action: {row['action']}, "
        f"Data: {row['data_type']}, Records: {row['records_accessed']}, Time: {row['timestamp']}"
    )

st.markdown("---")
st.caption("Automated Breach Detection Agent • DPDPA Compliance • MIT License ©2025")
