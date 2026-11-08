from pathlib import Path
import json,csv,collections
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image

stages={
'module':[
('Guides and carriage','P04, three P09 guides, P10','Fit the three D-profile guides in the matching hub sockets. Slide the carriage onto all three together. The flat faces locate the carriage angularly.','Run the bare carriage along the guides by hand. Correct a burr or a misaligned guide before adding the screw.'),
('Matched nuts and cover','P12, P26, P11 and two P29 screws','Test both nuts on P13. Place them in their lower and upper carriage pockets. Seat P11 and tighten the two cover screws alternately. Excess clamping pressure can bind the nut pair.','Rotate the screw through the assembled nuts by hand. Both nuts must follow the same three-start, 10 mm-lead profile.'),
('Insert the lead screw','P02 and P13','With the motor off the rear frame, bring P13 through the lateral opening. Keep the shaft parallel to its final axis, then seat its shoulder at the bearing. Lower this pair onto the guides and turn the screw into the nuts.','Observe the carriage while turning P13. One turn advances it 10 mm where enough free stroke remains. Keep the carriage aligned on the guides.'),
('Pillars, bushings and driver tray','Three P05; two P33/P34 pairs; P36/P37; E01','Fit the two short bushing and cone pairs to the ordinary pillar sectors. At the tray, use the longer P36 bushing from below and P37 cone from above. Install the tray before closing the driver enclosure.','Compare the two short stacks with the longer tray stack. All three pillars should seat without bowing the guides.'),
('Leaves, axles and link rods','Three left and three right P07 leaves; three P08 axles; six P16 rods; twelve P32 nuts','Pair one left and one right leaf at each sector. Insert P08 from the outside and engage its terminal thread in the hub. Attach each rod between a leaf and the carriage. Retain each end with a P32 nut.','Move all six joints by hand. The rod must pivot at both ends. A tight nut that clamps the joint will make the motor lose steps.'),
('Drive, wiring and receiver','Two P30/P03/P31 stacks; E02 and three E03; P44, P45 and P46','Align the geared motor output with P13, then fit the clamps. Seat the driver, route the cable and close E02. Thread P44 into the rear frame, slide on the D-profile P45 receiver, and insert the transverse P46.','Support the module by the body. Check the rod sweep, cable clearance and receiver alignment before attaching it to its chosen support.')],
}
common=[
('Base and first floor','J03 fit coupon; A01 bays 1, 2 and 3; J01 floor keys','Test the printed joint with J03. Lay out the three floor bays in their CAD order. The central stair opening sets the orientation of the middle bay. Seat the floor on the base and install its mating keys.','Use a flat surface. A stepped seam or a floor that rocks prevents the next level from seating.'),
('First occupied level','A02 rear frames, S01 lower stair flight and S02 upper flight','Locate the rear frames in the floor sockets. Assemble the two stair flights in the central opening. Build the sides and first interior while the space above the floor remains accessible.','Look down through the opening. The landing must meet the next floor and the stair must clear the adjacent room.'),
('Intermediate floors','A01 bays at each level; ordinary rear and side frames; stair flights','Repeat the three-bay floor stack. The CAD floor origins rise from 18.0 to 170.1, 322.2 and 474.3 mm. Assemble each occupied storey before covering it.','Use the three equal 152.1 mm level intervals to identify ordinary storeys. They are assembly-origin differences, not dimensions to add to individual STL parts.'),
('Upper storey and roof','Tall rear and side elements; A01 roof bays; T02 roof hatch','Use the tall frame parts at N4. The last floor-to-roof interval is 223.7 mm. Keep the service opening accessible when placing the three roof bays and the hatch.','Check the roof origin at Z = 698.0 mm in the scene. The hatch must remain accessible after fitting the cable channels.'),
('Front structure and receivers','Use the receiver hardware specified for this exact route.','Build three facade columns across four levels on a flat surface. Keep the module positions in front-view order: M01 to M04 at the top, M13 to M16 at the bottom. Columns 2 and 4 are rotated 180 degrees in the saved layouts.','Test one receiver and check tool access from behind it. Support the module body while fitting it. Repeat only after the first mount allows the required leaf travel.'),
('Roof equipment and cabling','E02 enclosure, E03 lid, two E04 clamps, E05/E06 control enclosure, E07 channels and E08 covers','Check the actual boards and source against the mounting geometry. Place the housings before routing cables. Route low-voltage leads to the drivers, leave service loops and fit the channel covers last.','With motor power off, move the leaves through their travel and remove one service cover. The cable should neither pull on its connector nor enter the linkage sweep.')]
for route in ['furnished','simplified']:
 st=[list(x) for x in common]
 if route=='furnished':
  st[0][1]+='; three B03 rear bases and three B04 fan bases'
  st[1][2]+=' Fit the two I01 reception units at N1 and locate each with an I02 two-pin bar from above. Fit the A05/A06 side panels by their matching CAD positions.'
  st[2][2]+=' Place the four workshop units across N2 and N3. Install the stair guards I03 and separate S03 rails while accessible.'
  st[3][2]+=' Fit both meeting-area units at N4 and use the tall A07 fin panels.'
  st[4][1]='Twelve F04 cassettes; six F05, two F06 and nine F07 splice keys; 32 F01 bolts and 16 F02 locking bars'
  st[4][2]+=' Match each C1-C3 and N1-N4 cassette. Join the vertical edges with F05/F06 and horizontal edges with F07 as shown in the scene. Each receiver takes two bolts and one locking bar.'
 else:
  st[0][1]+='; three each of B01, B02 and B03'
  st[1][2]+=' Fit V01 rear glazing into the A02 frames and V02 side glazing into A03 frames. The rapid lot omits the optional desk islands visible in the assembly reference.'
  st[2][2]+=' Keep glazing flat until installation. Match each ordinary pane to its own frame before stacking the next floor.'
  st[3][2]+=' Pair the tall V01/V02 panes with the tall A02/A03 frames. Check the stair opening before seating the roof.'
  st[4][1]='Twelve A04 load-bearing panels and 32 J02 D8 receiver screws'
  st[4][2]+=' Match each panel number and N1-N4 level to the rapid Blender scene. This route uses two J02 D8 screws per module. Keep these screws separate from the F01/F02 system on the furnished building and stand.'
 stages[route]=st
