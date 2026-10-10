import re

with open('app/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern_ip = r'async def ping_ip.*?return ip_address, proc\.returncode == 0'
new_ip = '''async def ping_ip(ip_address: str):
    import platform
    is_windows = platform.system().lower() == "windows"
    cmd = ['ping', '-n', '1', '-w', '1000', ip_address] if is_windows else ['ping', '-c', '1', '-W', '1', ip_address]
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    out_str = stdout.decode('utf-8', errors='ignore').lower()
    
    if 'unreachable' in out_str or 'inacess' in out_str:
        return ip_address, 'unreachable'
    elif proc.returncode == 0 and 'esgotado' not in out_str and 'time out' not in out_str and '100% packet loss' not in out_str:
        return ip_address, 'up'
    else:
        return ip_address, 'timeout' '''

text = re.sub(pattern_ip, new_ip, text, flags=re.DOTALL)

pattern_subnet = r'for ip_str, is_up in ping_status\.items\(\):.*?db\.add\(new_ip\)'
new_subnet = '''for ip_str, status_str in ping_status.items():
        if ip_str in db_ips_dict:
            db_ips_dict[ip_str].last_ping_result = status_str
        else:
            if status_str != 'timeout':
                new_ip = IP(ip_address=ip_str, subnet=req.subnet, status='Livre', last_ping_result=status_str)
                db.add(new_ip)'''

text = re.sub(pattern_subnet, new_subnet, text, flags=re.DOTALL)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
