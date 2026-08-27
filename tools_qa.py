from pathlib import Path
import ast,re,sys
root=Path(__file__).resolve().parent
errors=[]
for p in root.rglob('*.py'):
    if 'venv' in p.parts: continue
    try: ast.parse(p.read_text(encoding='utf-8'))
    except SyntaxError as e: errors.append(f'PY {p}: {e}')
app=(root/'app.py').read_text(encoding='utf-8')
funcs=set(re.findall(r'^def\s+(\w+)\(',app,re.M))
refs=set()
for p in (root/'templates').glob('*.html'):
    refs |= set(re.findall(r"url_for\(\s*['\"]([^'\"]+)",p.read_text(encoding='utf-8',errors='ignore')))
refs.discard('static')
missing=sorted(x for x in refs if x not in funcs)
if missing: errors.append('TEMPLATE ENDPOINTS NOT FOUND: '+', '.join(missing))
if errors:
    print('QA FAIL\n'+'\n'.join(errors)); sys.exit(1)
print('QA PASS: Python AST + template endpoint names')
