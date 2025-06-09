#!/usr/bin/python
import argparse
import serial
import sys
import re

parser = argparse.ArgumentParser()

parser.add_argument("port")

args = parser.parse_args()

ser = serial.Serial(args.port)
ser.write(b'AT+MODE=TEST\r\n')
print(ser.readline())
ser.write(b'AT+TEST=RFCFG,915,SF7,125,12,12,14,OFF,OFF,ON\r\n')
print(ser.readline())
ser.write(b'AT+TEST=RXLRPKT\r\n')
print(ser.readline())

while(1):
    try:
        incoming = ser.readline().decode('ascii', errors="replace")
        # regex escaping is miserable but this seems to work
        if (match := re.match("\+TEST: RX \\\"([0-9A-F]*)\\\"\r\n", incoming)) is not None:
            print(bytearray.fromhex(match.group(1)).decode('ascii', errors="replace"))
        else:
            print(incoming, file=sys.stderr)
    except KeyboardInterrupt:
        break