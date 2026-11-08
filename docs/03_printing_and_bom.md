# Printing and BOM

## How the model comes off the printer

A working hinge needs clearance between its moving faces. The leaves,
axles and rods are separate prints. Insert an axle after aligning the two
leaves, then attach the rods. This also leaves their bearing surfaces
accessible for cleaning before assembly.

The carriage and its cover form a pocket around two removable nuts.
You can test the thread outside the frame and replace a tight nut
without printing the carriage again. The rear frame has a side opening
for inserting the screw before the motor clamps close off access.

The tall stand breaks down into cassettes that bolt together after printing.
The ribs span their joints, and the wider base pieces support the feet.
For the office building, print the floor slabs, roof, rear framing,
stairs and interior pieces from their respective color folders.
Open the complete architectural assembly to identify their installed positions.

[Four arranged mechanism beds](13_print_beds.md) ·
[Footprint of each building and stand STL](15_print_dimensions.md)

## Mechanism

[Mechanism CSV](../bom/mechanism.csv) contains **28 types / 62 printed pieces per module**, with totals for 9, 12, 14 and 16 modules. Quantities in filenames apply to **one module**. A single STL normally contains one part, not all requested copies.

| Color | Typical parts | Folder |
|---|---|---|
| Windows blue | Frame, pillars, axles, guides, carriage, split nuts, covers | [Blue](../print/01_mechanism/one_module/windows_blue/) |
| White | Three left wings and three right wings | [White](../print/01_mechanism/one_module/white/) |
| Orange | Lead screw, six link rods, joint nuts, clamp cones and connectors | [Orange](../print/01_mechanism/one_module/orange/) |

Totals: 558 pieces for 9 modules; 744 for 12; 868 for 14; 992 for 16. Motors, drivers, common tools and the support structure are separate.

[Illustrated A4 parts catalogue](pdf/SOLARSKIN_PARTS_CATALOG.pdf) identifies similar parts with two views and their STL bounding-box dimensions. Bounding boxes describe print orientation and must not be confused with nominal thread diameter or under-head length.

## Frame and reinforcement

- [Frame BOM](../bom/frame.csv): frame, tools and receiver mounts for 16 positions. F01/F02 scale with occupied positions: **2 F01 + 1 F02 per module**.
- [Reinforcement BOM](../bom/reinforcement.csv): V4 ribs, base supports, rear-foot adapter and fasteners.
- The **extra F18 rear foot** is in the reinforcement list in addition to the original frame's F18. Reuse an existing extra foot if available.
- Four R41 clips are optional. Do not add the obsolete R40 organizer to the new requirement.

## Print setup

The prototype used a Bambu Lab P1S with a 0.4 mm nozzle. The user's Strong 0.20 mm profile is a starting point, not a supplied or certified universal profile. The three revised transmission parts had an earlier support-disabled slicing check at 0.16 mm, six walls and 100% infill. This does not validate every part with every filament.

Keep millimetres and 100% scale. Preserve delivered orientation where applicable. Do not globally scale an assembly to repair a thread fit. Remove first-layer burrs and test the screw/nut pair by hand before motor operation. Print a fit coupon or one complete module before producing a batch.

The publication preparation does not invoke Bambu Studio or claim new slicing times. Historical 3MF batch layouts are not included in this edition.

## Architectural building

Choose the [furnished office beds](../print/furnished/) or the [simplified office beds](../print/simplified/). Each inventory excludes the sixteen existing mechanisms.

[Shared printed tools](../print/08_shared_tools/) are workshop tools: print once, not once per mechanism. Historical batch layouts, experimental axles and draft electronics enclosures are excluded from this essential edition.
