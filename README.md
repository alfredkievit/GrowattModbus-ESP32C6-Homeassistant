# Growatt Modbus → Home Assistant (ESP32-C6 + ESPHome)

Een Growatt-omvormer (MIN TL-X / TL-XH, getest op een 3600TL-X en een MIN 4600TL-XH) lokaal uitlezen via
**Modbus RTU over RS485**, met een ESP32-C6 en ESPHome. Geen cloud, geen Growatt-stick nodig: de waarden komen elke
**10 seconden** in Home Assistant (de cloud geeft er elke 5 minuten één).

*English summary: ESPHome config for reading Growatt MIN TL-X(H) inverters over Modbus RTU (SYS COM port, RS485) with an ESP32-C6. 38400 baud, slave 1, input registers 3000+. Read-only.*

## Wat je nodig hebt

| Onderdeel | Opmerking |
|---|---|
| ESP32-C6-DevKitM-1 | andere ESP32-varianten kunnen ook, pas `variant` en pinnen aan |
| RS485-module met automatische richting (TTL ↔ RS485, 3,3 V) | geen DE/RE-pin nodig; zie hieronder |
| Kabel naar de **SYS COM**-aansluiting van de omvormer | pin 3 = A, pin 4 = B |
| Home Assistant met ESPHome | de ESPHome-integratie ontdekt het bordje vanzelf |

### De RS485-module

Een goedkoop blauw TTL-naar-RS485-printje (MAX485-type met automatische richtingsschakeling), met aan de ene kant een
schroefklem **A+ / B−** (naar de omvormer) en aan de andere kant de TTL-aansluiting (4-pins JST-stekker of pinnen) met
**VCC, TXD, RXD, GND** (naar de ESP32). Er zitten twee ledjes op (TXD/RXD): het RXD-ledje knippert als de omvormer antwoordt.
Controleer de volgorde van de pinnen op de print zelf; die verschilt per verkoper.

## Bedrading (kort, zie [docs/bedrading.md](docs/bedrading.md))

| RS485-module | Naar |
|---|---|
| A | SYS COM pin 3 |
| B | SYS COM pin 4 |
| RXD | ESP32 **GPIO4** (TX) |
| TXD | ESP32 **GPIO5** (RX) |
| VCC / GND | 3V3 / GND |

> **Let op:** gebruik de **SYS COM**-poort, nooit de COM/DRED-poort (daar staat +12 V op pin 1).
> De bedrukking "TX/RX" op het C6-bordje is UART0 (GPIO16/17) en niet de pinnen uit deze config.

## Snel starten

1. `cp esphome/secrets.example.yaml esphome/secrets.yaml` en vul wifi en een API-sleutel in.
2. Kopieer `esphome/growatt-example.yaml` naar bijvoorbeeld `growatt-dak.yaml`, geef het een eigen `name` en pas
   `latitude`/`longitude` aan (alleen voor de nacht-kleur van de led).
3. Compileren en flashen: `esphome run growatt-dak.yaml` (eerste keer via USB, daarna via wifi/OTA).
4. In Home Assistant verschijnt het apparaat met onder meer AC-vermogen, PV1/PV2 spanning, stroom en vermogen,
   netspanning, netstroom, netfrequentie, energie vandaag/totaal en omvormertemperatuur.

Gebruik je de ESPHome Builder in Home Assistant, zet dan dezelfde bestanden in `/config/esphome/` (inclusief `common/`).
Een oudere kopie daar wordt anders bij een update weer op het bordje gezet.

## Statusled

De ingebouwde WS2812 (GPIO8) laat de toestand zien:

| Kleur | Betekenis |
|---|---|
| Groen | wifi en Modbus ok |
| Oranje | Modbus ok, geen wifi |
| Rood | geen Modbus-antwoord |
| Blauw | nacht (zon < 3° boven de horizon) en geen Modbus: de omvormer slaapt, geen storing |

## Goed om te weten

- **Baudrate 38400.** De omvormer kan op 9600 of 38400 staan (holding register 22). De firmware begint op 38400 en wisselt
  na 90 s zonder antwoord naar 9600 en terug. Zie [docs/problemen-oplossen.md](docs/problemen-oplossen.md).
- **'s Nachts geen data.** De omvormer slaapt zonder zon en antwoordt dan niet. Dat is normaal; de sensoren worden
  `unknown` en komen 's ochtends vanzelf terug.
- **Alleen lezen.** Er wordt uitsluitend functiecode 0x04 gebruikt; de firmware schrijft nooit registers.
- Registerkaart en schaalfactoren: [docs/registers.md](docs/registers.md).

## Testen zonder ESP32

`tools/growatt_modbus_poc.py` leest de omvormer met een USB-RS485-adapter (pyserial):

```bash
pip install pyserial
python tools/growatt_modbus_poc.py COM5                 # of /dev/ttyUSB0
GROWATT_BAUD=9600 python tools/growatt_modbus_poc.py COM5
python tools/growatt_modbus_poc.py COM5 raw 3000 20    # ruwe registers
```

## Licentie

MIT, zie [LICENSE](LICENSE). Gebruik op eigen risico: je sluit aan op een omvormer die aan het net hangt.