titles={'module':'One kinetic module','furnished':'Furnished office','simplified':'Simplified office'}
titles['stand']='Independent reinforced stand'
stages['stand']=[
('Lay out the cassettes','Twelve F04 cassettes, engraved 25 to 36','View the frame from the rear. Arrange the top row as 28, 32, 36. Continue down with 27, 31, 35 then 26, 30, 34. Finish with 25, 29, 33 at the base. Align the cassette seams on a flat surface before installing the matching splices.','Check each engraved ID. The twelve cassettes together support sixteen module receivers.'),
('Join the side ribs','Four R01, four R02, six R04 plates and 24 R21 splice bolts','Use the four right ribs on the right and the four left ribs on the left. Position the six splice plates across the rib joints, four R21 bolts to a plate. Start all four before tightening the plate.','The rib joints should seat evenly. Reserve the other two R21 bolts for the rear adapter.'),
('Attach the front clamps','Sixteen R03 clamps and 32 R05 bolts','Fit the clamps at the frame-to-rib interfaces shown in scene 03. Use two R05 bolts for each clamp. Support the frame while aligning the ribs.','Check access to every receiver and look along the frame for twist. Reserve two R05 bolts for the rear foot.'),
('Stiffen the feet','Two R22 supports, two R23 supports, four R24 saddles and eight R25 screws','R22 fits the original left and middle F13 feet. R23 fits the original right F18 and the extra rear F18. Secure each sole with one saddle and two long R25 screws.','Place all four supported feet on the table. The nominal raise is 18 mm. Check seating before final tightening.'),
('Fit the rear adapter','R31, extra F18 foot, two R05 and two R21','Rotate the extra foot in plan so that it extends behind the stand. Place R31 against its upright. The two R05 screws engage the foot at nominal heights of 34 and 60 mm. Use two R21 screws to attach the adapter to the lower right rib.','Check that the rear sole extends the support footprint and that the original feet remain seated.'),
('Mount the mechanisms','Two F01 bolts and one F02 bar per occupied receiver; F17 long key','Work from the bottom up, alternating sides. Place F02 behind the cassette with its bushings toward P45. Start both flattened-head F01 bolts from the front. Align the heads with their recesses and tighten alternately. Fit an R41 cable clip where needed and leave a free cable loop.','With the motors unpowered, turn each mechanism through its free range. Check adjacent leaves, bolt heads, loose cables and the stance of the loaded frame.')]
pdf=Canvas('docs/pdf/SOLARSKIN_WORKSHOP_SEQUENCE.pdf',pagesize=A4);pdf.setTitle('SolarSkin | Workshop assembly sequence')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16)
for route,items in stages.items():
 lines=['# '+titles[route]+' - assembly sequence','','Orange identifies the group being discussed. Blue-grey gives the installed context. Views show final part positions. Fit each storey while it is open.','']
 for i,(name,parts,action,check) in enumerate(items):
  pic=f'media/atlas/{route}-stage-{i}.webp'
  if route=='stand':pic='media/renders/'+['frame_assembly','frame_vertical_splices','front_clamp_detail','base_assembly','assembly_08','assembly_05'][i]+'.webp'
  lines += [f'## {i+1}. {name}','',f'![{name}](../{pic})','',parts+'.','',action,'','**Check before continuing.** '+check,'']
  pdf.setFont('Helvetica-Bold',19);pdf.drawString(38,797,f'{i+1}. {name}');pdf.setFont('Helvetica',10);pdf.drawString(38,819,titles[route])
  pdf.drawImage(ImageReader(pic),40,379,510,391,preserveAspectRatio=True,anchor='c')
  y=361
  for label,value in [('Parts',parts),('Assembly',action),('Check',check)]:
   para=Paragraph(f'<b>{label}.</b> '+value,style);_,h=para.wrap(510,300);y-=h;para.drawOn(pdf,40,y);y-=18
  assert y>28
  pdf.showPage()
 if route=='stand':lines[2]='Use the rear-view cassette map first. The CAD illustrations use different viewing directions; keep the engraved IDs visible when working.'
 Path('docs/'+route+'_workshop.md').write_text('\n'.join(lines)+'\n')
pdf.save()
