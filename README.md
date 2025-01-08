# UD18 BLE Data Logger and Visualization  

This project is a real-time data logger and visualizer for UD18 BLE devices. The app collects voltage, current, power, and D+/D- measurements using BLE, saves the data to a CSV file, and displays live metrics and dynamic plots using Streamlit and Plotly.  

## Features  
- **Real-time BLE Data Logging** – Collect data from UD18 BLE devices every few seconds.  
- **Live Visualization** – Display dynamic Plotly graphs of power, voltage, current, and D+/D- values.  
- **Dual Data View** – Visualize data in real-time with plots and access the raw data in table form.  
- **Interactive UI** – Start/stop logging directly from the Streamlit app.  
- **Instant Metrics** – Real-time display of Voltage, Current, Power, and D+/- values in metric boxes.  

## How It Works  
- A Python script (`ud18Logger.py`) uses bleak to continuously log BLE data and save it to `ble_data_log.csv`.  
- The Streamlit app (`app.py`) visualizes this data in real time with dynamic plots and displays key metrics.  
- Key metrics such as Voltage, Current, Power, and D+/D- are displayed in metric boxes and updated every 2 seconds.  

## Project Structure  
📁 UD18-BLE-Logger/
│
├── app.py              # Streamlit app for visualization and control
├── ud18Logger.py       # BLE data logger script
├── ble_data_log.csv    # CSV file storing logged data (auto-generated)
├── README.md           # Project documentation
└── requirements.txt    # Required Python dependencies
└── requirements.txt # Required Python dependencies

## Requirements  
To run this project, you'll need **Python 3.8 or higher**.  

### Install Dependencies  
Use the following command to install required packages:  

pip install -r requirements.txt


## How to Run  
### Start the Logger:  
python ud18Logger.py

This script will continuously log data from the UD18 BLE device.  

### Run the Streamlit App:  
streamlit run app.py

Access the app at [http://localhost:8501](http://localhost:8501) to start/stop logging and view live visualizations.  

## Live Data Visualization  
- **Tab 1**: Control panel with live plots of:  
  - Voltage (V)  
  - Current (A)  
  - Power (W)  
  - D+ and D- voltages (combined in one plot)  
- **Tab 2**: Raw data table showing all logged entries from the CSV.  

## Dependencies  
**Key Libraries:**  
- **Streamlit** – Interactive web-based UI for Python apps.  
- **Plotly** – Real-time plotting and data visualization.  
- **Bleak** – BLE communication for data collection.  
- **Pandas** – Data manipulation and CSV handling.  

## BLE Device Requirements  
Ensure your system supports **BLE (Bluetooth Low Energy)**. This project uses the `bleak` library to interact with UD18 BLE devices.  

## Notes  
- Data is automatically saved to `ble_data_log.csv` during logging.  
- The CSV is deleted and recreated at the start of each logging session to prevent old data accumulation.  
- Adjust the logging interval by modifying `LOG_INTERVAL_SECONDS` in `ud18Logger.py`.  

## Future Enhancements  
- **Threshold Alerts** – Visual or email alerts if voltage/current exceeds defined thresholds.  
- **Historical Data** – Allow users to load and analyze past CSV files.  
- **Multi-Device Support** – Expand support to log from multiple UD18 devices sim

