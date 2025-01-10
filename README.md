# UD18 BLE Data Logger and Visualization

This project provides a **real-time data logger and visualizer** for UD18 BLE devices. Using Python, BLE communication, and Streamlit, the app logs voltage, current, power, and D+/D- values, stores the data in a CSV file, and visualizes live metrics with interactive plots.

![Device Photo](path/to/device_photo.jpg)  
*Figure 1: UD18 BLE Device*

## Features

- **Real-Time BLE Data Logging**  
  Collects data from UD18 BLE devices every few seconds.

- **Dynamic Visualizations**  
  Interactive Plotly graphs for power, voltage, current, and D+/D- measurements.

- **Dual Data View**  
  Simultaneously visualize data with dynamic plots and access raw data in a table format.

- **User-Friendly Control Panel**  
  Start or stop logging with a single click in the app interface.

- **Instant Metrics**  
  Displays real-time Voltage, Current, Power, and D+/D- values in intuitive metric boxes.

## How It Works

1. **Data Logging**  
   - The `ud18Logger.py` script uses the `bleak` library to collect data from the UD18 BLE device.  
   - Logs are saved in real-time to `ble_data_log.csv`.

2. **Live Visualization**  
   - The Streamlit app (`app.py`) reads the data, updates key metrics, and renders live visualizations.

3. **User Interaction**  
   - Users can control logging, view metrics, and switch between plots and the raw data table.

![App Screenshot](path/to/screenshot.jpg)  
*Figure 2: Streamlit App Interface*

## Project Structure

📁 UD18-BLE-Logger/  
│  
├── app.py              - Streamlit app for visualization and control  
├── ud18Logger.py       - BLE data logger script  
├── ble_data_log.csv    - CSV file storing logged data (auto-generated)  
├── README.md           - Project documentation  
└── requirements.txt    - Python dependencies  

## Installation

### Prerequisites

- **Python 3.8 or higher**  
- **BLE-compatible system** (Bluetooth Low Energy support is required).

### Install Dependencies

Run the following command:  
pip install -r requirements.txt

## How to Run

### Start the Logger

To start logging data, run:  
python ud18Logger.py

### Run the Visualization App

Launch the Streamlit app using:  
streamlit run app.py

Open the app in your browser at http://localhost:8501.

## Live Data Visualization

### Tab 1: Control Panel and Visualizations

- Real-time plots for:  
  - **Voltage (V)**  
  - **Current (A)**  
  - **Power (W)**  
  - **D+ and D- Voltages** (dual-line plot).

### Tab 2: Raw Data Table

- Displays logged data in a tabular format directly from `ble_data_log.csv`.

## Key Libraries

- **Streamlit** - Web-based interface for Python apps.  
- **Plotly** - Interactive plotting and visualizations.  
- **Bleak** - Bluetooth Low Energy communication.  
- **Pandas** - Data manipulation and CSV handling.

## Notes

- Data is saved to `ble_data_log.csv` automatically during logging.  
- The CSV is cleared at the start of each logging session to prevent data overflow.  
- Modify logging intervals by editing `LOG_INTERVAL_SECONDS` in `ud18Logger.py`.

## Future Enhancements

- **Alert System**: Notify users when metrics exceed thresholds.  
- **Historical Data Analysis**: Load and visualize past CSV files.  
- **Multi-Device Support**: Log data from multiple UD18 devices simultaneously.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For questions or support, please contact:  
**Martin Kaiser**  
martinkaiser.bln@gmail.com
