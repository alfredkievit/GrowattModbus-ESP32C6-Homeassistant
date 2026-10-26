# Bedrading

```
Omvormer SYS COM            RS485-module              ESP32-C6
  pin 3  ───────────────────  A
  pin 4  ───────────────────  B
                              RXD  ────────────────── GPIO4 (TX)
                              TXD  ────────────────── GPIO5 (RX)
                              VCC  ────────────────── 3V3
                              GND  ────────────────── GND
```

- Pin 3/4 van de SYS COM komt uit de praktijk (o.a. SolarAssistant voor de TL-XH), niet uit de Growatt-handleiding.
  Is er geen antwoord, wissel dan A en B om (veilig).
- **Niet de COM-poort (DRED/PCI) gebruiken:** pin 1 staat op +12 V. Pin 1, 2, 7 en 8 van de SYS COM zijn voor de batterij;
  sluit daar niets op aan.
- Een RS485-module met 3,3 V logica en automatische richting is nodig. Met een module met DE/RE-pinnen moet je die
  in de config zelf aansturen (`flow_control_pin`).
- De wifi-stick en het display blijven gewoon werken.

## UART-pinnen op de ESP32-C6-DevKitM-1

De bedrukking "TX" en "RX" op het bordje is UART0 (**GPIO16/GPIO17**). De "6" en "7" zijn GPIO6/GPIO7.
Deze config gebruikt **GPIO4 (TX) en GPIO5 (RX)** en zet de logger op de USB-serial-JTAG (`hardware_uart: USB_SERIAL_JTAG`),
zodat de logger de UART voor Modbus niet in de weg zit. Andere pinnen kies je met `uart_tx` / `uart_rx` in de substitutions.
