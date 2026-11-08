"""Animate one nominal rigid linkage through equal carriage increments."""
from pathlib import Path
import math
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
def height(theta):
    return 12*math.sin(theta)+math.sqrt(20**2-(12*math.cos(theta))**2)

def frame(fraction):
    lo,hi=0.,math.radians(75)
    z=16+fraction*(height(hi)-16)
    for _ in range(45):
        mid=(lo+hi)/2
        if height(mid)<z:lo=mid
        else:hi=mid
    b=(12*math.cos(mid),12*math.sin(mid))
    assert abs(math.hypot(b[0],z-b[1])-20)<1e-8
    im=Image.new('RGB',(620,340),'#f4f7fa');d=ImageDraw.Draw(im)
    def pos(x,y):return (150+7*x,285-7*y)
    a=pos(0,z);joint=pos(*b);pivot=pos(0,0)
    d.line([pos(0,35),pivot],fill='#8394a4',width=3)
    d.line([pivot,joint],fill='#e77e26',width=9)
    d.line([joint,a],fill='#2373a7',width=6)
    for x,y in [pivot,joint,a]:d.ellipse((x-4,y-4,x+4,y+4),fill='#172c3d')
    d.text((20,13),'ONE WING   /   SIDE ELEVATION',fill='#172c3d')
    for i,line in enumerate(['CAD linkage at nominal dimensions',f'Leaf angle: {math.degrees(mid):.1f} degrees',f'Carriage travel: {z-16:.2f} mm',f'Screw turns: {(z-16)/10:.3f}', 'Orange: 12 mm pivot arm','Blue: 20 mm connecting rod','Animation time is illustrative.']):
        d.text((320,55+28*i),line,fill='#172c3d')
    return im

if __name__=='__main__':
    frames=[frame(i/32) for i in range(33)]
    frames[0].save(ROOT/'media/engineering/one_wing_cycle.gif',save_all=True,append_images=frames[1:]+frames[-2:0:-1],duration=75,loop=0)
