import re

with open('app/templates/inventario.html', 'r', encoding='utf-8') as f:
    html = f.read()

form_html = re.search(r'<form id="form-cadastro-equipamento".*?</form>', html, flags=re.DOTALL)
if form_html:
    inputs = re.findall(r'<(?:input|select)[^>]*>', form_html.group(0))
    for item in inputs:
        print(item)
else:
    print('Form not found')
