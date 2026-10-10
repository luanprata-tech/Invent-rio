import re

with open('app/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_ping = '''    if 'unreachable' in out_str or 'inacess' in out_str:
        return ip_address, 'unreachable'
    elif proc.returncode == 0 and 'esgotado' not in out_str and 'time out' not in out_str and '100% packet loss' not in out_str:
        return ip_address, 'up'
    else:
        return ip_address, 'timeout' '''

new_ping = '''    if 'unreachable' in out_str or 'inacess' in out_str or '100% packet loss' in out_str:
        return ip_address, 'unreachable'
    elif proc.returncode == 0 and 'esgotado' not in out_str and 'time out' not in out_str:
        return ip_address, 'up'
    else:
        return ip_address, 'timeout' '''

text = text.replace(old_ping, new_ping)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
