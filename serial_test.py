import sys
import time

import serial


def segments(data, size=16):
    for a in range(0, len(data), size):
        yield data[a:a + size]


def example_1():
    bytes_0to255 = bytes(bytearray(range(256)))

    serial_port = serial.serial_for_url(
        'loop://',
        timeout=0
    )

    print('Serial port:', serial_port.portstr)

    serial_port.flushInput()

    # while True:
    try:
        for block in segments(bytes_0to255):
            length = len(block)
            serial_port.write(block)
            time.sleep(0.05)

            print('length:', serial_port.in_waiting)
            print('result:', serial_port.read(length))

        # header = [0x02, 0x56, 0x03]
        # serial.write(header)
        # res = serial.readline()
        # print(res)
    except Exception as e:
        print('Error:', e)
        serial_port.close()
        # break


def example_2():
    serial_port = serial.Serial('/dev/ttyUSB1')

    print('Serial port:', serial_port.portstr)

    serial_port.write('Test'.encode('utf-8'))
    time.sleep(0.05)

    print(serial_port.read(len('Test')).decode('utf-8'))

    serial_port.close()


def test_tower_lamp():
    serial_port = serial.Serial(
        '/dev/ttyUSB2',
        baudrate=19200,
        bytesize=8,
        parity=serial.PARITY_NONE,
        stopbits=1
    )

    serial_port.flushInput()

    cmd_input_signal = [0x02, 0x52, 0x03]
    cmd_output_signal = [0x02, 0x53, 0x03]

    cmd_output_relay_1 = [0x02, 0x57, 0x30, 0x03]
    cmd_output_relay_2 = [0x02, 0x54, 0x30, 0x03]
    cmd_output_relay_3 = [0x02, 0x4F, 0x31, 0x30, 0x03]

    length = serial_port.write(cmd_output_relay_3)

    time.sleep(0.5)

    # while True:
    res = serial_port.read(length)
    print(res)

    serial_port.close()


def main():
    test_tower_lamp()


if __name__ == "__main__":
    sys.exit(main())
