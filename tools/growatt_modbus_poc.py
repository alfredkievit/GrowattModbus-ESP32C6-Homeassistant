#!/usr/bin/env python3
"""Proof of concept: Growatt MIN TL-X uitlezen via RS485 (Modbus RTU), zonder cloud.

Alleen lezen (functie 0x04, input registers). Vereist alleen pyserial:
    pip install pyserial
    python growatt_modbus_poc.py COM5          # Windows
    python growatt_modbus_poc.py /dev/ttyUSB0  # Linux
    python growatt_modbus_poc.py COM5 raw 3000 20   # ruwe registers 3000..3019 (ook 0 en 1000 proberen)

Aansluiting: adapter A/D+ naar pin 3 (A), B/D- naar pin 4 (B) van de COM-stekker
(pinout eerst controleren op het label van de omvormer; bij geen antwoord A en B omwisselen).
Instellingen: 38400 baud (oudere firmware: 9600, zet GROWATT_BAUD=9600), 8N1, adres 1. Registers volgens het Growatt Modbus RTU-protocol
(3000-reeks voor MIN/MAX TL-X); controleer de schaalfactoren tegen het display.
"""
import os
import struct
import sys
import time

import serial

BAUD = int(os.environ.get("GROWATT_BAUD", 38400))
ADDR = 1


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def read_input(ser, start, count):
    req = struct.pack(">BBHH", ADDR, 0x04, start, count)
    req += struct.pack("<H", crc16(req))
    ser.reset_input_buffer()
    ser.write(req)
    want = 5 + 2 * count
    resp = ser.read(want)
    if len(resp) < want:
        raise IOError(f"geen/te kort antwoord ({len(resp)} van {want} bytes): A/B omwisselen?")
    if crc16(resp[:-2]) != struct.unpack("<H", resp[-2:])[0]:
        raise IOError("CRC-fout")
    if resp[1] & 0x80:
        raise IOError(f"Modbus-fout {resp[2]}")
    return list(struct.unpack(f">{count}H", resp[3:-2]))


def u32(regs, i):
    return (regs[i] << 16) | regs[i + 1]


def raw(port, start, count):
    with serial.Serial(port, BAUD, bytesize=8, parity="N", stopbits=1, timeout=1) as ser:
        regs = read_input(ser, start, count)
    for i, v in enumerate(regs):
        print(f"{start + i}: {v}")


def main(port):
    with serial.Serial(port, BAUD, bytesize=8, parity="N", stopbits=1, timeout=1) as ser:
        while True:
            try:
                r = read_input(ser, 3000, 100)  # 3000..3099
            except IOError as e:
                print(time.strftime("%H:%M:%S"), "FOUT:", e)
                time.sleep(2)
                continue
            print(time.strftime("%H:%M:%S"),
                  f"status={r[0]}",
                  f"Ppv={u32(r, 1) / 10:.1f}W",
                  f"Vpv1={r[3] / 10:.1f}V Vpv2={r[7] / 10:.1f}V",
                  f"Pac={u32(r, 23) / 10:.1f}W",
                  f"Fac={r[25] / 100:.2f}Hz Vac={r[26] / 10:.1f}V",
                  f"vandaag={u32(r, 49) / 10:.1f}kWh totaal={u32(r, 51) / 10:.1f}kWh",
                  f"T={r[93] / 10:.1f}C")
            time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[2] == "raw":
        raw(sys.argv[1], int(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(__doc__)
