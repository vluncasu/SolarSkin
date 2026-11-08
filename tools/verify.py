#!/usr/bin/env python3
"""Check the essential publication, local links, BOMs and distribution exclusions."""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
 errors=[]
 for f in [ROOT/'README.md',*ROOT.joinpath('docs').rglob('*.md'),*ROOT.joinpath('tools').glob('*.md')]:
  for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',f.read_text()):
   target=target.split('#')[0]
   if target and not re.match(r'^\w+://',target) and not (f.parent/target).exists():errors.append(f'Broken link: {f.name}: {target}')
 rows=list(csv.DictReader((ROOT/'bom/mechanism.csv').open()))
 if len(rows)!=28 or sum(int(r['per_module']) for r in rows)!=62:errors.append('Unexpected mechanism inventory.')
 for name in ['mechanism.csv','frame.csv','reinforcement.csv']:
  for row in csv.DictReader((ROOT/'bom'/name).open()):
   if not (ROOT/row['file']).is_file():errors.append('Missing print file: '+row['file'])
 total=0;count=0
 for f in ROOT.rglob('*'):
  if not f.is_file() or any(x in {'.git','.pio','tmp','local_releases','__pycache__'} for x in f.relative_to(ROOT).parts):continue
  total+=f.stat().st_size;count+=1
  if f.suffix.lower() in {'.html','.htm'}:errors.append('Standalone HTML file: '+str(f.relative_to(ROOT)))
  if f.name in {'solarskin_config.h','secrets.h','.env'}:errors.append('Private configuration: '+str(f.relative_to(ROOT)))
 if (ROOT/'archive').exists():errors.append('Historical archive must not be distributed.')
 required=['cad/04_building_optional/BUILDING_ASSEMBLY.blend','cad/04_building_optional/BUILDING.FCStd','docs/pdf/SOLARSKIN_ENGINEERING_AND_ASSEMBLY.pdf','docs/pdf/SOLARSKIN_PARTS_CATALOG.pdf']
 for name in required:
  if not (ROOT/name).exists():errors.append('Missing essential file: '+name)
 result={'result':'PASS' if not errors else 'FAIL','edition':'essential','files':count,'working_bytes':total,'mechanism_types':len(rows),'mechanism_pieces_per_module':sum(int(r['per_module']) for r in rows),'historical_archive_included':False,'errors':errors}
 (ROOT/'verification/publication.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
