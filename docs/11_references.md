# Technical references

## Project evidence

- `engineering/evidence/cad_stroke_samples.json`: final 10 mm-drive stroke and nine CAD positions.
- `engineering/evidence/thread_geometry_check.json`: lead, starts, clearance and source solid checks.
- `engineering/evidence/original_kinematic_helpers.py`: r=12 mm, l=20 mm kinematic function used by the source CAD.
- `engineering/source/rebuild_thread.FCMacro`: portable matched-thread generator with preserved interface reference.
- `bom/`: manufacturing quantities and STL dimensions.

## Primary technical documentation

- [Thomson: screw pitch and lead](https://www.thomsonlinear.com/en/support/tips/difference-between-screw-pitch-and-lead).
- [Thomson: Precision Screws catalogue](https://www.thomsonlinear.com/downloads/screws/Precision_Screws_ctuk.pdf).
- [WM Berg: lead-screw calculations](https://www.wmberg.com/resources/tech-and-application-support/lead-screw-load).
- [TI: SN74HC595 datasheet](https://www.ti.com/lit/ds/symlink/sn74hc595.pdf).
- [TI: ULN2003A datasheet](https://www.ti.com/lit/ds/symlink/uln2003a.pdf).
- [Espressif: ESP32-WROOM-32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf).
- [Microchip: stepper drive modes](https://onlinedocs.microchip.com/oxy/GUID-9537581F-9321-4878-AD68-1F3DE335FF53-en-US-1/GUID-09C5CECC-3B9F-44AB-8033-FCE8E03DC586.html).
- [Gentiam: vendor 28BYJ-48 reference datasheet](https://www.gentiam.com/wp-content/uploads/2022/09/GentiamElectronics-28BYJ-48-Stepper-Motor-Datasheet-Rev20220925-final.pdf). This supports the nominal motor-family discussion; the actual motor manufacturer and exact gearbox ratio are unverified.

## Repository handling

- [GitHub: large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
- [GitHub: repository licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

External specifications are not measurements of this prototype. The calculation examples identify their assumptions explicitly.
