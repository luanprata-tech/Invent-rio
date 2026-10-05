with open('app/templates/inventario.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

m1 = re.search(r'<input[^>]*id="delete-attr-endpoint"[^>]*>', html)
m2 = re.search(r'<input[^>]*id="delete-attr-id"[^>]*>', html)

if m1:
    print('endpoint:', m1.group(0))
else:
    print('endpoint NOT FOUND')

if m2:
    print('id:', m2.group(0))
else:
    print('id NOT FOUND')
