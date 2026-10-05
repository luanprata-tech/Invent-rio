with open('app/templates/inventario.html', 'r', encoding='utf-8') as f:
    html = f.read()
if 'id="input-categoria"' in html:
    print('exists')
else:
    print('does not exist')
