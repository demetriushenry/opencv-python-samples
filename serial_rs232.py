import io
import sys

import serial


def main():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        timeout=None)
    sio = io.TextIOWrapper(io.BufferedReader(ser))

    print(ser.isOpen())

    while True:
        data = sio.readline()
        if data:
            print('>>', data)
            break

    ser.close()
    print(ser.isOpen())
    del sio


if __name__ == "__main__":
    sys.exit(main())
