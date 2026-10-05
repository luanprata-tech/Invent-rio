import re

with open('app/templates/inventario.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.finditer(r'<button[^>]*title="Ver Detalhes[^>]*>.*?</button>', html, re.DOTALL)
for m in matches:
    print(m.group(0))

