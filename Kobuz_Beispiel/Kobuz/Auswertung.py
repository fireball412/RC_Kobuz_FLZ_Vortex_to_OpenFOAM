"""Aktuellen Kobuz-Kraftverlauf auswerten. Nur Python-Standardbibliothek."""
from pathlib import Path
import csv, json, math, re
root=Path(__file__).resolve().parent
files=list((root/'postProcessing'/'coefficients').glob('*/forceCoeffs.dat'))
if not files:
    raise SystemExit('Keine forceCoeffs.dat gefunden. Zuerst den Fall rechnen.')
file=max(files,key=lambda p:float(p.parent.name))
text=file.read_text()
def header(key):
    m=re.search(r'^#\s*'+key+r'\s*:\s*([-+\d.eE]+)',text,re.M)
    if not m: raise ValueError('Fehlender Parameter '+key)
    return float(m.group(1))
V,A,ell=header('magUInf'),header('Aref'),header('lRef')
control=(root/'system'/'controlDict').read_text()
rho=float(re.search(r'\brhoInf\s+([-+\d.eE]+)\s*;',control).group(1))
rows=[list(map(float,line.split())) for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')]
if not rows: raise SystemExit('Die Koeffizientendatei enthaelt noch keine Werte.')
t,Cm,Cd,Cl,*_=rows[-1]
q=.5*rho*V*V
E=Cl/Cd
gamma=math.atan2(Cd,Cl)
result={'iteration':t,'Cl':Cl,'Cd':Cd,'Cm':Cm,'rho':rho,'V':V,'Aref':A,'lRef':ell,
        'lift_N':q*A*Cl,'drag_N':q*A*Cd,'moment_Nm':q*A*ell*Cm,
        'L_zu_D':E,'aequivalenter_Gleitwinkel_Grad':math.degrees(gamma),
        'aequivalentes_Sinken_m_s':V*math.sin(gamma),
        'Hinweis':'Ein Betriebspunkt ohne Nachweis von Trimmung und Netzunabhaengigkeit.'}
(root/'Aktuell_Ergebnisse.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (root/'Aktuell_Kraftverlauf.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['iteration','Cm','Cd','Cl','Cl_front','Cl_rear']);w.writerows(rows)
print(json.dumps(result,ensure_ascii=False,indent=2))
