import re

with open('app/templates/ips.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace legend
legend_old = r'<span class="flex items-center gap-1\.5"><span class="w-3 h-3 rounded-sm bg-emerald-500"></span> Livre</span>'
legend_new = '''<span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-emerald-500"></span> Livre</span>\n                            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-orange-400"></span> Timeout (Livre)</span>'''
text = re.sub(legend_old, legend_new, text)

# Map logic - Alocado
aloc_old = r"{%\s*if ip_data\.last_ping_result == False\s*%}"
aloc_new = "{% if ip_data.last_ping_result == 'timeout' or ip_data.last_ping_result == 'unreachable' or ip_data.last_ping_result == False %}"
text = re.sub(aloc_old, aloc_new, text)

# Map logic - Livre
livre_old = r"{%\s*if ip_data\.last_ping_result == True\s*%}\s*<div.*?ALERTA.*?</div>\s*{%\s*else\s*%}\s*<div(.*?)bg-emerald-500(.*?)Livre(.*?)</div>\s*{%\s*endif\s*%}"
livre_new = r'''{% if ip_data.last_ping_result == 'up' or ip_data.last_ping_result == True %}
                                        <div onclick="openBindModal('{{ full_ip }}', 'Livre')" class="w-7 h-5 rounded-sm bg-error text-white font-bold flex items-center justify-center font-mono text-[9px] ring-1 ring-error/50 animate-pulse cursor-pointer shadow-sm select-none" title="ALERTA: {{ full_ip }} - Falso Livre!">.{{ i }}</div>
                                    {% elif ip_data.last_ping_result == 'timeout' %}
                                        <div onclick="openBindModal('{{ full_ip }}', 'Livre')" class="w-7 h-5 rounded-sm bg-orange-400 text-white font-bold flex items-center justify-center font-mono text-[9px] cursor-pointer hover:bg-orange-500 shadow-sm select-none" title="TIMEOUT: {{ full_ip }} - Livre (Sem Certeza)">.{{ i }}</div>
                                    {% else %}
                                        <div\1bg-emerald-500\2Livre\3</div>
                                    {% endif %}'''
text = re.sub(livre_old, livre_new, text, flags=re.DOTALL)

# Table filters
filter_old = r'<button class="px-3 py-1\.5 rounded-full bg-surface-container text-emerald-700.*?data-filter="livre">Livres</button>'
filter_new = r'<button class="px-3 py-1.5 rounded-full bg-surface-container text-emerald-700 font-label-sm text-[11px] font-bold uppercase tracking-wider transition-colors hover:bg-emerald-500/10 border border-emerald-500/30" data-filter="livre">Livres</button>\n                            <button class="px-3 py-1.5 rounded-full bg-surface-container text-orange-600 font-label-sm text-[11px] font-bold uppercase tracking-wider transition-colors hover:bg-orange-500/10 border border-orange-500/30" data-filter="timeout_livre">Livres (Timeout)</button>'
text = re.sub(filter_old, filter_new, text)

# Table logic - Alocado
table_aloc_old = r"{%\s*if ip\.last_ping_result == False\s*%}"
table_aloc_new = "{% if ip.last_ping_result == 'timeout' or ip.last_ping_result == 'unreachable' or ip.last_ping_result == False %}"
text = re.sub(table_aloc_old, table_aloc_new, text)

# Table logic - Livre
table_livre_old = r"{%\s*if ip\.last_ping_result == True\s*%}\s*{%\s*set computed_status = 'Livre \(Alerta\)'\s*%}.*?{%\s*else\s*%}\s*{%\s*set computed_status = 'Livre'\s*%}\s*{%\s*set filter_key = 'livre'\s*%}\s*{%\s*set badge_class = 'bg-emerald-500 text-white'\s*%}\s*{%\s*endif\s*%}"
table_livre_new = r'''{% if ip.last_ping_result == 'up' or ip.last_ping_result == True %}
                                            {% set computed_status = 'Livre (Alerta)' %}
                                            {% set filter_key = 'falso_livre' %}
                                            {% set badge_class = 'bg-error text-white animate-pulse' %}
                                        {% elif ip.last_ping_result == 'timeout' %}
                                            {% set computed_status = 'Livre (Timeout)' %}
                                            {% set filter_key = 'timeout_livre' %}
                                            {% set badge_class = 'bg-orange-400 text-white' %}
                                        {% else %}
                                            {% set computed_status = 'Livre' %}
                                            {% set filter_key = 'livre' %}
                                            {% set badge_class = 'bg-emerald-500 text-white' %}
                                        {% endif %}'''
text = re.sub(table_livre_old, table_livre_new, text, flags=re.DOTALL)


with open('app/templates/ips.html', 'w', encoding='utf-8') as f:
    f.write(text)
