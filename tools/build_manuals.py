from pathlib import Path
import math,json,csv,textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/pdf';OUT.mkdir(parents=True,exist_ok=True)
MEDIA=ROOT/'media/renders';PLOTS=ROOT/'media/engineering';PLOTS.mkdir(parents=True,exist_ok=True)
fonts = [(Path('/System/Library/Fonts/Supplemental/Arial.ttf'), Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf')), (Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))]
regular, bold = next((a,b) for a,b in fonts if a.exists() and b.exists())
pdfmetrics.registerFont(TTFont('Body',str(regular)));pdfmetrics.registerFont(TTFont('Bold',str(bold)))
W,H=595.276,841.89;INK=HexColor('#162b40');BLUE=HexColor('#0765a7');ORANGE=HexColor('#e76d25');GRAY=HexColor('#546574');PALE=HexColor('#f3f6f9');LINE=HexColor('#dce4eb')
STYLE=ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=15,textColor=INK)
def z(a):
 t=math.radians(a);return 12*math.sin(t)+math.sqrt(400-144*math.cos(t)**2)
angles=list(range(76));stroke=[z(a)-16 for a in angles]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#162b40','xtick.color':'#546574','ytick.color':'#546574'})
fig,ax=plt.subplots(figsize=(7.4,3.3));ax.plot(angles,stroke,color='#0765a7',lw=2.7);ax.scatter([0,75],[0,stroke[-1]],color='#e76d25',s=30,zorder=3);ax.set(xlabel='Wing angle (degrees)',ylabel='Carriage travel from closed (mm)',xlim=(0,75));ax.grid(alpha=.18);fig.tight_layout();fig.savefig(PLOTS/'carriage_travel.png',dpi=220);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.4,3.3));r=12;l=20;t=math.radians(40);B=(r*math.cos(t),r*math.sin(t));A=(0,z(40));ax.plot([0,B[0]],[0,B[1]],color='#e76d25',lw=4,label='Wing attachment radius r = 12 mm');ax.plot([B[0],A[0]],[B[1],A[1]],color='#0765a7',lw=4,label='Connecting rod l = 20 mm');ax.plot([0,0],[-2,35],color='#8498a9',ls='--');ax.scatter([0,B[0],0],[0,B[1],A[1]],color='#162b40',s=30);ax.text(.7,-1,'Wing pivot');ax.text(B[0]+.7,B[1],'B');ax.text(.7,A[1],'A: carriage');ax.set(xlabel='In-plane lateral coordinate (mm)',ylabel='Axial coordinate z (mm)',xlim=(-2,22),ylim=(-3,36));ax.set_aspect('equal');ax.legend(loc='upper right',fontsize=8,frameon=False,bbox_to_anchor=(1.7,1));fig.tight_layout();fig.savefig(PLOTS/'linkage_geometry.png',dpi=220,bbox_inches='tight');plt.close(fig)
class Manual:
 def __init__(self,file,title):self.c=canvas.Canvas(str(file),pagesize=(W,H));self.c.setTitle(title);self.c.setAuthor('SolarSkin project');self.page=0;self.title=title
 def new(self,title,kicker='ENGINEERING AND ASSEMBLY'):
  if self.page:self.c.showPage()
  self.page+=1;c=self.c;c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(BLUE);c.rect(0,H-8,W,8,fill=1,stroke=0)
  c.setFont('Bold',9);c.setFillColor(BLUE);c.drawString(40,H-42,'SOLARSKIN');c.setFont('Body',8);c.setFillColor(GRAY);c.drawRightString(W-40,H-42,kicker)
  size=min(25,515/max(1,pdfmetrics.stringWidth(title.replace('\n',' '),'Bold',1)));self.text(title.replace('\n','<br/>'),40,H-70,515,size,size*1.2,bold=True)
  c.setStrokeColor(LINE);c.line(40,38,W-40,38);c.setFont('Body',8);c.setFillColor(GRAY);c.drawString(40,24,'10 mm lead / three starts / 08 November 2026');c.drawRightString(W-40,24,f'{self.page:02}')
 def text(self,s,x,y,w=515,size=10.2,leading=None,bold=False):
  st=ParagraphStyle('p',parent=STYLE,fontName='Bold' if bold else 'Body',fontSize=size,leading=leading or size*1.45)
  p=Paragraph(s,st);_,h=p.wrap(w,1000)
  if y-h<47:raise RuntimeError(f'Page {self.page} text overflow: {s[:60]}')
  p.drawOn(self.c,x,y-h);return y-h
 def image(self,file,x,y,w,h):
  p=Path(file);p=p if p.is_absolute() else MEDIA/p
  if not p.exists() and p.suffix == '.png': p=p.with_suffix('.webp')
  if not p.exists():raise FileNotFoundError(p)
  self.c.drawImage(str(p),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
 def table(self,rows,widths,x,y,size=9):
  data=[[Paragraph(str(v),ParagraphStyle('cell',parent=STYLE,fontSize=size,leading=size*1.3)) for v in row] for row in rows]
  t=Table(data,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.8,BLUE),('LINEBELOW',(0,1),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));_,h=t.wrap(sum(widths),1000)
  if y-h<47:raise RuntimeError(f'Page {self.page} table overflow')
  t.drawOn(self.c,x,y-h);return y-h
 def save(self):self.c.save()
