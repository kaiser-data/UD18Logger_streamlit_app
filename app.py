import streamlit as st
import pandas as pd
import subprocess
import os
import time
import plotly.express as px

CSV_FILE = "ble_data_log.csv"
LOGGING_PROCESS = None  # Process handler for background logging

st.title("UD18 BLE Data Logger")

# Initialize logging state
if "logging" not in st.session_state:
    st.session_state["logging"] = False


def start_logging():
    global LOGGING_PROCESS
    if not st.session_state["logging"]:
        LOGGING_PROCESS = subprocess.Popen(["python", "ud18Logger.py"])
        st.session_state["logging"] = True
        st.success("Data logging started.")
    else:
        if LOGGING_PROCESS:
            LOGGING_PROCESS.terminate()
            LOGGING_PROCESS = None
        st.session_state["logging"] = False
        st.warning("Data logging stopped.")


# Create tabs for control panel and raw data
tab1, tab2 = st.tabs(["Control Panel & Visualizations", "Raw Data Table"])

# ---- Tab 1: Control Panel and Plots ----
with tab1:
    st.header("Control Panel and Real-Time Plots")

    # Start/Stop Button
    button_text = "Stop Logging" if st.session_state["logging"] else "Start Logging"
    st.button(button_text, on_click=start_logging)

    st.info("Use this tab to start or stop data logging and visualize data in real-time.")

    # Metric placeholders for real-time data in 4 columns
    col1, col2, col3, col4 = st.columns(4)

    # Voltage (V) Metric
    with col1:
        voltage_box = st.metric(label="Voltage (V)", value="--")
        voltage_plot = st.empty()

    # Current (A) Metric
    with col2:
        current_box = st.metric(label="Current (A)", value="--")
        current_plot = st.empty()

    # Power (W) Metric
    with col3:
        power_box = st.metric(label="Power (W)", value="--")
        power_plot = st.empty()

    # D+ and D- Voltage Metrics
    with col4:
        dplus_box = st.metric(label="D+ Voltage (V)", value="--")
        dminus_box = st.metric(label="D- Voltage (V)", value="--")
        dplus_dminus_plot = st.empty()

# ---- Tab 2: Raw Data Table ----
with tab2:
    st.header("Raw Data Table")
    data_table = st.empty()


# Helper function to load data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()


# Continuous Polling Loop for Real-Time Updates
while st.session_state["logging"]:
    df = load_data()

    if not df.empty:
        # Calculate elapsed time in seconds
        df['elapsed_seconds'] = (
                    pd.to_datetime(df['timestamp']) - pd.to_datetime(df['timestamp'].iloc[0])).dt.total_seconds()

        # Get the latest row of data for metrics
        latest_data = df.iloc[-1]

        # Update metric boxes with real-time data
        voltage_box.metric(label="Voltage (V)", value=f"{latest_data['voltage']:.2f}")
        current_box.metric(label="Current (A)", value=f"{latest_data['current']:.2f}")
        power_box.metric(label="Power (W)", value=f"{latest_data['power']:.2f}")
        dplus_box.metric(label="D+ Voltage (V)", value=f"{latest_data['d_plus_V']:.2f}")
        dminus_box.metric(label="D- Voltage (V)", value=f"{latest_data['d_minus_V']:.2f}")

        # Power (Watt) over Time
        fig_power = px.line(df, x='elapsed_seconds', y='power', title='Power (Watt) over Time',
                            color_discrete_sequence=["#EF553B"])
        fig_power.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Power (W)")

        # Voltage over Time
        fig_voltage = px.line(df, x='elapsed_seconds', y='voltage', title='Voltage over Time',
                              color_discrete_sequence=["#636EFA"])
        fig_voltage.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Voltage (V)")

        # Current (Ampere) over Time
        fig_current = px.line(df, x='elapsed_seconds', y='current', title='Current (Ampere) over Time',
                              color_discrete_sequence=["#00CC96"])
        fig_current.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Current (A)")

        # D+ and D- over Time (Dual Line Plot)
        fig_dplus_dminus = px.line(df, x='elapsed_seconds', y=['d_plus_V', 'd_minus_V'],
                                   title='D+ and D- Voltage over Time',
                                   color_discrete_sequence=["#FFA15A", "#AB63FA"])
        fig_dplus_dminus.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Voltage (V)")

        # Update Plots
        voltage_plot.plotly_chart(fig_voltage)
        current_plot.plotly_chart(fig_current)
        power_plot.plotly_chart(fig_power)
        dplus_dminus_plot.plotly_chart(fig_dplus_dminus)

        # Update Data Table in Tab 2
        with data_table.container():
            st.dataframe(df)

    time.sleep(2)  # Poll every 2 seconds to keep it responsive
