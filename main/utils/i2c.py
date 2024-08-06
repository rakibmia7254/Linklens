import sqlite3, ipaddress


def ip_to_integer(ip):
    try:
        return int(ipaddress.ip_address(ip))
    except:
        return None

def lookup_ip(ip):
    ip_int = ip_to_integer(ip)
    
    if not ip_int:
        return "Unknown"
    
    conn = sqlite3.connect('./ip_geolocation.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT region
        FROM ip_ranges
        WHERE ? BETWEEN start_ip AND end_ip
    ''', (ip_int,))
    result = cursor.fetchone()
    conn.close()
    if result:
        if result[0] == "Reserved":
            return "Unknown"
        return result[0]
    else:
        return "Unknown"