m=Manual(OUT/'SOLARSKIN_ENGINEERING_AND_ASSEMBLY.pdf','SolarSkin - Engineering and Assembly')
m.new('SolarSkin / Kinetic office facade','BUILDING AND MECHANISM')
m.image('furnished_open.webp',40,190,515,510)
m.text('The furnished office places sixteen six-leaf modules in front of eight interior units and a central stair. Each unit is installed before the next floor closes access to its two-pin locating bar.',40,174)
m.text('Editable assembly: cad/furnished/OFFICE_16.blend. Manufacturing lot: print/furnished/.',40,100,size=9)
m.new('The simplified office','ARCHITECTURAL COMPARISON')
m.image('simplified_open.webp',40,395,250,300)
m.image('simplified_floor_print.webp',305,395,250,300)
m.text('The rapid lot retains the building and stair, with optional furniture omitted. It contains 158 new pieces on 63 beds. The furnished office contains 193 new pieces on 46 beds. Both inventories assume sixteen existing mechanisms.',40,370)
m.text('Print the rapid floor slabs on edge with the specified 5 mm outer brim. Remove the two sacrificial ribs at the stair opening after printing. Check a representative bridge before repeating the floors.',40,235)
m.text('Editable assembly: cad/simplified/OFFICE_16.blend. Manufacturing lot: print/simplified/.',40,115,size=9)
m.new('The independent stand','STRUCTURE AND CONTROL')
m.image('assembly_03.webp',40,375,515,320)
m.text('The reinforced stand exposes the receivers, joints and motor cables. Open scene 03 for the frame, then scenes 04 to 06 for a module connection. The rear foot extends the support footprint. Actual stability depends on the mass and position of the installed modules.',40,340)
m.text('The frame has sixteen nominal positions. Seven shift registers provide fourteen motor channels. The comparative study explains how geometric capacity, printed quantities and electrical capacity were determined: docs/12_building_and_facade.md.',40,200)
m.new('Mechanism and reinforced stand','TECHNICAL MANUAL')
m.image('assembly_01.png',40,205,515,500)
m.text('A three-start printed lead screw drives a guided carriage and six linked leaves. This manual covers the 10 mm-lead mechanism, the reinforced frame and the 7-register / 14-channel controller.',40,192)
m.table([['MECHANISM','FRAME','CONTROLLER'],['28 types / 62 prints','16 nominal positions','7 registers / 14 channels']],[172,172,171],40,105,8.5)
m.new('Design map and document index')
m.table([['SECTION','CONTENT'],['06-10','Kinematics, thread construction, motor turns, reduction and force'],['11-15','Mechanism assembly: guides, screw, wings, motor and receiver'],['16-20','Frame, side reinforcement, feet and module attachment'],['21-23','Electronics, firmware and calibration'],['24-25','Printing, verification and source references']],[95,420],40,730)
m.text('<b>One module:</b> 3 mirrored wing pairs, 3 radial axles, 6 rods and 12 joint nuts. The 62 printed pieces do not include the motor, driver or common assembly tools.',40,480)
m.text('<b>Frame versus electronics:</b> the CAD has 16 receiver positions. Seven 74HC595 registers provide 14 motor channels. A picture with 16 modules is not proof of 16 electrically active motors.',40,406)
m.text('<b>CAD:</b> use the numbered scenes in REINFORCED_16_MODULE_ASSEMBLY.blend. Scene 03 is the frame; 04-06 show the module mount; 08-10 show feet and rib connections. Exploded offsets show order, not certified insertion paths.',40,332)
m.text('<b>Parts identification:</b> the separate parts catalogue has six parts per A4 sheet, two views per part, per-module quantities and bounding-box dimensions. The CSV BOM is the machine-readable quantity reference.',40,240)
m.text('<b>Revision rule:</b> install P13/P12/P26 from the same 10 mm-lead family. Use F01/F02 for the current receiver mounting, not the older 20-module rail system.',40,150)
m.new('01 / Link geometry and carriage travel')
m.image(PLOTS/'linkage_geometry.png',40,425,515,280)
m.text('The source places the wing attachment at radius r = 12 mm and uses a 20 mm connecting rod. In each wing plane the carriage joint A is constrained to the axial line; joint B follows the wing.',40,410)
m.text('<b>Rod constraint</b><br/>(r cos theta)<super>2</super> + (z - r sin theta)<super>2</super> = l<super>2</super><br/><br/><b>CAD branch</b><br/>z(theta) = r sin theta + sqrt(l<super>2</super> - r<super>2</super> cos<super>2</super> theta)',40,330,size=12)
m.table([['ANGLE','CARRIAGE z','TRAVEL FROM CLOSED'],['0 degrees','16.000000 mm','0.000000 mm'],['75 degrees','31.348484 mm','15.348484 mm']],[140,180,195],40,170)
m.new('02 / Nonlinear motion and leverage')
m.image(PLOTS/'carriage_travel.png',40,445,515,260)
m.text('Equal wing-angle increments do not require equal carriage movement. The analytic curve reproduces all nine positions in the saved final CAD stroke report.',40,425)
m.text('<b>Derivative, theta in radians</b><br/>dz/dtheta = r cos theta + r<super>2</super> sin theta cos theta / sqrt(l<super>2</super> - r<super>2</super> cos<super>2</super> theta)',40,345,size=11.5)
m.text('<b>Virtual work for six equal resisting wing torques</b><br/>F<sub>c</sub> dz = 6 tau<sub>w</sub> dtheta<br/>tau<sub>w</sub> = (F<sub>c</sub> / 6) (dz/dtheta)',40,250,size=12)
m.text('Convert mm/radian to m/radian to obtain N m from force in newtons. This relation neglects joint friction, uneven loads, printed compliance and backlash. It is not a measured torque rating.',40,150)
m.new('03 / Three-start thread construction')
m.image('lead_screw_10mm.png',40,420,515,290)
m.text('<b>Lead L = starts n x axial pitch p</b><br/>10 mm/rev = 3 x 3.333333 mm<br/>Start spacing = 360/3 = 120 degrees',40,410,size=13)
m.table([['CONSTRUCTION PARAMETER','VALUE'],['Core cylinder diameter','8.04 mm'],['Nominal crest diameter','10.20 mm'],['Section radius / axial coordinates','(3.90,-1.25), (5.10,-0.15), (5.10,+0.15), (3.90,+1.25) mm'],['Female envelope expansion','0.20 mm nominal radial clearance'],['Split-nut external body','13 x 13 x 7 mm, each'],['Matched parts','P13 screw + P12 lower nut + P26 upper nut']],[225,290],40,300,8.8)
m.text('The custom swept profile is not an ISO thread. Its crest diameter must not be used silently as a certified pitch diameter. The upper coupling/journal interface is retained from the earlier model.',40,100,size=9)
m.new('04 / Motor rotations, steps and reduction')
m.text('<b>Three different rotations must be distinguished:</b> the internal motor rotor, its already-geared output shaft, and the lead screw after any additional reduction.',40,730)
m.text('N<sub>screw</sub> = x/L<br/>N<sub>motor output</sub> = G x/L<br/>N<sub>steps</sub> = S G x/L',40,650,size=16)
m.text('G means motor geared-output revolutions per screw revolution. The nominal step resolution S is 4096 half-steps or 2048 full steps per geared-output revolution. Do not multiply the internal nominal 64:1 gearbox into S again.',40,545)
m.table([['EXTRA G','OUTPUT TURNS','HALF-STEPS','FULL STEPS'],['1','1.534848','6286.739','3143.370'],['2','3.069697','12573.478','6286.739'],['4','6.139394','25146.956','12573.478'],['8','12.278787','50293.912','25146.956']],[90,140,145,140],40,445)
m.text('<b>Why 6287?</b> At the CAD stroke of 15.348484 mm, a direct 10 mm-lead drive needs 1.534848 screw turns = 552.545423 degrees. At nominal S = 4096, that is 6286.739 half-steps, rounded to 6287. The internal rotor makes about 98.2303 turns at nominal 64:1.',40,220)
m.text('<b>Long-demo setting:</b> 25148 full steps = 50296 half-step equivalents. It commands 122.793 mm at G=1, or 15.3491 mm at G=8. The actual additional reduction has not been recorded: calibrate it before using that command.',40,120)
m.new('05 / Speed, time and force')
m.text('v = L f / (S G) [mm/s]<br/>t approximately N<sub>steps</sub> / f [s]<br/>T<sub>screw</sub> = eta<sub>g</sub> G T<sub>motor output</sub>',40,730,size=14)
m.table([['COMMAND','CONSTANT-RATE TIME','WITH NOMINAL RAMP'],['6287 half-steps at 180/s','34.93 s','about 36 s'],['25148 full steps at 120/s','209.57 s','about 212 s']],[245,135,135],40,595,9)
m.text('<b>Rotary-to-linear energy</b><br/>2 pi T<sub>screw</sub> eta<sub>s</sub> = F L<sub>metres</sub><br/>F = 2 pi eta<sub>s</sub> T<sub>screw</sub> / L<sub>metres</sub>',40,460,size=14)
m.text('Illustrative values only: torque 0.020 N m, screw efficiency 0.30 and lead 10 mm give 3.77 N. No motor torque or printed-thread load rating was measured to establish that example as a design limit.',40,350)
m.text('<b>Why change 6 mm lead to 10 mm?</b><br/>At equal rotational speed: linear speed x1.667; stroke time x0.60; ideal axial force at equal torque and efficiency x0.60. The change was a travel-speed trade-off, not a motor-torque increase.',40,250)
m.text('Lead angle: tan lambda = L / (pi d<sub>m</sub>). Effective pitch diameter and friction are not certified for this custom profile. Self-locking is not established. Additional reduction trades speed for torque; it does not create power.',40,140)
# Assembly pages: fixed layouts prevent orphan headings and oversized images.
def assembly_page(title,parts,image,steps,note=''):
 m.new(title);m.text(parts,40,733,size=10,bold=True)
 m.image(image,40,365,515,345)
 y=350
 for i,s in enumerate(steps,1):y=m.text(f'<b>{i:02}</b>  '+s,40,y,size=10.2)-12
 if note:m.text(note,40,min(y-5,105),size=9)
