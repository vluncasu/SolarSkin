# Lead screw, motor rotations and reduction

## 1. Lead is not pitch

For `n` thread starts, axial pitch `p` and lead `L`:

$$L=n p.$$

SolarSkin uses **n = 3**, **L = 10 mm/revolution**, hence **p = 10/3 = 3.333333 mm**. One complete screw revolution advances the nut 10 mm, not 3.333 mm. The three starts are spaced by 120 degrees. This is a custom matched printed thread, not an ISO fastener designation.

Sources: [Thomson: pitch versus lead](https://www.thomsonlinear.com/en/support/tips/difference-between-screw-pitch-and-lead), [WM Berg: lead-screw calculations](https://www.wmberg.com/resources/tech-and-application-support/lead-screw-load).

## 2. Geometry implemented in CAD

The generator constructs each helix with lead 10 mm and rotates its matching section by `i*120 deg`, for `i = 0,1,2`. A helix can be written as

$$H_i(t)=\left[R\cos(t+2\pi i/3),R\sin(t+2\pi i/3),z_0+Lt/(2\pi)\right].$$

Here, t is the angle turned in radians. Follow one ridge with your finger.
After a quarter turn its height has increased by 2.5 mm. After a whole turn
it has increased by 10 mm. The offset angle selects the second or third ridge
without changing the distance climbed. In CAD the cross-section sweeps along
each of those paths. The matching nut is cut with a slightly larger copy.

The unexpanded section uses these `(radius, axial offset)` points in millimetres:

| Point | Radius | Axial offset |
|---|---:|---:|
| 1 | 3.90 | -1.25 |
| 2 | 5.10 | -0.15 |
| 3 | 5.10 | +0.15 |
| 4 | 3.90 | +1.25 |

The core cylinder radius is 4.02 mm. The nominal crest diameter is therefore 10.20 mm; the core cylinder diameter is 8.04 mm. These are construction dimensions, not a certified ISO pitch diameter. The useful generated thread is clipped between source-coordinate Z = 34.0 and 75.6 mm. The upper journal/coupling interface is retained from the earlier working model.

The female cutting envelope is expanded by a nominal **0.20 mm radial clearance** with the generator's axial profile expansion. This is a designed clearance, not a measured print fit. P12/P26 each have a 13 x 13 x 7 mm external body. Replace **P13, P12 and P26 together** when changing lead.

[Geometry report](../engineering/evidence/thread_geometry_check.json) · [Portable FreeCAD rebuild macro](../engineering/source/rebuild_thread.FCMacro)

## 3. Why the original command was about 6,287 half-steps

Define:

- `x`: carriage travel in mm.
- `L`: screw lead in mm/revolution.
- `G`: additional reduction, **motor geared-output revolutions per screw revolution**. `G=1` means direct coupling.
- `S`: command steps per revolution of the motor's already-geared output shaft.

Then

$$N_s=x/L,\qquad N_m=Gx/L,\qquad N_{steps}=S Gx/L.$$

The project assumes nominal `S_half = 4096` or `S_full = 2048`. A nominal 5.625-degree/64 motor specification leads to this half-step count. The exact gearbox and motor variant must be calibrated; the 12 V winding version is a separate selection from the step-mode assumption. [Motor vendor datasheet](https://www.gentiam.com/wp-content/uploads/2022/09/GentiamElectronics-28BYJ-48-Stepper-Motor-Datasheet-Rev20220925-final.pdf).

For `x = 15.348483958 mm`, `L = 10 mm/rev`, `G=1`:

- Screw: **1.534848396 revolutions** = **552.5454225 degrees**.
- Motor geared output: **1.534848396 revolutions**.
- Internal rotor, assuming a nominal 64:1 gearbox: **98.2302973 revolutions**.
- Half-step command: **6286.739**, rounded to **6287**.
- Full-step command: **3143.370**, nearest integer **3143**.

**Do not multiply by the internal 64:1 gearbox a second time.** It is already included in 4096/2048.

## 4. Additional reduction

| Additional reduction G | Motor output turns | Ideal half-steps | Ideal full steps |
|---:|---:|---:|---:|
| 1 | 1.53485 | 6286.74 | 3143.37 |
| 2 | 3.06970 | 12573.48 | 6286.74 |
| 4 | 6.13939 | 25146.96 | 12573.48 |
| 8 | 12.27879 | 50293.91 | 25146.96 |

The exhibition firmware's historical `25148 full steps` equals `50296 half-step-equivalents`. It came from multiplying rounded earlier commands, not a measured gear ratio. At `G=1` it commands **122.79296875 mm** with a 10 mm lead. At `G=8` it commands **15.349121094 mm**. The actual additional reduction was not provided, so this setting must not be treated as calibrated direct-drive travel.

```sh
python3 engineering/calculations.py --reduction 8 --mode full --rate 120
```

## 5. Speed and time

For command frequency `f` in steps/second:

$$n_m=f/S\quad[rev/s],\qquad v=Lf/(SG)\quad[mm/s],\qquad t\approx N_{steps}/f.$$

The baseline 6287 half-steps at 180 half-steps/s takes approximately 34.93 seconds at constant rate, about 36 seconds including its ramp. The long 25148-full-step command at 120 full steps/s takes 209.57 seconds at constant rate, approximately 212 seconds including the nominal ramp. Full steps and half-steps must not be compared as identical units.

An additional reduction increases available screw torque while reducing screw speed. It does **not** create power. For gearbox efficiency `eta_g`, screw torque is approximately `T_s = eta_g G T_m` and screw speed is `n_s = n_m/G`.

## 6. Force and the 6-to-10 mm design trade-off

From energy per revolution:

$$2\pi T_s\eta_s=F L_m,\qquad F=\frac{2\pi\eta_s T_s}{L_m},$$

where `L_m` is lead in **metres**, torque is in N m, and force is in N. Equivalently, with lead in millimetres:

$$T_s[Nm]=\frac{F[N]L[mm]}{2000\pi\eta_s}.$$

At equal rotational speed, changing lead from 6 to 10 mm increases ideal linear speed by `10/6 = 1.667`. For the same stroke, ideal time becomes `6/10 = 0.60`; ideal force at equal torque and efficiency also becomes `0.60`. The larger lead was selected for travel speed, not for a torque increase.

An **illustrative**, unmeasured example: `T_s=0.020 N m`, `eta_s=0.30`, `L=10 mm` gives `F=3.77 N`. Do not use this example as a motor or printed-thread load rating. [Thomson screw catalogue](https://www.thomsonlinear.com/downloads/screws/Precision_Screws_ctuk.pdf).

## 7. Lead angle, friction and retention

$$\tan\lambda=L/(\pi d_m).$$

The effective pitch diameter `d_m` has not been certified for this custom swept profile. Do not substitute the crest diameter silently. For an illustrative `d_m=9 mm`, `lambda` is about 19.5 degrees. Self-locking depends on friction and flank geometry; the printed transmission is not established as self-locking. The uniform two-coil command during the short reversal pause is electrical holding, not mechanical braking or a load rating.
