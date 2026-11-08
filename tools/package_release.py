#!/usr/bin/env python3
"""Package only the essential edition; verify ZIP CRCs and record SHA256."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
 out=ROOT/'local_releases';out.mkdir(exist_ok=True);target=out/'SOLARSKIN_ESSENTIAL.zip'
 excluded={'.git','.pio','tmp','local_releases','__pycache__','archive','historical'}
 files=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(ROOT).parts) and p.name not in {'solarskin_config.h','secrets.h','.env'}]
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in sorted(files):z.write(p,'SolarSkin/'+str(p.relative_to(ROOT)))
 with zipfile.ZipFile(target) as z:
  if z.testzip():raise RuntimeError('ZIP integrity check failed')
 assets=[target,*sorted((ROOT/'docs/pdf').glob('*.pdf'))];rows=[]
 for p in assets:
  h=hashlib.sha256()
  with p.open('rb') as f:
   while b:=f.read(1024*1024):h.update(b)
  rows.append({'file':p.name,'bytes':p.stat().st_size,'sha256':h.hexdigest()})
 (out/'SHA256SUMS.txt').write_text(''.join(f"{v['sha256']}  {v['file']}\n" for v in rows))
 (out/'release_assets.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
