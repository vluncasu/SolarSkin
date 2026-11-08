"""Typeset the comparative study using its Markdown chapters and original CAD views."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table
from PIL import Image as Raster

root = Path(__file__).resolve().parents[1]
source = root / 'docs/12_building_and_facade.md'
target = root / 'docs/pdf/SOLARSKIN_COMPARATIVE_DESIGN_STUDY.pdf'
styles = getSampleStyleSheet()
story = []
for block in source.read_text().strip().split('\n\n'):
    if block.startswith('# '):
        story += [Paragraph(escape(block[2:]), styles['Title']), Spacer(1, 18)]
    elif block.startswith('## '):
        if re.match(r'## (I+\.|IV\.|Reproduction)', block):
            story.append(PageBreak())
        story.append(Paragraph(escape(block[3:]), styles['Heading2']))
    elif block.startswith('!['):
        alt, path = re.fullmatch(r'!\[(.*?)\]\((.*?)\)',block).groups()
        file = source.parent / path
        with Raster.open(file) as img:
            w,h = img.size
        scale = min(420/w, 140/h)
        story += [Image(str(file),width=w*scale,height=h*scale),Paragraph(escape(alt),styles['Italic']),Spacer(1,6)]
    elif block.startswith('|'):
        data = []
        for row in block.splitlines():
            if '---' in row: continue
            cells = [re.sub(r'\[(.*?)\]\(.*?\)',r'\1',v.strip()) for v in row.strip('|').split('|')]
            data.append([Paragraph(escape(v),styles['BodyText']) for v in cells])
        story.append(Table(data,colWidths=[94,155,191],style=[('VALIGN',(0,0),(-1,-1),'TOP')]))
    else:
        value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block).replace('\n',' ').replace('`','')
        story += [Paragraph(escape(value),styles['BodyText']),Spacer(1,5)]
def footer(canvas,doc):
    canvas.setFont('Helvetica',8)
    canvas.drawString(52,28,'SolarSkin | Comparative architectural design')
    canvas.drawRightString(540,28,str(doc.page))
SimpleDocTemplate(str(target),pagesize=A4,leftMargin=52,rightMargin=52,topMargin=40,bottomMargin=44,title='SolarSkin | Comparative architectural design').build(story,onFirstPage=footer,onLaterPages=footer)
