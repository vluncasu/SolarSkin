# SolarSkin - kinetic facade design for three architectural prototypes

![Furnished office with a sixteen-module kinetic facade](media/renders/furnished_open.webp)

The same six-leaf mechanism appears in three configurations. Choose the
assembly that corresponds to the question you want to investigate.

| Furnished office | Simplified office | Independent stand |
|---|---|---|
| ![Office interior and stairs](media/renders/furnished_interior.webp) | ![Rapid office model](media/renders/simplified_open.webp) | ![Reinforced frame](media/renders/assembly_03.webp) |
| [Open building CAD](cad/furnished/OFFICE_16.blend) | [Open building CAD](cad/simplified/OFFICE_16.blend) | [Open stand CAD](cad/03_reinforced_assembly/REINFORCED_16_MODULE_ASSEMBLY.blend) |
| [46 architectural print beds](print/furnished/) | [63 architectural print beds](print/simplified/) | [Frame and foot assembly](docs/05_frame_assembly.md) |

[Read the comparative design study](docs/12_building_and_facade.md) ·
[Download the study as a PDF](docs/pdf/SOLARSKIN_COMPARATIVE_DESIGN_STUDY.pdf).
It traces the design from the office interior to the support frame and
relates both to the actuator stroke and the fourteen-channel controller.

[Download the project and illustrated manuals](https://github.com/vluncasu/SolarSkin/releases).

## Print one working module

| Filament | Pieces | What to look for |
|---|---:|---|
| Windows blue | 30 | Hub, guides, carriage, split nuts, axles and mounting parts |
| White | 6 | Three left leaves and three right leaves |
| Orange | 26 | Lead screw, links, joint nuts and connectors |

Start with the orange P13 screw and the blue P12 and P26 nuts.
Thread each nut onto the screw by hand. One turn advances it 10 mm.
This small print checks the fit of the most sensitive interface
before you commit to printing the full facade.

[Four prearranged 3MF plates](print/09_one_module_plates/) ·
[One-module bed layouts](docs/13_print_beds.md) ·
[Dimensions of every printable STL](docs/15_print_dimensions.md) ·
[Color folders and quantities](docs/03_printing_and_bom.md) ·
[Illustrated parts catalogue](docs/pdf/SOLARSKIN_PARTS_CATALOG.pdf)

## Assemble the mechanism

| Screw and split nuts | Screw entering the frame |
|---|---|
| ![Orange lead screw passing through the blue nuts](media/renders/lead_screw_10mm.webp) | ![Side opening used to insert P13 before fitting the motor](media/renders/screw_insertion_01.webp) |

The carriage slides along three guides. Push the screw through the side
opening in the rear frame before fitting the motor. Each printed axle carries
a left and a right leaf. A short rod connects each leaf to the carriage.
Turn the assembled screw by hand and watch all six joints through a full cycle.

[Module assembly, in order](docs/04_mechanism_assembly.md) ·
[Frame, feet and receiver mounting](docs/05_frame_assembly.md) ·
[Engineering and assembly PDF](docs/pdf/SOLARSKIN_ENGINEERING_AND_ASSEMBLY.pdf)

## Calculate how far the motor must turn

Three helices share the screw. Adjacent crests are 3.333 mm apart along its
axis. Follow the same helix for a complete turn and it climbs 10 mm.
The 12 mm pivot arm and 20 mm rod need 15.348 mm of carriage travel
to move a leaf from 0 to 75 degrees in CAD.

That takes 15.348 / 10 = 1.535 screw turns. At direct drive, the motor's
nominal 4,096 half-steps per geared output turn give about 6,287 half-steps.
With an additional reduction, multiply by the measured number of motor
output turns per screw turn.

[Thread profile, helix equations and clearance](docs/02_screw_and_motor_calculations.md) ·
[Linkage derivation](docs/01_mechanism_and_kinematics.md) ·
[Reproduce the calculations](engineering/calculations.py)

## Wire and run the controller

One ESP32 sends 56 bits through seven 74HC595 registers.
Each register feeds two ULN2003 drivers. Each driver operates one
12 V motor. The baseline firmware cycles through opening and closing
as soon as its startup delay ends. A phone connected to the SolarSkin
Wi-Fi network can stop, resume or reverse the motion.

The exhibition program uses 25,148 full steps per direction.
Measure the extra reduction before using that setting. With direct coupling,
it would command about 122.8 mm against a CAD stroke of only 15.35 mm.
The controller counts commands and has no end-position sensor.

[Pin-by-pin wiring](docs/06_electronics.md) ·
[Set the travel, upload firmware and open the controls](docs/07_firmware.md) ·
[What was tested](docs/09_verification.md) · [Engineering references](docs/11_references.md)

Maintained by [vluncasu](https://github.com/vluncasu).
[License status](LICENSE_STATUS.md).
