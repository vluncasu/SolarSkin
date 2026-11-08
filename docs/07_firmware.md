# Firmware and calibration

| Variant | Mode | Default command per direction | Intended use |
|---|---|---:|---|
| [`stand`](../firmware/stand/) | Full-step, two coils active | 25,148 full steps = 50,296 half-step-equivalents | Long demonstration; requires calibrated downstream reduction/travel |
| [`baseline_web`](../firmware/baseline_web/) | Half-step, synchronized | 6,287 half-steps | 4 November simple motion baseline with web override |
| [`minimal`](../firmware/minimal/) | Half-step, no Wi-Fi | 6,287 half-steps | Isolating the motor command from networking |

All present variants command **seven registers and fourteen motor channels**. None detects which motors actually move. All channels receive the same phase; the historical independently choreographed firmware is not the current synchronized baseline.

## Autonomous state machine

```text
POWER ON -> startup delay -> OPEN -> short reversal pause -> CLOSE -> repeat
Web Open/Close -> change target -> finish that direction -> resume alternating
Web Stop -> zero all motor outputs -> remain stopped until Resume
```

The motion loop does not require a browser or Wi-Fi client. The network task runs separately. In the exhibition mode, both coils remain energized through the 0.3-second reversal pause; Stop clears them. Startup delay is three seconds in `stand`, five seconds in the baseline.

## Calibration before running the long demo

1. Identify the installed thread family: P13/P12/P26 with 10 mm lead.
2. Measure the additional reduction **after** the motor's built-in gearbox. Define `G = geared-output turns / screw turns`.
3. With power off, confirm the mechanism's unobstructed endpoints. The CAD target is about 15.35 mm, not an arbitrary long run.
4. Run `python3 engineering/calculations.py --reduction G --mode full` or `--mode half` and choose a conservative initial count.
5. Update the selected firmware's stroke constant or its stopped-state setting. Test an observed cycle and account for real end clearance, backlash and missed steps.

The long default is roughly an 8:1 downstream-reduction example. Without that reduction it commands much more than the source CAD stroke. No physical homing or end-stop sensing is implemented. Power cycling assumes the mechanism is closed; it is not a recovery procedure for an unknown position.

## Wi-Fi configuration

```sh
cd firmware/stand             # or firmware/baseline_web
cp src/config.example.h src/solarskin_config.h
```

Choose a local password in `solarskin_config.h`. That file is ignored by Git. Without it the public example uses `CHANGE_THIS_PASSWORD`; it is not a secret. The original device's credentials were not changed by preparing this repository.

Connect to **SolarSkin**, then open **http://192.168.4.1** or **http://solarskin2.local** where mDNS is supported. The network is local and does not provide Internet access.

The graphical firmware interface is embedded in a C++ header; there is no separate HTML catalogue or documentation website in this package. Edit the `PAGE` string in the relevant header and rebuild.

## Build and upload

```sh
pio run -j 1 -d firmware/stand
pio run -j 1 -d firmware/stand -t upload
```

Use one connected ESP32 and a USB data cable. The platform and board are pinned in `platformio.ini`. No precompiled private firmware binary is distributed. `FLASH.command` is a convenience wrapper for a local build and upload; it is not executed by repository preparation.

## Tests

```sh
python3 engineering/test_calculations.py
c++ -std=c++17 -O2 firmware/stand/test/firmware_test.cpp -o /tmp/solarskin-test
/tmp/solarskin-test
```

The baseline web variant has an equivalent test; the minimal version has `host_test.cpp`. Simulation checks phase packing, 56 clocks per latch, automatic reversal, bounds, Stop/Resume and override behavior. It does not measure electrical levels or motor shaft rotation.
