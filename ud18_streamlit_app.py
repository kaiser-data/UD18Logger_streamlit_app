import streamlit as st
import pandas as pd
import subprocess
import os
import time
import plotly.express as px

CSV_FILE = "ble_data_log.csv"
LOGGING_PROCESS = None  # Process handler for background logging

st.set_page_config(layout="wide")  # Set layout to wide
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
        voltage_html = st.empty()
        voltage_plot = st.empty()

    # Current (A) Metric
    with col2:
        current_html = st.empty()
        current_plot = st.empty()

    # Power (W) Metric
    with col3:
        power_html = st.empty()
        power_plot = st.empty()

    # D+ and D- Voltage Metrics
    with col4:
        # Display D+ and D- side by side
        dplus_dminus_html = st.empty()
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
try:
    while st.session_state["logging"]:
        df = load_data()

        if not df.empty:
            # Handle timestamp parsing with automatic inference
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df.dropna(subset=['timestamp'], inplace=True)  # Remove invalid timestamps
            except Exception as e:
                st.error(f"Error parsing timestamps: {e}")
                break

            # Calculate elapsed time in seconds
            df['elapsed_seconds'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

            # Get the latest row of data for metrics
            latest_data = df.iloc[-1]

            # HTML Styling for Metrics
            voltage_color = "#636EFA"  # Voltage color
            current_color = "#00CC96"  # Current color
            power_color = "#EF553B"  # Power color
            dplus_color = "#FFA15A"  # D+ Voltage color
            dminus_color = "#AB63FA"  # D- Voltage color

            voltage_html.markdown(
                f"<h4 style='color:{voltage_color};'>Voltage (V)</h4>"
                f"<h2 style='color:{voltage_color};'>{latest_data['voltage']:.2f}</h2>",
                unsafe_allow_html=True,
            )
            current_html.markdown(
                f"<h4 style='color:{current_color};'>Current (A)</h4>"
                f"<h2 style='color:{current_color};'>{latest_data['current']:.2f}</h2>",
                unsafe_allow_html=True,
            )
            power_html.markdown(
                f"<h4 style='color:{power_color};'>Power (W)</h4>"
                f"<h2 style='color:{power_color};'>{latest_data['power']:.2f}</h2>",
                unsafe_allow_html=True,
            )

            # D+ and D- Metrics Side-by-Side
            dplus_dminus_html.markdown(
                f"""
                <div style='display: flex; justify-content: space-between;'>
                    <div>
                        <h4 style='color:{dplus_color};'>D+ Voltage (V)</h4>
                        <h2 style='color:{dplus_color};'>{latest_data['d_plus_V']:.2f}</h2>
                    </div>
                    <div>
                        <h4 style='color:{dminus_color};'>D- Voltage (V)</h4>
                        <h2 style='color:{dminus_color};'>{latest_data['d_minus_V']:.2f}</h2>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Power (Watt) over Time
            fig_power = px.line(df, x='elapsed_seconds', y='power', title='Power (Watt) over Time',
                                color_discrete_sequence=[power_color])
            fig_power.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Power (W)")

            # Voltage over Time
            fig_voltage = px.line(df, x='elapsed_seconds', y='voltage', title='Voltage over Time',
                                  color_discrete_sequence=[voltage_color])
            fig_voltage.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Voltage (V)")

            # Current (Ampere) over Time
            fig_current = px.line(df, x='elapsed_seconds', y='current', title='Current (Ampere) over Time',
                                  color_discrete_sequence=[current_color])
            fig_current.update_layout(xaxis_title="Time (Seconds)", yaxis_title="Current (A)")

            # D+ and D- over Time (Dual Line Plot)
            fig_dplus_dminus = px.line(df, x='elapsed_seconds', y=['d_plus_V', 'd_minus_V'],
                                       title='D+ and D- Voltage over Time',
                                       labels={"value": "Voltage (V)", "variable": "Signal"},
                                       color_discrete_sequence=[dplus_color, dminus_color])
            fig_dplus_dminus.update_layout(
                xaxis_title="Time (Seconds)",
                yaxis_title="Voltage (V)",
                showlegend=False  # Remove legend
            )

            # Update Plots
            voltage_plot.plotly_chart(fig_voltage, use_container_width=True)
            current_plot.plotly_chart(fig_current, use_container_width=True)
            power_plot.plotly_chart(fig_power, use_container_width=True)
            dplus_dminus_plot.plotly_chart(fig_dplus_dminus, use_container_width=True)

            # Update Data Table in Tab 2
            with data_table.container():
                st.dataframe(df)

        time.sleep(2)  # Poll every 2 seconds to keep it responsive
except Exception as e:
    st.error(f"An error occurred: {e}")
