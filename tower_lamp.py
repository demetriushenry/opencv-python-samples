"""Custom Tower Lamp class using pyserial package.

Plus-725 model
"""
import time

import serial


class TowerLamp:
    """Tower Lamp class implementation."""
    
    CMD_IN_SIGNAL = [0x02, 0x52, 0x03]
    CMD_OUT_SIGNAL = [0x02, 0x53, 0x03]

    CMD_OUT_RELAY_OP_1_W_R1 = [0x02, 0x57, 0x30, 0x03]
    CMD_OUT_RELAY_OP_1_W_R2 = [0x02, 0x57, 0x31, 0x03]
    CMD_OUT_RELAY_OP_1_W_R3 = [0x02, 0x57, 0x32, 0x03]
    CMD_OUT_RELAY_OP_1_W_R4 = [0x02, 0x57, 0x33, 0x03]

    CMD_OUT_RELAY_OP_2_T_R1 = [0x02, 0x54, 0x30, 0x03]
    CMD_OUT_RELAY_OP_2_T_R2 = [0x02, 0x54, 0x31, 0x03]
    CMD_OUT_RELAY_OP_2_T_R3 = [0x02, 0x54, 0x32, 0x03]
    CMD_OUT_RELAY_OP_2_T_R4 = [0x02, 0x54, 0x33, 0x03]

    CMD_OUT_RELAY_OP_3_O_R1_OFF = [0x02, 0x4F, 0x30, 0x30, 0x03]
    CMD_OUT_RELAY_OP_3_O_R1_ON = [0x02, 0x4F, 0x30, 0x31, 0x03]

    CMD_OUT_RELAY_OP_3_O_R2_OFF = [0x02, 0x4F, 0x31, 0x30, 0x03]
    CMD_OUT_RELAY_OP_3_O_R2_ON = [0x02, 0x4F, 0x31, 0x31, 0x03]

    CMD_OUT_RELAY_OP_3_O_R3_OFF = [0x02, 0x4F, 0x32, 0x30, 0x03]
    CMD_OUT_RELAY_OP_3_O_R3_ON = [0x02, 0x4F, 0x32, 0x31, 0x03]

    CMD_OUT_RELAY_OP_3_O_R4_OFF = [0x02, 0x4F, 0x33, 0x30, 0x03]
    CMD_OUT_RELAY_OP_3_O_R4_ON = [0x02, 0x4F, 0x33, 0x31, 0x03]

    RELAY_1 = 1
    RELAY_2 = 2
    RELAY_3 = 3
    RELAY_4 = 4

    def __init__(self, port_path):
        """Towerlamp class constructor.
        
        Arguments:
            port_path {str} -- serial port path on system
        """
        self.port = serial.Serial(
            port_path,
            baudrate=19200,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=1
        )

        self.port.flushInput()

    def _run_cmd(self, cmd):
        self.port.write(cmd)
        time.sleep(0.05)

    def toggle_relay(relay, on=True):
        """Turn On/Off specific relay.
        
        Arguments:
            relay {int} -- relay number (1 ~ 4)
        
        Keyword Arguments:
            on {bool} -- turn On or turn Off relay flag (default: {True})
        
        Returns:
            str -- show result sent by serial port

        """
        if relay == RELAY_1:
            if on:
                cmd = CMD_OUT_RELAY_OP_3_O_R1_ON
            else:
                cmd = CMD_OUT_RELAY_OP_3_O_R1_OFF
        elif relay == RELAY_2:
            if on:
                cmd = CMD_OUT_RELAY_OP_3_O_R2_ON
            else:
                cmd = CMD_OUT_RELAY_OP_3_O_R2_OFF
        elif relay == RELAY_3:
            if on:
                cmd = CMD_OUT_RELAY_OP_3_O_R3_ON
            else:
                cmd = CMD_OUT_RELAY_OP_3_O_R3_OFF
        else:
            if on:
                cmd = CMD_OUT_RELAY_OP_3_O_R4_ON
            else:
                cmd = CMD_OUT_RELAY_OP_3_O_R4_OFF

        length = self._run_cmd(cmd)

        return self.port.read(length)

    def close_connection():
        """Close created serial connection."""
        self.port.close()
