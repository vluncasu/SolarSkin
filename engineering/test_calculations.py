import json,math,unittest
from calculations import *
class Kinematics(unittest.TestCase):
 def test_source_cad_samples(self):
  rows=json.loads((ROOT/'engineering/evidence/cad_stroke_samples.json').read_text())
  for r in rows['positions']:
   offset=carriage_z(r['wing_deg'])-carriage_z(75)
   self.assertAlmostEqual(offset,r['travel_mm'],places=10)
   self.assertAlmostEqual(-offset/LEAD_MM*360,r['screw_rotation_deg'],places=9)
 def test_link_closure(self):
  for a in range(76):
   t=math.radians(a);self.assertAlmostEqual((12*math.cos(t))**2+(carriage_z(a)-12*math.sin(t))**2,400,places=10)
 def test_derivative(self):
  for a in range(1,75):
   delta=1e-5;finite=(carriage_z(a+math.degrees(delta))-carriage_z(a-math.degrees(delta)))/(2*delta)
   self.assertAlmostEqual(finite,derivative_mm_per_radian(a),places=7)
 def test_nominal_motor_counts(self):
  stroke=carriage_z(75)-carriage_z(0);a=size_drive(stroke);b=size_drive(stroke,8);c=size_drive(stroke,1,'full')
  self.assertEqual(a['nearest_integer_steps'],6287);self.assertAlmostEqual(b['ideal_step_count'],a['ideal_step_count']*8);self.assertAlmostEqual(c['ideal_step_count']*2,a['ideal_step_count'])
 def test_force_units(self):self.assertAlmostEqual(thrust_N(.02,.3),3.7699111843,places=8)
 def test_invalid_inputs(self):
  for args in [(0,1),(-1,1),(1,0)]:
   with self.assertRaises(ValueError):size_drive(*args)
if __name__=='__main__':unittest.main()
