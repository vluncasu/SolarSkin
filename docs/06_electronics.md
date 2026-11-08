# Electronics

## Hardware for the present chain

| Component | Quantity | Role |
|---|---:|---|
| ESP32 | 1 active controller | Generates all phase commands |
| SN74HC595N / 74HC595 | 7 | Eight outputs each; two motors per register |
| ULN2003 driver board | 14 | One per motor |
| 28BYJ-48, 12 V variant | Up to 14 | Confirm winding voltage before connection |
| 12 V, 5 A, 60 W supply | 1 nominal supply | Motor distribution; not an ESP32 GPIO supply |
| Additional ESP32 / three Blue Pill boards | Optional/reserve | No Blue Pill firmware is supplied as a working substitute |

The enclosure concept accommodates four ESP32 boards. That does not mean four controllers are needed for this chain.

## ESP32 to registers

| Signal | ESP32 GPIO | Physical 74HC595 pin |
|---|---:|---:|
| DATA / SER | 23 | 14, REG1 only |
| CLOCK / SRCLK | 18 | 11, all |
| LATCH / RCLK | 21 | 12, all |
| OE | 22 | 13, all; LOW enables outputs |
| Logic supply | 3V3 | 16 |
| SRCLR inactive | 3V3 | 10 |
| Ground | Common GND | 8 |

Cascade **pin 9 QH-prime/NEXT to pin 14 SER/DATA of the next register**. Clock and latch are parallel buses, not serial links. Do not connect OE to both GPIO22 and ground.

## Register outputs to drivers

| Register output | Physical pin | First/second motor input |
|---|---:|---|
| Q0, Q1, Q2, Q3 | 15, 1, 2, 3 | First motor IN1, IN2, IN3, IN4 |
| Q4, Q5, Q6, Q7 | 4, 5, 6, 7 | Second motor IN1, IN2, IN3, IN4 |

REG1 drives M01/M02 through their two driver boards; REG2 M03/M04; ...; REG7 M13/M14. Register pin numbers are not ESP32 GPIO numbers. The motor's five-contact plug goes to its ULN2003 board.

## Frame serialization

Each update shifts **56 bits**, farthest register first, most-significant bit first, followed by one latch pulse. For a common 4-bit motor phase `p`, each register receives `(p & 15) | ((p & 15) << 4)`. The code retains 5-microsecond data/clock delays from the functioning baseline.

In full-step mode the patterns are `0011, 0110, 1100, 1001`: two commanded coils per motor. Reversing the phase order reverses rotation. Half-step mode inserts one-coil states between those patterns. [Microchip stepper modes](https://onlinedocs.microchip.com/oxy/GUID-9537581F-9321-4878-AD68-1F3DE335FF53-en-US-1/GUID-09C5CECC-3B9F-44AB-8033-FCE8E03DC586.html).

## Power and diagnosis

ESP32 was powered by USB; the 12 V supply feeds the 12 V motor drivers. Logic, ESP32 and driver grounds must be common. Never route motor supply through ESP32 GPIO or 3V3. Fit local decoupling and verify the actual logic rail at the chips.

The earlier user-reported **1.5 V on 3V3 remains unresolved in the recorded evidence**. ESP32-WROOM-32 specifies 3.0-3.6 V supply operation; 74HC595 specifies 2-6 V. A software frame counter cannot verify either rail. [Espressif datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf), [TI register datasheet](https://www.ti.com/lit/ds/symlink/sn74hc595.pdf).

For steady coil-current sizing, a first approximation is `I_coil=(V_supply-V_driver_drop)/R_coil`. With two coils per active motor, `I_motors≈2*n*I_coil`. Coil resistance, driver drop, dynamic current and temperature must be measured for the actual variant. The 60 W label does not prove enough margin, maximum torque, or enclosure thermal safety.

## Enclosure draft

Draft electronics boxes are excluded from this essential edition. Their recorded bridge and lid-fit issues remain unresolved; do not assume that enclosure geometry has been validated for mains insulation or thermal operation.
