# Problemen oplossen

| Symptoom | Oorzaak / oplossing |
|---|---|
| Led rood, sensoren `unknown` overdag | Verkeerde baudrate of A/B verwisseld. De omvormers uit dit project stonden op **38400** (holding 22 = 1), eerder op 9600. De config wisselt zelf na 90 s. Probeer anders A en B om te wisselen. |
| Sensoren `unknown` na een update vanuit de ESPHome Builder | De YAML in `/config/esphome/` was een oudere versie (andere pinnen/baudrate). Zet de actuele bestanden in `/config/esphome/` en flash opnieuw. |
| Geen enkel antwoord, ook niet na wisselen | Pinnen controleren: de bedrukking TX/RX op het bordje is GPIO16/17. Controleer RXD → TX en TXD → RX (gekruist). |
| Losse time-outs | Zet `max_cmd_retries: 4` en `command_throttle: 500ms` (staat al zo) en houd de kabel kort. |
| 's Nachts niets | Normaal: de omvormer slaapt zonder PV-vermogen. |
| Modbus-waarden wijken af van de Growatt-cloud | De cloud middelt over 5 minuten, Modbus is een momentopname elke 10 s. Vergelijk dagtotalen (kWh) voor een eerlijke vergelijking. |

## Uitlezen testen met een USB-adapter

Sluit een USB-RS485-adapter aan op pin 3/4 en draai `tools/growatt_modbus_poc.py`. Werkt dat wel maar de ESP32 niet, dan
ligt het aan de bedrading of de pinnen van het bordje; werkt het niet, dan ligt het aan baudrate, A/B of het slave-adres
(standaard 1).
