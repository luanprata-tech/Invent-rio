with open('app/templates/inventario.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('<script id="script-modal-cadastro')
end = html.find('</script>', idx)
print(html[idx:end+9])
