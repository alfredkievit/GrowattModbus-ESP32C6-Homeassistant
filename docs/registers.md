# Registerkaart (input registers, functiecode 0x04)

TL-X/XH-kaart 3000..3124 (de oude kaart 0..124 geeft dezelfde waarden). Serie: 38400 of 9600 baud, 8N1, slave 1.
Waarden zijn gecontroleerd tegen het display van de omvormer en tegen de Growatt-cloud (Grott).

| Register | Betekenis | Schaal | Opmerking |
|---|---|---|---|
| 3000 | Status | – | 1 = normaal |
| 3001–3002 | PV-vermogen totaal (u32) | 0,1 W | |
| 3003 / 3004 / 3005–3006 | PV1 spanning / stroom / vermogen | 0,1 V / 0,1 A / 0,1 W | |
| 3007 / 3008 / 3009–3010 | PV2 spanning / stroom / vermogen | 0,1 V / 0,1 A / 0,1 W | |
| 3023–3024 | AC-vermogen (u32) | 0,1 W | |
| 3025 | Netfrequentie | 0,01 Hz | |
| 3026 | Netspanning fase 1 | 0,1 V | |
| 3027 | Netstroom fase 1 | 0,1 A | |
| 3047–3048 | Werkuren (u32) | 0,5 s | |
| 3049–3050 | Energie vandaag (u32) | 0,1 kWh | |
| 3051–3052 | Energie totaal AC (u32) | 0,1 kWh | |
| 3053–3054 | Energie totaal PV (u32) | 0,1 kWh | |
| 3093 | Temperatuur omvormer | 0,1 °C | |

Holding 22 = baudrate-keuze (1 = 38400). Holding 3001–3005 bevat het serienummer als ASCII (op sommige modellen).
Alleen lezen: schrijf nooit registers met functiecode 0x06/0x10.
