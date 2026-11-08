"""Render two orthographic views per distributed STL and assemble illustrated inventories."""
from pathlib import Path
from collections import defaultdict
import csv,json,re
import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

root=Path(__file__).resolve().parents[1]
def read(path):
    with (root/path).open() as src:
        return list(csv.DictReader(src))

def view(tri,direction):
    camera=np.array(direction,dtype=float)
    camera/=np.linalg.norm(camera)
    right=np.cross([0,0,1],camera)
    right/=np.linalg.norm(right)
    up=np.cross(camera,right)
    points=tri@np.array([right,-up,camera]).T
    flat=points[:,:,:2]
    xy=flat.reshape(-1,2)
    factor=min(204/max(0.01,np.ptp(xy[:,0])),134/max(0.01,np.ptp(xy[:,1])))
    coords=np.rint((flat-(xy.min(0)+xy.max(0))/2)*factor+[110,75]).astype(np.int32)
    normal=np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0])
    normal/=np.maximum(1e-12,np.linalg.norm(normal,axis=1))[:,None]
    light=np.abs(normal@np.array([-.36,.45,.81]))
    shade=((.43+.52*light[:,None])*np.array([108,159,193])).astype(int).tolist()
    pic=np.full((150,220,3),250,np.uint8)
    for idx in np.argsort(points[:,:,2].mean(1)):
        cv2.fillConvexPoly(pic,coords[idx],shade[idx])
    return pic

def render(path,target):
    data=path.read_bytes()
    n=int.from_bytes(data[80:84],'little')
    assert len(data)==84+50*n,path
    tri=np.ndarray((n,3,3),'<f4',data,96,(50,12,4)).astype(float)
    img=np.concatenate([view(tri,[1,-1,0.85]),view(tri,[-1,.85,0.50])],axis=1)
    Image.fromarray(img).save(target,quality=88)
    return ' x '.join(f'{v:.1f}' for v in np.ptp(tri,axis=(0,1)))

def main():
    groups={}
    for table,label in [('mechanism','One mechanism'),('frame','Independent stand'),('reinforcement','Stand reinforcement')]:
        groups[label]=[(a['part_id'],a.get('per_module') or a['quantity'],a['color'],a['file'],'') for a in read('bom/'+table+'.csv')]
    for variant in ['furnished','simplified']:
        beds=defaultdict(set)
        for a in read(f'print/{variant}/placements.csv'):
            beds[a['part_id']].add(int(a['bed']))
        groups[variant.title()+' office']=[(a['part_id'],a['copies'],a['material'],f"print/{variant}/parts/{a['part_id']}.stl",', '.join(map(str,sorted(beds[a['part_id']])))) for a in read(f'print/{variant}/inventory.csv')]
    older=json.loads((root/'bom/building_optional_files.json').read_text())
    groups['Optional architectural revision']=[(Path(path).stem,old.split('_')[0],Path(path).parent.name,path,'') for old,path in older.items()]
    covered={v[3] for group in groups.values() for v in group}
    groups['Workshop tools and additional exports']=[(p.stem,'see file',p.parent.name,str(p.relative_to(root)),'') for p in sorted((root/'print').rglob('*.stl')) if str(p.relative_to(root)) not in covered]
    pdf=Canvas(str(root/'docs/pdf/SOLARSKIN_ALL_PARTS.pdf'),pagesize=A4)
    pdf.setTitle('SolarSkin | Illustrated manufacturing inventory')
    index=['# Illustrated parts inventory','','Choose one construction route. Quantities apply to the named group. The same identifier can refer to different geometry across revisions. All dimensions below are STL bounding boxes in millimetres.','']
    for group,items in groups.items():
        slug=group.lower().replace(' ','-')
        lines=['# '+group,'','The two views are rendered from the linked print file at independent scale. See the dimensions to distinguish similar parts.','']
        index.append(f'- [{group} - {len(items)} entries]({slug}.md)')
        for i,(name,qty,color,path,beds) in enumerate(items):
            target=root/f'media/atlas/{slug}-{i+1:03}.webp'
            dims=render(root/path,target)
            lines += [f'### {name}',f'![Two views of {name}](../../media/atlas/{target.name})','',f'Quantity: {qty}. Material/color: {color}. Size: {dims} mm.'+(f' Bed: {beds}.' if beds else ''),f'[Print mesh](../../{path})','']
            if i%6==0:
                pdf.setFont('Helvetica-Bold',18);pdf.drawString(32,807,group)
                pdf.setFont('Helvetica',9);pdf.drawString(32,786,'STL dimensions in mm | two views per item | counts apply to this configuration')
            x=30+(i%2)*270;y=745-(i%6//2)*238
            pdf.setFont('Helvetica-Bold',min(10,395/max(1,len(name))));pdf.drawString(x,y,name)
            pdf.drawImage(ImageReader(str(target)),x,y-107,252,86)
            pdf.setFont('Helvetica',10);pdf.drawString(x,y-130,f'Qty {qty}   |   {color}')
            pdf.drawString(x,y-148,dims+' mm')
            if beds:
                for offset in range(0,len(beds),45):pdf.drawString(x,y-166-offset//45*13,('Beds: ' if not offset else '')+beds[offset:offset+45])
            if i%6==5 or i==len(items)-1:pdf.showPage()
        (root/f'docs/atlas/{slug}.md').write_text('\n'.join(lines)+'\n')
    (root/'docs/atlas/README.md').write_text('\n'.join(index)+'\n')
    pdf.save()
if __name__=='__main__':
    main()
