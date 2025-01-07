# main.py
import serial
import sys
import serial


def test_connection(port="/dev/cu.UD18_SPP", baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        # Try to read a few bytes
        data = ser.read(10)
        ser.close()
        if data:
            print(f"Read some data (length={len(data)}). Connection looks good!")
        else:
            print("No data read, but the port opened successfully.")
    except Exception as e:
        print(f"Error opening port {port}: {e}")
        sys.exit(1)

def main():
    # For now, just test the connection
    test_connection()
    print("Connection test completed.")

if __name__ == "__main__":
    main()
