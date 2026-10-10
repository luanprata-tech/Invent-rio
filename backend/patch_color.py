with open('app/templates/ips.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('bg-orange-400 text-white', 'bg-slate-200 text-slate-600')
text = text.replace('bg-orange-400', 'bg-slate-200')
text = text.replace('hover:bg-orange-500 shadow-sm', 'hover:bg-slate-300 shadow-sm')
text = text.replace('text-orange-600', 'text-slate-500')
text = text.replace('hover:bg-orange-500/10 border border-orange-500/30', 'hover:bg-slate-500/10 border border-slate-500/30')

with open('app/templates/ips.html', 'w', encoding='utf-8') as f:
    f.write(text)
