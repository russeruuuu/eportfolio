"""Create static, read-only notebook pages without executing any notebook code."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import quote, urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'notebooks';OUT.mkdir(exist_ok=True)

def joined(value):return ''.join(value) if isinstance(value,list) else str(value or '')
def inline(text):
 text=escape(text)
 text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
 text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
 text=re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)',r'<em>\1</em>',text)
 return text

def markdown(text):
 lines=text.splitlines();out=[];paragraph=[];code=None;listing=False;table=False
 def flush():
  if paragraph:out.append('<p>'+inline('\n'.join(paragraph))+'</p>');paragraph.clear()
 def close_list():
  nonlocal listing
  if listing:out.append('</ul>');listing=False
 def close_table():
  nonlocal table
  if table:out.append('</tbody></table></div>');table=False
 for line in lines:
  if line.strip().startswith('```'):
   flush();close_list();close_table()
   if code is None:code=[]
   else:out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>');code=None
   continue
  if code is not None:code.append(line);continue
  if re.match(r'^\s*\|?[\s:|-]+\|[\s:|-]*$',line):continue
  if line.strip().startswith('|') and '|' in line.strip()[1:]:
   flush();close_list()
   if not table:out.append('<div class="nb-table"><table><tbody>');table=True
   out.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in line.strip().strip('|').split('|'))+'</tr>');continue
  close_table()
  h=re.match(r'^(#{1,6})\s+(.+)$',line)
  bullet=re.match(r'^\s*(?:[-*+]\s+|\d+[.)]\s+)(.+)$',line)
  if h:
   flush();close_list();level=min(len(h[1])+1,6);out.append(f'<h{level}>'+inline(h[2])+f'</h{level}>')
  elif bullet:
   flush()
   if not listing:out.append('<ul>');listing=True
   out.append('<li>'+inline(bullet[1])+'</li>')
  elif not line.strip():flush();close_list()
  elif re.match(r'^\s*[-*_]{3,}\s*$',line):flush();close_list();out.append('<hr>')
  else:close_list();paragraph.append(line)
 flush();close_list();close_table()
 if code is not None:out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>')
 return '\n'.join(out)

class SafeHTML(HTMLParser):
 allowed={'table','thead','tbody','tfoot','tr','th','td','caption','p','div','span','strong','b','em','i','br','pre','code','ul','ol','li','h1','h2','h3','h4','h5','h6','a','hr','sup','sub'}
 blocked={'script','style','iframe','object','embed','svg','form','button','input'}
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.block=0
 def handle_starttag(self,tag,attrs):
  if tag in self.blocked:self.block+=1;return
  if self.block or tag not in self.allowed:return
  attributes=''
  for name,value in attrs:
   if tag=='a' and name=='href' and urlsplit(value or '').scheme in ('https','http'):
    attributes+=' href="'+escape(value,quote=True)+'" target="_blank" rel="noopener noreferrer"'
   if tag in ('td','th') and name in ('colspan','rowspan') and (value or '').isdigit():attributes+=' '+name+'="'+value+'"'
  self.parts.append('<'+tag+attributes+'>')
 def handle_endtag(self,tag):
  if tag in self.blocked:self.block=max(0,self.block-1);return
  if not self.block and tag in self.allowed and tag not in ('br','hr'):self.parts.append('</'+tag+'>')
 def handle_data(self,data):
  if not self.block:self.parts.append(escape(data))

def output_html(output):
 kind=output.get('output_type');data=output.get('data',{})
 if kind=='stream':return '<pre class="nb-output">'+escape(re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', joined(output.get('text'))))+'</pre>'
 if kind=='error':
  text='\n'.join(output.get('traceback',[])) or output.get('ename','')+': '+output.get('evalue','')
  return '<pre class="nb-output nb-error">'+escape(re.sub(r'\x1b\[[0-9;]*m','',text))+'</pre>'
 for mime in ('image/png','image/jpeg'):
  if mime in data:
   encoded=re.sub(r'\s','',joined(data[mime]))
   if re.fullmatch(r'[A-Za-z0-9+/=]+',encoded):return '<figure><img loading="lazy" src="data:'+mime+';base64,'+encoded+'" alt="Saved notebook chart output"></figure>'
 if 'text/html' in data:
  parser=SafeHTML();parser.feed(joined(data['text/html']));return '<div class="nb-rich-output">'+''.join(parser.parts)+'</div>'
 if 'text/plain' in data:return '<pre class="nb-output">'+escape(joined(data['text/plain']))+'</pre>'
 return '<p class="nb-widget-note">This interactive output is available in the original notebook.</p>' if data else ''

catalog=json.loads((ROOT/'assets/catalog.js').read_text().split(' = ',1)[1].rstrip(';\n'))
count=0
for activity in catalog:
 for file in activity['files']:
  if file['type']!='IPYNB':continue
  notebook=json.loads((ROOT/file['path']).read_text());cells=[];code_count=0;output_count=0
  for i,cell in enumerate(notebook.get('cells',[]),1):
   source=joined(cell.get('source'))
   if cell.get('cell_type')=='markdown':cells.append('<section class="nb-markdown">'+markdown(source)+'</section>')
   elif cell.get('cell_type')=='code':
    code_count+=1;outputs=cell.get('outputs',[]);output_count+=len(outputs)
    execution=cell.get('execution_count');label='Code cell '+str(code_count)+(f' · In [{execution}]' if execution is not None else '')
    cells.append('<section class="nb-cell"><details class="nb-code" open><summary>'+label+'</summary><pre><code>'+escape(source)+'</code></pre></details>'+(''.join(output_html(o) for o in outputs))+'</section>')
   elif source:cells.append('<pre>'+escape(source)+'</pre>')
  download='../'+quote(file['path'],safe='/')
  page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+escape(activity['title'])+''' — Notebook</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/notebook.css"><script src="../assets/notebook.js" defer></script></head><body><a class="skip" href="#notebook">Skip to notebook</a><header class="nb-toolbar"><a href="../index.html#work">← Back to activities</a><div><button id="toggle-code" aria-pressed="false">Hide code</button><a href="'''+download+'''" download>Download .ipynb ↗</a></div></header><main class="nb-page" id="notebook"><p class="eyebrow">'''+escape(activity['term'].upper())+' / WEEK '+activity['week']+''' · NOTEBOOK</p><h1>'''+escape(activity['title'])+'''</h1><p class="nb-filename">'''+escape(file['name'])+'''</p><p class="nb-intro">Read the explanations, code, and saved results below. This preview does not run code; interactive widgets require opening the original notebook in Jupyter or Colab.</p><p class="nb-stats">'''+str(code_count)+' code cells · '+str(output_count)+''' saved outputs</p><div class="nb-content">'''+''.join(cells)+'''</div><a class="nb-end" href="../index.html#work">← Back to activities</a></main></body></html>'''
  (OUT/(activity['id']+'.html')).write_text(page);count+=1
print('Generated',count,'read-only notebook previews. No notebook code was executed.')
