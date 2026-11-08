"""Minimal FreeCAD helpers for the standalone V7 module. Units: millimetres."""
import sys,math,json
from pathlib import Path
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as A,Part,MeshPart
V=A.Vector
def box(x,y,z,p=(0,0,0)):return Part.makeBox(x,y,z,V(*p))
def cyl(r,h,p=(0,0,0),axis=(0,0,1)):return Part.makeCylinder(r,h,V(*p),V(*axis))
def poly(points,h):
 vs=[V(*p) for p in points];return Part.Face(Part.makePolygon(vs+[vs[0]])).extrude(V(0,0,h))
def fuse(ss):return ss[0].multiFuse(ss[1:]).removeSplitter() if len(ss)>1 else ss[0]
def moved(s,p=(0,0,0),axis=(0,0,1),angle=0):
 s=s.copy();s.rotate(V(),V(*axis),angle);s.translate(V(*p));return s
def place(p=(0,0,0),axis=(0,0,1),angle=0):return A.Placement(V(*p),A.Rotation(V(*axis),angle))
def guides():return [(14.5*math.cos(math.radians(30+120*k)),14.5*math.sin(math.radians(30+120*k))) for k in range(3)]
def ztheta(t):
 a=math.radians(t);return 12*math.sin(a)+math.sqrt(400-144*math.cos(a)**2)
def sectorplace(k):return place(angle=90+120*k)
def pivot(t):return place(axis=(1,0,0),angle=t)
def prism_yz(points,x,length):
 vs=[V(x,y,z) for y,z in points];return Part.Face(Part.makePolygon(vs+[vs[0]])).extrude(V(length,0,0))
def drop_hole(r,x,length,y=0,z=0):
 return cyl(r,length,(x,y,z),(1,0,0)).fuse(prism_yz([(y-r*.707,z+r*.707),(y,z+r*1.414),(y+r*.707,z+r*.707)],x,length))
def roof_barrel(r,x,length):
 return cyl(r,length,(x,0,0),(1,0,0)).fuse(prism_yz([(-r*.707,-r*.707),(-r*.414,-r),(r*.414,-r),(r*.707,-r*.707)],x,length))
