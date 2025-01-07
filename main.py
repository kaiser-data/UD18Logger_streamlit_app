#!/usr/bin/env python3
import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

NOTIFY_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
WRITE_CHAR_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"


def parse_ud18_packet(packet: bytes):
    # Handle 37-byte packets by ignoring the last byte
    if len(packet) == 37:
        packet = packet[:36]
    if len(packet) < 36:
        return None

    if packet[0] != 0xFF or packet[1] != 0x55:
        return None
    if packet[2] != 0x01:
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
        "voltage": voltage,
        "current": current,
        "power": power,
        "capacity_mAh": mah,
        "energy_Wh": wh,
        "d_minus_V": d_minus,
        "d_plus_V": d_plus,
        "runtime": f"{hour:02d}:{minute:02d}:{second:02d}",
    }


def notification_handler(sender, data: bytearray):
    print(f"\n[Notify] Characteristic {sender}:")
    print(f"Raw bytes: {data.hex()}")

    result = parse_ud18_packet(data)
    if result:
        print("UD18 Parse Result:")
        print(f"  Voltage  : {result['voltage']} V")
        print(f"  Current  : {result['current']} A")
        print(f"  Power    : {result['power']} W")
        print(f"  Capacity : {result['capacity_mAh']} mAh")
        print(f"  Energy   : {result['energy_Wh']} Wh")
        print(f"  USB D-   : {result['d_minus_V']} V")
        print(f"  USB D+   : {result['d_plus_V']} V")
        print(f"  Runtime  : {result['runtime']}")
    else:
        print("Packet doesn't match the expected UD18 format.")


async def main():
    print("Scanning 5s for 'UD18_BLE' name...")
    devices = await BleakScanner.discover(timeout=5)

    ud18_device = None
    for d in devices:
        if d.name and "UD18_BLE" in d.name.upper():
            ud18_device = d
            break

    if not ud18_device:
        print("No UD18_BLE device found. Exiting.")
        return

    print(f"Found {ud18_device.name} at {ud18_device.address}, attempting to connect...")
    async with BleakClient(ud18_device) as client:
        # Bleak 0.19+ changes is_connected to a property
        # so we can do either: if not client.is_connected:
        # or ignore it if it successfully opened the context manager
        if not await client.is_connected():
            print("Connection failed.")
            return
        print(f"Connected to {ud18_device.name} ({ud18_device.address})")

        # List services & characteristics
        # (Warning about "future version" is normal in Bleak 0.19)
        services = await client.get_services()
        print("\n== Listing Services & Characteristics ==")
        for svc in services:
            print(f"Service: {svc.uuid} - {svc.description}")
            for char in svc.characteristics:
                print(f"  Characteristic: {char.uuid} - {char.properties}")

        # Possibly send an init/start command if your meter needs it
        # start_cmd = b"\xFF\x55\x01\x00"
        # await client.write_gatt_char(WRITE_CHAR_UUID, start_cmd)

        print(f"\nSubscribing to notifications on {NOTIFY_CHAR_UUID}...")
        try:
            await client.start_notify(NOTIFY_CHAR_UUID, notification_handler)
        except BleakError as e:
            print(f"Failed to subscribe: {e}")
            return

        print("Receiving notifications. Press Ctrl+C to stop.\n")
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting script...")
