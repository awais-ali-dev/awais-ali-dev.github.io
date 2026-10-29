"""Offline release checks for the static portfolio; no external requests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re,json,base64,hashlib
from site_config import SITE_URL, BASE_PATH

ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'
errors=[];checks=0
def check(condition,message):
    global checks
    checks+=1
    if not condition:errors.append(message)

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.nodes=[];self.ids=[];self.scripts=[];self.current=None;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.nodes.append((tag,a))
        if a.get('id'):self.ids.append(a['id'])
        if tag=='script':self.current={'attrs':a,'text':''};self.scripts.append(self.current)
    def handle_data(self,data):
        if self.current is not None:self.current['text']+=data
    def handle_endtag(self,tag):
        if tag=='script':self.current=None

files=sorted(p for p in DIST.rglob('*.html') if not p.name.startswith('__qa'))
pages={p:Page(p.read_text(encoding='utf-8')) for p in files}
for path,doc in pages.items():
    rel=str(path.relative_to(DIST))
    canonical=next((a.get('href','') for tag,a in doc.nodes if tag=='link' and a.get('rel')=='canonical'),'')
    check(canonical.startswith(SITE_URL+'/'),f'{rel}: incorrect canonical URL')
    check(len(doc.ids)==len(set(doc.ids)),f'{rel}: duplicate IDs')
    check(sum(tag=='h1' for tag,a in doc.nodes)==1,f'{rel}: expected one main heading')
    check(any(tag=='html' and a.get('lang')=='en' for tag,a in doc.nodes),f'{rel}: language')
    check(any(tag=='meta' and a.get('name')=='description' and a.get('content') for tag,a in doc.nodes),f'{rel}: description')
    csp=next((a['content'] for t,a in doc.nodes if t=='meta' and a.get('http-equiv')=='Content-Security-Policy'),'')
    for directive in ["default-src 'none'","connect-src 'none'","object-src 'none'","base-uri 'none'","form-action 'none'"]:
        check(directive in csp,f'{rel}: missing {directive}')
    check('unsafe-inline' not in csp and 'unsafe-eval' not in csp,f'{rel}: unsafe CSP')
    for tag,a in doc.nodes:
        check(not any(k.lower().startswith('on') for k in a),f'{rel}: inline event handler')
        check('style' not in a,f'{rel}: inline styles')
        check(tag not in ['form','iframe','object','embed'],f'{rel}: unexpected active surface {tag}')
        if tag=='img':check(bool(a.get('alt')),f'{rel}: missing image description')
        if tag=='a' and a.get('target')=='_blank':
            check({'noopener','noreferrer'}.issubset(set(a.get('rel','').split())),f'{rel}: unsafe new tab')
        for attr in ['href','src']:
            if attr not in a:continue
            link=a[attr];u=urlsplit(link)
            check(u.scheme in ['', 'https','mailto'],f'{rel}: unsafe scheme {u.scheme}')
            if u.scheme or u.netloc:continue
            local_path=unquote(u.path)
            if local_path.startswith('/'):
                check(local_path.startswith(BASE_PATH+'/'),f'{rel}: path is outside site base {link}')
                local_path=local_path[len(BASE_PATH):]
                target=DIST/local_path.lstrip('/')
            else:
                target=path.parent/local_path
            if not u.path:target=path
            if target.is_dir():target=target/'index.html'
            check(target.exists(),f'{rel}: missing local destination {link}')
            if u.fragment and target in pages:check(unquote(u.fragment) in pages[target].ids,f'{rel}: missing anchor {link}')
        if tag in ['script','link','img'] and a.get('src',a.get('href','')).startswith('http') and a.get('rel') not in ['canonical']:
            check(False,f'{rel}: externally loaded asset')
    for script in doc.scripts:
        a=script['attrs']
        if a.get('src'):continue
        check(a.get('type')=='application/ld+json',f'{rel}: unexpected inline script')
        if a.get('type')=='application/ld+json':
            json.loads(script['text'])
            digest=base64.b64encode(hashlib.sha256(script['text'].encode()).digest()).decode()
            check('sha256-'+digest in csp,f'{rel}: JSON-LD hash mismatch')

js=(DIST/'assets/site.js').read_text(encoding='utf-8')
for pattern in [r'\.innerHTML\b',r'\.outerHTML\s*=',r'\beval\s*\(',r'new Function\s*\(',r'\bdocument\.write',r'\bfetch\s*\(',r'XMLHttpRequest',r'localStorage',r'sessionStorage',r'\.cookie\s*=']:
    check(not re.search(pattern,js),f'Unsafe or unexpected JS API: {pattern}')
for p in DIST.rglob('*'):
    if not p.is_file():continue
    check(not any(x in p.name.lower() for x in ['cnic','domicile','idcard','transcript','my_sign','.env','__qa','source-map']),f'Unexpected private/debug file: {p.name}')
    check(p.suffix not in ['.zip','.map','.docx','.py'],f'Unexpected deployment file: {p.name}')
    if p.suffix in ['.html','.js','.css','.json','.txt','.xml','.svg']:
        text=p.read_text(encoding='utf-8')
        for pattern in [r'AKIA[0-9A-Z]{16}',r'ghp_[A-Za-z0-9]{30,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'\b\d{5}-\d{7}-\d\b',r'\b\d{3}-\d{2}-\d{4}\b']:
            check(not re.search(pattern,text),f'Sensitive data pattern in {p.name}')
check(len(json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8')))==13,'Project content count')
check(len(json.loads((ROOT/'content/credentials.json').read_text(encoding='utf-8')))==42,'Credential content count')
headers=(DIST/'_headers').read_text(encoding='utf-8')
for h in ['Content-Security-Policy:','X-Content-Type-Options: nosniff','Referrer-Policy: no-referrer','Permissions-Policy:','Strict-Transport-Security:',"frame-ancestors 'none'"]:
    check(h in headers,'Missing header configuration '+h)
check((DIST/'.well-known/security.txt').exists(),'Missing security contact')
check((DIST/'sitemap.xml').exists(),'Missing sitemap')
check((DIST/'assets/site.js').stat().st_size<12000,'JS size budget')
check((DIST/'index.html').stat().st_size<50000,'Homepage size budget')
result={'status':'passed' if not errors else 'failed','checks':checks,'html_files':len(files),'errors':errors,'limits':'Static and structural checks only; not a penetration test or proof of hosting header enforcement.'}
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
