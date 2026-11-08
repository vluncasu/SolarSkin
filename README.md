# SolarSkin — 3D Printed Kinetic Facade with ESP32

SolarSkin is a **3D printed kinetic facade** for an architectural office-building model. Motor-driven leaves open and close through a printed lead screw, guided carriage and six connecting rods. This repository contains the large building assembly, mechanism CAD, reinforced display frame, color-separated STL files, illustrated assembly manuals and ESP32 firmware.

![SolarSkin office-building model with nine open kinetic facade modules and visible floors](media/renders/building_open.webp)

**[Download the essential package](https://github.com/vluncasu/SolarSkin/releases)** · **[Assembly manual](docs/pdf/SOLARSKIN_ENGINEERING_AND_ASSEMBLY.pdf)** · **[Illustrated parts catalogue](docs/pdf/SOLARSKIN_PARTS_CATALOG.pdf)**

## The building and moving facade

The architectural model has **nine facade module positions**, office floors, furniture and a visible rear structure. Open [BUILDING_ASSEMBLY.blend](cad/04_building_optional/BUILDING_ASSEMBLY.blend) to inspect the complete composition. Editable FreeCAD and STEP building files are included alongside it.

[Building, interior and facade guide](docs/12_building_and_facade.md) explains the models and their relationship to the later mechanism and stand revisions.

![Rear of the SolarSkin office building showing the supporting structure and interior](media/renders/building_rear.webp)

## How the kinetic mechanism works

Each module has **six leaves in three mirrored pairs**. A three-start screw with **10 mm lead** moves a carriage along three guides. Six rods translate that carriage movement into leaf rotation.

| Parameter | Current mechanism |
|---|---:|
| Leaf attachment radius / rod length | 12 mm / 20 mm |
| Wing motion represented in the saved CAD | 0–75 degrees |
| Calculated carriage stroke | 15.348484 mm |
| Screw revolutions for that stroke | 1.534848 |
| Nominal direct-drive command | Approximately 6,287 half-steps |
| Printed parts per module | 28 types / 62 pieces |
| Nine complete mechanisms | 558 printed mechanism pieces |

![Ten-millimetre-lead kinetic facade mechanism with blue structure, white leaves and orange links](media/renders/mechanism_10mm.webp)

The [kinematic model](docs/01_mechanism_and_kinematics.md) and [thread and motor calculations](docs/02_screw_and_motor_calculations.md) derive the motion from the CAD. Lead is 10 mm per revolution; axial pitch is 10/3 mm. The motor's built-in gearbox is already included in its nominal output-step resolution. Any additional reduction must be counted separately.

## Print and assemble

1. Select a configuration: the architectural building or the separate reinforced presentation stand.
2. [Print one mechanism by color](docs/03_printing_and_bom.md), using the [quantity and dimension BOM](bom/mechanism.csv).
3. Follow the [mechanism assembly sequence](docs/04_mechanism_assembly.md). The A4 catalogue shows two views per part and six parts per full sheet.
4. For the stand, use the [frame, reinforcement, feet and module-mounting guide](docs/05_frame_assembly.md).
5. Follow the [ESP32 wiring diagram](docs/06_electronics.md), then calibrate the actual installed reduction before motor operation.

![Reinforced SolarSkin presentation frame populated with sixteen nominal mechanism positions](media/renders/assembly_01.webp)

The frame above has **16 nominal mechanical positions**. The current controller uses **seven 74HC595 registers and fourteen motor channels**. These are separate configurations; the building render does not establish that every latest stand component has been integrated into the architectural model.

## ESP32 firmware

The [firmware guide](docs/07_firmware.md) covers autonomous alternating motion, web override, Wi-Fi setup, compilation and calibration. Three small source variants are included: long exhibition motion, a simple web baseline and a minimal motor test.

```sh
pio run -j 1 -d firmware/baseline_web
```

The long exhibition command is **50,296 half-step-equivalents per direction**. It corresponds to about 122.79 mm at direct drive, or 15.35 mm with an additional 8:1 reduction. The actual added reduction is unconfirmed; this command is not a calibrated direct-drive stroke. No end-stop sensing or automatic homing is implemented.

## Files and validation

| Directory | Contents |
|---|---|
| [cad](cad/) | Building, mechanism and reinforced-frame Blender/FreeCAD/STEP models |
| [print](print/) | Current mechanism, frame, reinforcement and building STL files |
| [bom](bom/) | Quantities, color groups and mechanism dimensions |
| [docs](docs/) | English assembly, electronics, firmware and engineering documentation |
| [engineering](engineering/) | Equations, calculation code, CAD evidence and numerical results |
| [firmware](firmware/) | ESP32 source and motor-control simulations |
| [media](media/) | Building, mechanism, frame and part-identification renders |

All three firmware variants compiled and passed host simulations. Six calculation tests passed. The PDFs were rendered and visually inspected. These checks do not certify physical stiffness, printed fit, electrical wiring or endurance. [Verification and limitations](docs/09_verification.md) · [Primary references](docs/11_references.md).

The multi-gigabyte working history, duplicate full-mechanism STEP export, experimental parts and draft electronics enclosures are excluded. Use the complete essential ZIP in Releases for a download without Git; cloning the editable assets requires Git LFS.

Maintained by [vluncasu](https://github.com/vluncasu). [License status](LICENSE_STATUS.md). Report reproducible problems in [Issues](https://github.com/vluncasu/SolarSkin/issues), including the part ID or firmware variant.