assembly_page('06 / Guides, carriage and split nuts','P04 x1 / P09 x3 / P10 x1 / P12 x1 / P26 x1 / P11 x1 / P29 x2','mechanism_10mm.png',[
 'Align the three D-profile guides with the matching hub sockets. Fit them and slide the carriage over them; it must translate freely without forced rotation.',
 'Test each split nut on the 10 mm-lead screw by hand. Seat P12 and P26 in their matching carriage pockets.',
 'Fit P11 and tighten the two P29 alternately. Do not force the nuts together axially to correct a misalignment.'
],'Use only the matched P13/P12/P26 transmission family.')
assembly_page('07 / Lateral screw insertion','P02 rear frame / P13 lead screw','screw_insertion_01.png',[
 'Leave the motor, clamps and large frame connector off P02 while inserting the screw.',
 'Keep P13 parallel to its final axis. Enter through the side opening opposite the large connector.',
 'Slide toward the bearing without changing shoulder height. Move inward until the coupling shoulder seats.'
],'The original source validates this lateral approach digitally; physical fit still depends on the print.')
assembly_page('08 / Seat the frame and fit the pillars','P05 x3 / P33-P34 x2 / P36-P37 x1 / E01 x1','screw_insertion_03.png',[
 'Lower the P02/P13 subassembly onto the guides and turn the screw into the nuts by hand. Do not twist the carriage to force the engagement.',
 'Install the three pillars and the driver tray. At the tray sector, P37 enters from above; the longer P36 comes from below.',
 'Complete the tray-side fastening through its access opening before installing the driver board and cover. The other sectors use the short pairs.'
])
assembly_page('09 / Wings, axles and connecting rods','P07L x3 / P07R x3 / P08 x3 / P16 x6 / P32 x12','mechanism_10mm.png',[
 'Align each left/right wing pair with its pillar and hub. Insert the axle from outside, through the pillar and leaves, then engage its terminal thread in the hub.',
 'Seat the recessed round/slotted axle head by hand. Do not clamp the wing bearing solid.',
 'Fit one connecting rod to each leaf. Every rod receives two joint nuts. Confirm that all six rods articulate freely after tightening.'
],'Original axle: 85 mm overall; wing-bearing diameter 5.13 mm; terminal thread diameter 4 mm, pitch 1.2 mm, length 6 mm.')
assembly_page('10 / Motor, driver and receiver','P30 x2 / P03 x2 / P31 x2 / E02 x1 / E03 x3 / P44-P45-P46','mechanism_10mm.png',[
 'Use the motor fastening stack: screw, clamp, then locknut. Engage the clamp pin in the motor ear and align the motor shaft with the screw socket.',
 'Place the driver and cable before fitting E02. Keep the cable away from moving parts; fit all three E03 cover screws.',
 'Seat P44 in the frame, slide P45 over the D-profile shank and install P46 transversely. Mount the receiver to the current stand with F01/F02.'
],'Do not substitute the old 20-module rail mounting bolts for the current F01/F02 system.')
assembly_page('11 / Assemble the structural cassettes','12 structural cassettes / matching rear splices / three original base segments','assembly_03.png',[
 'Build the cassette frame on a flat surface before adding mechanism weight. Preserve the engraved positions and handedness.',
 'Fit the matching rear splices and engage all fasteners before alternating tightening. Do not force alignment by over-tightening a single screw.',
 'The frame has 16 nominal mechanism positions. Its 12 structural cassettes are not a count of installed mechanisms.'
],'Rear cassette map, top to bottom: 28-32-36 / 27-31-35 / 26-30-34 / 25-29-33. Original feet: 64-64-69.')
assembly_page('12 / Side ribs and front clamps','R01 x4 / R02 x4 / R03 x16 / R04 x6','assembly_03.png',[
 'Fit the four right ribs and four left ribs. Do not mirror a threaded part.',
 'Join the segments with six R04 splices and 24 R21 screws. The nominal rib-segment joint is 0.4 mm.',
 'Install two R03 front clamps per rib segment, using 32 R05 screws. Reserve two additional R05 and two R21 for the rear-foot adapter.'
],'Complete reinforcement totals: 34 R05 at 15 mm overall length; 26 R21 at 18.8 mm. These are not F01 receiver bolts.')
assembly_page('13 / Four base supports and rear foot','R22 x2 / R23 x2 / R24 x4 / R25 x8 / R31 x1 / extra F18 x1','assembly_08.png',[
 'R22 supports the two original 64 feet. R23 supports the right 69 foot and the additional 69 foot at the rear: two R23 copies are required.',
 'Each foot uses one R24 saddle and two R25 screws, 61 mm overall. Seat all four supports before final tightening.',
 'Rotate the extra foot backward in plan, fit R31 with two R05, and connect the adapter to the lower R01 with two R21. Do not lift another sole from the table.'
],'All four base supports raise the supported feet nominally 18 mm. The rear foot is not a carrying handle.')
assembly_page('14 / Mount one mechanism to the frame','Per module: F01 x2 / F02 x1 / long key F17 (engraved 68)','assembly_05.png',[
 'Support the module body, not the wings. Place F02 behind the cassette with its bushings toward the receiver, initially leaving about 6 mm of rear access.',
 'Insert both flattened-head F01 bolts from the front beside P45. Bring the F02 bushings through the cassette into the receiver.',
 'Start both threads before alternating final tightening with the long key. Keep the mating stack free of cables. Work bottom-up, alternating sides.'
],'F01: 18.4 mm overall, custom diameter 5.8 / pitch 1.5 mm. For 16 modules: 32 bolts + 16 bars. For 12: 24 + 12.')
m.new('15 / Cable routing and structural rationale')
m.image('cable_clip_section.png',40,420,515,290)
m.text('Four optional R41 clips guide wires along available rear rib edges. Trial one clip first. Leave motion loops and provide actual strain relief; a cable guide is not strain relief. R41 replaces the older large R40 organizer.',40,405)
m.text('<b>Local bending:</b> I = b h<super>3</super>/12 and ideal cantilever deflection delta = F L<super>3</super>/(3 E I). Rib depth can improve local stiffness efficiently. These relations do not certify the complete printed frame.',40,300)
m.text('<b>Stability:</b> horizontal force at height H gives an overturning moment F H. Gravity restores through the actual centre of mass and contact polygon. The extra rear foot increases fore-aft support extent only when all soles remain seated.',40,205)
m.text('Check the first module, the full cable sweep, neighbouring wings and the footing contact before populating the frame. Keep the original frame and mechanism quantities separate.',40,110)
m.new('16 / Electrical connections')
m.table([['SIGNAL','ESP32 GPIO','74HC595 PHYSICAL PIN'],['DATA','23','14 on REG1 only'],['CLOCK','18','11 on all registers'],['LATCH','21','12 on all registers'],['OE, active LOW','22','13 on all registers'],['3V3','-','16 VCC and 10 SRCLR'],['Common GND','-','8']],[125,110,280],40,730)
m.text('<b>Cascade:</b> pin 9 NEXT/QH-prime of each register goes to pin 14 DATA/SER of the next. CLOCK and LATCH are common parallel buses. Never tie OE to both GPIO22 and ground.',40,430)
m.table([['OUTPUTS','PHYSICAL PINS','DRIVER INPUTS'],['Q0, Q1, Q2, Q3','15, 1, 2, 3','First motor IN1-IN4'],['Q4, Q5, Q6, Q7','4, 5, 6, 7','Second motor IN1-IN4']],[170,160,185],40,340)
m.text('REG1 = M01/M02; ...; REG7 = M13/M14. Each motor needs its own ULN2003 board. The 12 V supply feeds the 12 V motors/drivers, not ESP32 GPIO or logic VCC. ESP32 was USB-powered; logic and motor-driver grounds are common.',40,215)
m.text('The earlier 1.5 V report on 3V3 is unresolved in the recorded evidence. ESP32-WROOM-32 specifies 3.0-3.6 V operation. Do not treat a software counter as an electrical measurement.',40,115,size=9)
m.new('17 / Firmware and autonomous operation')
m.table([['VARIANT','DEFAULT MOTION'],['stand','25,148 full steps/sense; maximum 120 full steps/s; 0.3 s reversal pause'],['baseline_web','6,287 half-steps/sense; maximum 180 half-steps/s; 1 s pause'],['minimal','Same simple half-step cycle without networking']],[130,385],40,730)
m.text('<b>State sequence</b><br/>Power on - startup delay - open - pause - close - repeat.<br/>Open/Close changes target and cycling resumes.<br/>Stop clears outputs and remains active until Resume.',40,525,size=12)
m.text('The network task and motion loop are separate. No browser or Wi-Fi client is required for motion. The web interface is embedded in C++ source; this publication has no standalone HTML catalogue.',40,400)
m.text('<b>Public Wi-Fi template</b><br/>Copy src/config.example.h to src/solarskin_config.h and set a local password. The local file is ignored by Git. Connect to SolarSkin and open http://192.168.4.1. The public fallback password is a template, not a secret.',40,300)
m.text('<b>Build:</b> pio run -j 1 -d firmware/stand<br/><b>Upload:</b> pio run -j 1 -d firmware/stand -t upload<br/><b>Math:</b> python3 engineering/calculations.py --reduction 8 --mode full',40,185,size=10)
m.new('18 / Calibrate the actual reduction')
steps=[('Identify the drivetrain','Confirm the installed P13/P12/P26 lead family and the extra reduction downstream of the geared motor output.'),('Measure the ratio','Count geared-output shaft turns per lead-screw turn. The built-in nominal 64:1 is already included in the step resolution.'),('Confirm physical travel','With power off, check the unobstructed stroke, direction and cable motion. The CAD target is about 15.35 mm.'),('Calculate the initial count','Use N = S G x/L. Select a conservative count and keep clearance to actual mechanical stops.'),('Observe a cycle','Check all leaves and rods. A missed step or stalled motor does not update the position estimate.'),('Test the populated frame','Check neighbouring modules, supply voltage, driver behavior and temperature; then extend the demonstration.')]
y=730
for title,body in steps:y=m.text(title,40,y,size=12,bold=True)-5;y=m.text(body,40,y)-22
m.text('Power cycling assumes the mechanism is closed. It does not recover an unknown physical position. No end-stop sensors or torque feedback are implemented.',40,115,size=9)
m.new('19 / Manufacturing and version control')
m.table([['GROUP','QUANTITY RULE'],['Mechanism','28 types / 62 printed pieces per module'],['9 / 12 / 14 / 16 modules','558 / 744 / 868 / 992 mechanism pieces'],['Frame and reinforcement','One common stand; do not multiply with module count'],['Shared tools','One workshop set'],['P08 alternatives','Substitute only after testing; do not add on top of originals']],[190,325],40,730)
m.text('P1S with a 0.4 mm nozzle and the user\'s Strong 0.20 mm profile is the project starting point. Keep millimetres, 100% scale and the supplied orientation. First-layer burrs, thread fit and bridging depend on the actual filament.',40,455)
m.text('The original three-part transmission revision had a support-disabled slicing check at 0.16 mm, six walls and 100% infill. This is not validation of every archived part with every profile. No Bambu Studio operation was performed for this publication.',40,350)
m.text('<b>Draft enclosures:</b> the power-supply base has a recorded 66 mm bridge and lid-seating clearances require revision. The E09 screw quantities 10 and 14 are alternatives, not a summed requirement.',40,245)
m.text('<b>Split P08 axle:</b> two halves plus one rail per axle; print the short coupon first. No positive axial locking or equivalent strength to the solid axle has been demonstrated.',40,145)
m.new('20 / Verification and source references')
m.table([['CHECK','WHAT IT ESTABLISHES'],['Analytic kinematics','All nine saved CAD positions, link closure and derivative consistency'],['Firmware simulation','Phase packing, 56 clocks/latch, automatic reversal, Stop/Resume and bounds'],['CAD/mesh reports','Recorded nominal solids, intersections and placements'],['Physical evidence','User-reported tests; no certified global strength/endurance result']],[165,350],40,730)
m.text('<b>Project evidence</b><br/>engineering/evidence/cad_stroke_samples.json<br/>engineering/evidence/thread_geometry_check.json<br/>engineering/source/rebuild_thread.FCMacro<br/>bom/mechanism.csv, frame.csv, reinforcement.csv',40,445,size=9.5)
m.text('<b>Primary technical references</b><br/>Thomson - Difference between screw pitch and lead; Precision Screws catalogue.<br/>WM Berg - Lead screw calculations.<br/>TI - SN74HC595 and ULN2003A datasheets.<br/>Espressif - ESP32-WROOM-32 datasheet.<br/>Full URLs are listed in docs/11_references.md.',40,315,size=9.5)
m.text('New assembly images render the supplied final CAD geometry. Earlier architectural renders show optional building concepts. Neither is a photograph or a physical qualification test.',40,190)
m.text('Author and license selection remain with the project owner. Third-party component CAD requires attribution/license review before online redistribution.',40,105,size=9)
m.save()
# Six parts per A4 page, two views per part, no handwritten stock assumptions.
rows=list(csv.DictReader((ROOT/'bom/mechanism.csv').open()))
cat=Manual(OUT/'SOLARSKIN_PARTS_CATALOG.pdf','SolarSkin - Parts Identification Catalogue')
notes={'P04':'Nominal hub disc diameter 39 mm, disc thickness 6 mm; total bounding box includes stops.','P05':'Pillar length 110.90 mm; axle-head recess.','P08':'85 mm axle; shaft diameter 5.13; tip diameter 4, pitch 1.2, thread length 6 mm.','P09':'D-profile guide, 112.65 mm long.','P13':'Three starts; 10 mm lead; 3.333333 mm pitch; nominal crest diameter 10.20 mm.','P33':'Short bushing, body length 9.8 mm; mate with P34.','P36':'Long tray bushing, body length 11.8 mm; mate with P37.','P34':'Short cone/screw pair for P33; 10 mm under head.','P37':'Long cone/screw pair for P36; 12 mm under head.','P44':'Custom diameter 16, pitch 4; 16 mm engagement; D-profile shank.','P46':'12.8 mm overall; 10 mm under head; not the E03 cover screw.','E03':'22 mm overall; 20 mm under head; terminal diameter 4, pitch 1.2. Three per module.'}
for page_start in range(0,len(rows),6):
 cat.new('Mechanism parts / '+str(page_start//6+1),'SIX PARTS PER A4 SHEET')
 cat.text('Quantities are per module. Multiply only mechanism quantities. Dimensions below are STL bounding boxes in print orientation.',40,735,size=8.5)
 for j,row in enumerate(rows[page_start:page_start+6]):
  col=j%2;rr=j//2;x=40+col*265;y=690-rr*204;cw=250
  c=cat.c;c.setFillColor(PALE);c.roundRect(x,y-190,cw,190,7,fill=1,stroke=0)
  code=row['part_id'].split('_')[0];cat.text(code+' / '+row['per_module']+' per module',x+10,y-8,cw-20,11,bold=True)
  cat.text(row['description'],x+10,y-28,cw-20,8,10)
  for k,view in enumerate(['iso','plan']):
   image=ROOT/'media/parts'/f'{code}_{view}.png'
   cat.image(image,x+8+k*118,y-130,115,78)
  bounds=' x '.join(f'{float(row[k]):.2f}' for k in ['size_x_mm','size_y_mm','size_z_mm'])+' mm'
  cat.text(bounds+' / '+row['color'].replace('_',' '),x+10,y-135,cw-20,7.8,10)
  cat.text(notes.get(code,'Match the part ID and orientation to the assembly CAD.'),x+10,y-151,cw-20,7.2,9)
cat.save()
print('Engineering manual pages:',m.page,'Parts catalogue pages:',cat.page)
