from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,re,math
root=Path(__file__).resolve().parent
page=Path(__file__).with_name('progress.html').read_bytes()
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path.startswith('/status'):
   logs=list(root.glob('log.*')); newest=max(logs,key=lambda p:p.stat().st_mtime) if logs else None
   tail=newest.read_text(errors='replace')[-12000:] if newest else ''
   solver=(root/'log.foamRun').read_text(errors='replace')[-250000:] if (root/'log.foamRun').exists() else ''
   it=re.findall(r'^Time = (\S+)',solver,re.M)
   vals={}
   for key in ['Cd','Cl','Cm']:
    matches=re.findall(r'^\s*'+key+r'\s*=\s*([-+\deE.]+)',solver,re.M)
    if matches:
     try: vals[key]=float(matches[-1])
     except ValueError:pass
   data={'stage':(root/'stage.txt').read_text() if (root/'stage.txt').exists() else 'Preparing','iteration':it[-1].rstrip('s') if it else None,'coefficients':vals,'log':newest.name if newest else '', 'tail':tail[-6000:]}
   body=json.dumps(data).encode(); mime='application/json'
  else:body=page;mime='text/html; charset=utf-8'
  self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass
ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
