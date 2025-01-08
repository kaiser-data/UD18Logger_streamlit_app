import asyncio
import pandas as pd
from bleak import BleakScanner, BleakClient
from datetime import datetime
import os

NOTIFY_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
CSV_FILE = "ble_data_log.csv"
LOG_INTERVAL_SECONDS = 5
last_logged_time = None


def delete_existing_csv():
    """Delete the existing CSV file if it exists."""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        print(f"Deleted existing {CSV_FILE}")


def parse_ud18_packet(packet: bytes):
    if len(packet) == 37:
        packet = packet[:36]
    if len(packet) < 36 or packet[0] != 0xFF or packet[1] != 0x55 or packet[2] != 0x01:
        return None

    volt_raw = int.from_bytes(packet[4:7], byteorder='big')
    amp_raw = int.from_bytes(packet[7:10], byteorder='big')
    mah = int.from_bytes(packet[10:13], byteorder='big')
    wh_raw = int.from_bytes(packet[13:17], byteorder='big')
    dmin_raw = int.from_bytes(packet[17:19], byteorder='big')
    dplus_raw = int.from_bytes(packet[19:21], byteorder='big')

    voltage = volt_raw / 100.0
    current = amp_raw / 100.0
    power = voltage * current
    wh = wh_raw / 100.0
    d_minus = dmin_raw / 100.0
    d_plus = dplus_raw / 100.0

    hour = packet[24]
    minute = packet[25]
    second = packet[26]

    return {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "voltage": voltage,
        "current": current,
        "power": power,
        "capacity_mAh": mah,
        "energy_Wh": wh,
        "d_minus_V": d_minus,
        "d_plus_V": d_plus,
        "runtime": f"{hour:02d}:{minute:02d}:{second:02d}"
    }


def save_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    df = pd.DataFrame([data])
    df.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)
    print(f"Data saved to {CSV_FILE}")


def notification_handler(sender, data: bytearray):
    global last_logged_time
    result = parse_ud18_packet(data)
    if result:
        current_time = datetime.now()
        if last_logged_time is None or (current_time - last_logged_time).total_seconds() >= LOG_INTERVAL_SECONDS:
            save_to_csv(result)
            last_logged_time = current_time
            print(f"Data logged at {result['timestamp']}")
        else:
            print("Skipping data due to interval.")


async def main():
    delete_existing_csv()  # Ensure CSV is deleted before logging starts

    devices = await BleakScanner.discover(timeout=5)
    ud18_device = next((d for d in devices if d.name and "UD18_BLE" in d.name.upper()), None)
    if not ud18_device:
        print("No UD18_BLE device found. Exiting.")
        return

    async with BleakClient(ud18_device) as client:
        if not await client.is_connected():
            print("Failed to connect.")
            return

        await client.start_notify(NOTIFY_CHAR_UUID, notification_handler)
        print("Logging data... Press Ctrl+C to stop.")

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Logging stopped.")
