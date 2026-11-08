# Print beds for one six-leaf module

Use the STLs at 100% scale in millimetres. Each row below is one copy.
Start with one module. Either sixteen-position office repeats this list sixteen times when all modules are new.
The stand, tools and office furniture have their own print folders.

These layouts use the exported X/Y bounding boxes on a 256 mm square bed.
X and Y locate the lower-left corner of each bounding box, measured from the
lower-left corner of the bed. For a slicer that positions parts by their centre,
add half the width to X and half the depth to Y. Keep the exported orientation.
The layout leaves 10 mm around the edge and at least 5 mm between boxes.
Check the printer exclusion area and allow extra room for any brim or purge line.

[Download the four prearranged 3MF plates](../print/09_one_module_plates/).
Open each file in millimetres and keep its part placements. These files contain
the actual meshes with their lowest vertices on the bed. Select filament,
printer and process settings in your slicer before generating toolpaths.

For the stand, the two foot designs and their base supports extend 246 mm
along one axis. Centered on a nominal 256 mm bed, that leaves 5 mm at each
end. Preview each one on its own with the printer's excluded corner enabled.
[Check every building and stand piece by filename](15_print_dimensions.md).

## Before starting the batch

Use the P1S with a 0.4 mm nozzle and the project's 0.20 mm Strong profile as a starting point.
Preview the first layer of each part. Check that small axles and screw heads have enough contact to stay down.
Inspect the first layer of every bridge and the underside of the thread flanks in the layer preview.
Only the revised screw and two nuts have a recorded support-off slicing check at 0.16 mm.
The layout below checks footprint clearance. A successful first print is the fit test for your filament.

Print P13, P12 and P26 first. Turn the screw through each nut by hand.
One full turn should advance the nut 10 mm. If it binds, check for a first-layer lip
and confirm that all three files belong to the 10 mm set before printing the rest.


### Windows Blue - plate 1

| Part | X | Y | Width | Depth |
|---|---:|---:|---:|---:|
| P09 | 10.00 | 10.00 | 6.00 | 112.65 |
| P09 | 21.00 | 10.00 | 6.00 | 112.65 |
| P09 | 32.00 | 10.00 | 6.00 | 112.65 |
| P05 | 42.99 | 10.00 | 61.00 | 110.90 |
| P05 | 108.99 | 10.00 | 61.00 | 110.90 |
| P05 | 174.99 | 10.00 | 61.00 | 110.90 |
| E01 | 42.99 | 125.90 | 80.00 | 95.50 |
| E02 | 127.99 | 125.90 | 80.00 | 95.50 |
| P03 | 212.99 | 125.90 | 13.00 | 21.00 |
| P03 | 230.99 | 125.90 | 13.00 | 21.00 |
| P12 | 10.00 | 127.65 | 13.00 | 13.00 |
| P26 | 10.00 | 145.65 | 13.00 | 13.00 |
| P29 | 212.99 | 151.90 | 12.00 | 12.00 |
| P29 | 229.99 | 151.90 | 12.00 | 12.00 |
| P31 | 10.00 | 163.65 | 13.00 | 11.26 |
| P31 | 212.99 | 168.90 | 13.00 | 11.26 |
| P36 | 230.99 | 168.90 | 12.00 | 10.39 |
| P33 | 10.00 | 179.91 | 12.00 | 10.39 |
| P33 | 230.99 | 184.29 | 12.00 | 10.39 |
| E03 | 28.00 | 127.65 | 8.00 | 8.00 |
| E03 | 28.00 | 140.65 | 8.00 | 8.00 |
| E03 | 28.00 | 153.65 | 8.00 | 8.00 |
| P08 | 28.00 | 166.65 | 7.00 | 7.00 |
| P08 | 28.00 | 178.65 | 7.00 | 7.00 |
| P08 | 212.99 | 185.16 | 7.00 | 7.00 |

### Windows Blue - plate 2

| Part | X | Y | Width | Depth |
|---|---:|---:|---:|---:|
| P02 | 10.00 | 10.00 | 86.21 | 87.00 |
| P10 | 101.21 | 10.00 | 85.14 | 73.76 |
| P04 | 191.35 | 10.00 | 42.51 | 41.50 |
| P45 | 191.35 | 56.50 | 46.00 | 26.00 |
| P11 | 191.35 | 87.50 | 42.40 | 22.00 |

### White - plate 1

| Part | X | Y | Width | Depth |
|---|---:|---:|---:|---:|
| P07L | 10.00 | 10.00 | 75.63 | 43.90 |
| P07L | 90.63 | 10.00 | 75.63 | 43.90 |
| P07L | 10.00 | 58.90 | 75.63 | 43.90 |
| P07R | 90.63 | 58.90 | 77.48 | 43.90 |
| P07R | 10.00 | 107.80 | 77.48 | 43.90 |
| P07R | 92.48 | 107.80 | 77.48 | 43.90 |

### Orange - plate 1

| Part | X | Y | Width | Depth |
|---|---:|---:|---:|---:|
| P16 | 10.00 | 10.00 | 7.40 | 27.40 |
| P16 | 22.40 | 10.00 | 7.40 | 27.40 |
| P16 | 34.80 | 10.00 | 7.40 | 27.40 |
| P16 | 47.20 | 10.00 | 7.40 | 27.40 |
| P16 | 59.60 | 10.00 | 7.40 | 27.40 |
| P16 | 72.00 | 10.00 | 7.40 | 27.40 |
| P44 | 84.40 | 10.00 | 24.00 | 24.00 |
| P13 | 113.40 | 10.00 | 16.00 | 16.00 |
| P30 | 134.40 | 10.00 | 12.00 | 10.39 |
| P30 | 151.40 | 10.00 | 12.00 | 10.39 |
| P46 | 168.40 | 10.00 | 10.00 | 10.00 |
| P37 | 183.40 | 10.00 | 11.00 | 9.53 |
| P34 | 199.40 | 10.00 | 11.00 | 9.53 |
| P34 | 215.40 | 10.00 | 11.00 | 9.53 |
| P32 | 231.40 | 10.00 | 8.00 | 8.00 |
| P32 | 231.40 | 23.00 | 8.00 | 8.00 |
| P32 | 183.40 | 24.53 | 8.00 | 8.00 |
| P32 | 196.40 | 24.53 | 8.00 | 8.00 |
| P32 | 209.40 | 24.53 | 8.00 | 8.00 |
| P32 | 168.40 | 25.00 | 8.00 | 8.00 |
| P32 | 134.40 | 25.39 | 8.00 | 8.00 |
| P32 | 147.40 | 25.39 | 8.00 | 8.00 |
| P32 | 113.40 | 31.00 | 8.00 | 8.00 |
| P32 | 222.40 | 36.00 | 8.00 | 8.00 |
| P32 | 235.40 | 36.00 | 8.00 | 8.00 |
| P32 | 181.40 | 37.53 | 8.00 | 8.00 |
