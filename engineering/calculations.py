#!/usr/bin/env python3
"""SolarSkin kinematics and screw-drive sizing. Standard library only."""
from pathlib import Path
import argparse,csv,json,math
ROOT=Path(__file__).resolve().parents[1]
LEAD_MM=10.0;STARTS=3;ARM_MM=12.0;LINK_MM=20.0
NOMINAL_HALFSTEPS_PER_OUTPUT_REV=4096
NOMINAL_FULLSTEPS_PER_OUTPUT_REV=2048
NOMINAL_INTERNAL_REDUCTION=64

def carriage_z(angle_deg):
 a=math.radians(angle_deg)
 return ARM_MM*math.sin(a)+math.sqrt(LINK_MM**2-ARM_MM**2*math.cos(a)**2)

def derivative_mm_per_radian(angle_deg):
 a=math.radians(angle_deg)
 return ARM_MM*math.cos(a)+ARM_MM**2*math.sin(a)*math.cos(a)/math.sqrt(LINK_MM**2-ARM_MM**2*math.cos(a)**2)

def size_drive(stroke_mm,reduction=1.0,mode='half',rate=None):
 if stroke_mm<=0 or reduction<=0 or mode not in {'half','full'}:raise ValueError('Positive stroke/reduction and half/full mode required.')
 resolution=NOMINAL_HALFSTEPS_PER_OUTPUT_REV if mode=='half' else NOMINAL_FULLSTEPS_PER_OUTPUT_REV
 rate=rate or (180 if mode=='half' else 120)
 if rate<=0:raise ValueError('Rate must be positive.')
 screw_revs=stroke_mm/LEAD_MM;output_revs=screw_revs*reduction;ideal_steps=output_revs*resolution
 return {'stroke_mm':stroke_mm,'extra_reduction':reduction,'step_mode':mode,'nominal_steps_per_output_rev':resolution,'screw_revolutions':screw_revs,'geared_motor_output_revolutions':output_revs,'internal_rotor_revolutions_nominal':output_revs*NOMINAL_INTERNAL_REDUCTION,'ideal_step_count':ideal_steps,'nearest_integer_steps':math.floor(ideal_steps+.5),'rate_steps_per_second':rate,'constant_rate_time_s':ideal_steps/rate,'linear_speed_mm_per_second':LEAD_MM*rate/(resolution*reduction)}

def thrust_N(screw_torque_Nm,efficiency,lead_mm=LEAD_MM):
 if screw_torque_Nm<0 or not 0<efficiency<=1 or lead_mm<=0:raise ValueError('Invalid torque, efficiency or lead.')
 return 2*math.pi*efficiency*screw_torque_Nm/(lead_mm/1000)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--reduction',type=float,default=1);ap.add_argument('--mode',choices=['half','full'],default='half');ap.add_argument('--rate',type=float);ap.add_argument('--export',action='store_true');args=ap.parse_args()
 stroke=carriage_z(75)-carriage_z(0);result=size_drive(stroke,args.reduction,args.mode,args.rate)
 result['thread_pitch_mm']=LEAD_MM/STARTS;result['assumption']='4096 halfsteps or 2048 full steps per geared output revolution; nominal, not measured. Extra reduction is downstream of that output.'
 print(json.dumps(result,indent=2))
 if args.export:
  dest=ROOT/'engineering/results';dest.mkdir(exist_ok=True)
  (dest/'baseline.json').write_text(json.dumps(result,indent=2)+'\n')
  with (dest/'reduction_table.csv').open('w',newline='') as f:
   rows=[size_drive(stroke,g,m) for g in [1,2,4,8] for m in ['half','full']];w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
  with (dest/'kinematic_samples.csv').open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['wing_angle_deg','carriage_z_mm','travel_from_closed_mm','dz_dtheta_mm_per_rad','screw_turns_from_closed'])
   for angle in range(76):
    z=carriage_z(angle);w.writerow([angle,z,z-carriage_z(0),derivative_mm_per_radian(angle),(z-carriage_z(0))/LEAD_MM])
if __name__=='__main__':main()
