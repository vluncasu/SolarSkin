# Large office building and kinetic facade

The architectural assembly combines a multi-storey office-building shell, floors, furniture, service cores and nine facade module positions in a three-by-three arrangement. It is the main architectural presentation model in this repository.

![Office-building model with nine open kinetic facade modules](../media/renders/building_open.webp)

## Open the assembly

Use [BUILDING_ASSEMBLY.blend](../cad/04_building_optional/BUILDING_ASSEMBLY.blend) to inspect the complete architectural composition and the integrated moving-module geometry. [BUILDING.FCStd](../cad/04_building_optional/BUILDING.FCStd) provides the editable building model, and [BUILDING_FACADE.step](../cad/04_building_optional/BUILDING_FACADE.step) provides its exchange geometry. Blender materials and earlier model identifiers are preserved to retain the original assembly and animation references.

![Office-building facade in its closed presentation pose](../media/renders/building_closed.webp)

## Inspect the interior and rear structure

![Rear structure of the office-building kinetic facade](../media/renders/building_rear.webp)

![Office floors, furniture and interior arrangement](../media/renders/building_floors.webp)

The shell, floors and furniture belong to the architectural display. They are not additional items in the 62-piece mechanism BOM. Use the [building print set](../print/07_building_optional/) for architectural pieces and the [mechanism BOM](../bom/mechanism.csv) for each complete module. Nine complete current mechanisms require 558 printed mechanism pieces, in addition to the building.

## Which configuration is being shown?

| Configuration | Module positions | Role |
|---|---:|---|
| Original architectural building | 9 | Building and interior presentation |
| Reinforced presentation stand | 16 nominal | Separate current frame and mounting reference |
| Current ESP32 register chain | 14 motor channels | Seven 74HC595 registers; physical motion depends on working drivers and wiring |

The architectural renders predate the latest reinforced stand and show an earlier green/white/orange material palette. The current mechanism print set specifies blue structural parts, white leaves and orange transmission/accent parts. Do not interpret material colors as different part quantities or assume that the architectural assembly silently incorporates every later reinforcement revision.

## Assemble and explain the motion

Build one module with the [step-by-step mechanism instructions](04_mechanism_assembly.md), then inspect its connector and receiver before repeating it across the facade. The current stand's [F01/F02 cassette mounting](05_frame_assembly.md) belongs to that stand; it must not be substituted for a different building attachment without checking the mating CAD geometry.

Each current module has six leaves, six rods and a guided carriage driven by a three-start lead screw. A 10 mm lead produces 10 mm carriage travel per screw revolution. The saved 0–75 degree wing motion requires 15.348484 mm of carriage travel, or 1.534848 screw revolutions. [Exact equations and reduction-dependent motor counts](02_screw_and_motor_calculations.md) explain the motion without confusing screw revolutions, motor-output turns and the motor's internal gearbox.

The renders show design geometry rather than a load-tested building. The architectural mounting and the latest mechanism interfaces must be compared before manufacturing a full architectural assembly.
