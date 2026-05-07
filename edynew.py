import os, sys, time, json, base64, uuid, subprocess, socket

# လိုအပ်တဲ့ requests library ရှိမရှိ စစ်မယ်
try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests

# အရောင်များ
G, R, B, Y, C, W = "\033[1;32m", "\033[1;31m", "\033[1;34m", "\033[1;33m", "\033[1;36m", "\033[1;37m"

def banner():
    os.system('clear')
    print(f"""{B}
    ╔════════════════════════════════════════╗
    ║      EDY ULTIMATE - ALL IN ONE TOOL    ║
    ╚════════════════════════════════════════╝{W}
    DEV   : {G}AungMyoHein{W}
    POWER : {Y}IP Check + Bug Scan + VPN Gen{W}
    GGMU  : {R}Manchester United Fan 🔴{W}
    ------------------------------------------""")

# --- [1] VMESS GENERATOR ---
def generate_vmess(bug, ip):
    v2_json = {
        "v": "2", "ps": f"EDY-FREE-{bug}",
        "add": ip, "port": "80", "id": str(uuid.uuid4()),
        "aid": "0", "scy": "auto", "net": "ws",
        "type": "none", "host": bug, "path": "/", "tls": "none"
    }
    js_str = json.dumps(v2_json)
    return "vmess://" + base64.b64encode(js_str.encode('ascii')).decode('ascii')

# --- [2] CLOUDFLARE IP CHECKER ---
def cf_ip_checker():
    banner()
    print(f"{C}[*] Cloudflare IP Speed Checker Starting...{W}\n")
    targets = ["104.16.10", "104.17.10", "104.18.10", "172.67.73", "104.21.10"]
    
    for subnet in targets:
        for i in range(1, 6):
            ip = f"{subnet}.{i}"
            print(f"{W}[Testing] {ip}...", end="\r")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, 80))
                if result == 0:
                    ping_cmd = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True)
                    ping_time = "N/A"
                    if "time=" in ping_cmd.stdout:
                        ping_time = ping_cmd.stdout.split("time=")[1].split(" ")[0]
                    print(f"{G}[FOUND] {ip:<15} | Latency: {ping_time} ms{W}")
                sock.close()
            except:
                continue
    input(f"\n{Y}Press Enter to return...{W}")

# --- [3] BUG SCANNER ---
def bug_scanner_gen():
    banner()
    target = input(f"{Y}[?] Enter Domain (eg. mytel.com.mm): {W}")
    cf_ip = input(f"{Y}[?] Enter Fast CF IP (Default: 104.18.10.1): {W}") or "104.18.10.1"
    
    print(f"\n{C}[*] Scanning Subdomains & Checking Bugs...{W}\n")
    print(f"{'HOST':<30} | {'CODE':<5} | {'RESULT'}")
    print("-" * 55)
    
    try:
        res = requests.get(f"https://crt.sh/?q=%25.{target}&output=json", timeout=15)
        subs = list(set([item['common_name'] for item in res.json()]))
        
        for host in subs:
            if "*" in host: continue
            try:
                r = requests.get(f"http://{host}", timeout=3, allow_redirects=False)
                ws_r = requests.get(f"http://{host}", headers={"Upgrade": "websocket", "Connection": "Upgrade"}, timeout=3)
                status = r.status_code
                ws_status = ws_r.status_code
                
                if status == 200 or ws_status == 101:
                    print(f"{G}{host:<30} | {status:<5} | WORKING!{W}")
                    link = generate_vmess(host, cf_ip)
                    print(f"{Y}[V2RAY] {link}{W}\n")
                elif status in [301, 302]:
                    print(f"{Y}{host:<30} | {status:<5} | REDIRECT{W}")
            except:
                continue
    except Exception as e:
        print(f"{R}[!] Error: {e}{W}")
    input(f"\n{G}Scan Complete! Press Enter to return...{W}")

# --- [4] ALL IN ONE VPN MAKER ---
def vpn_config_maker():
    while True:
        banner()
        print(f"{C}      --- ALL-IN-ONE VPN MAKER ---{W}")
        print(f"{G}[1]{W} HA Tunnel Plus (Host Mode)")
        print(f"{G}[2]{W} HTTP Injector (V2Ray Config)")
        print(f"{G}[3]{W} SSH Server Setup")
        print(f"{G}[4]{W} DNSTT (SlowDNS) Setup")
        print(f"{G}[5]{W} Shadowsocks Generator")
        print(f"{R}[0]{W} Back to Main Menu")
        
        c = input(f"\n{C}Choice > {W}")
        
        if c == '1':
            bug = input(f"{Y}Enter Bug Host: {W}")
            print(f"\n{G}[✔] Setup: Mode: HTTP Custom | Host: {bug} | Port: 80{W}")
            input("\nPress Enter...")
        elif c == '2':
            ip = input(f"{Y}V2Ray IP: {W}")
            uuid_val = input(f"{Y}UUID: {W}")
            bug = input(f"{Y}Bug Host: {W}")
            print(f"\n{G}[✔] Config: {W}{generate_vmess(bug, ip)}")
            input("\nPress Enter...")
        elif c == '3':
            host = input(f"{Y}SSH Host: {W}")
            user = input(f"{Y}User: {W}")
            pw = input(f"{Y}Pass: {W}")
            print(f"\n{G}[✔] SSH: {host} | Port: 22, 443 | {user}:{pw}{W}")
            input("\nPress Enter...")
        elif c == '4':
            ns = input(f"{Y}Nameserver (NS): {W}")
            pub = input(f"{Y}Public Key: {W}")
            ip = input(f"{Y}Target IP: {W}")
            print(f"\n{G}[✔] DNSTT: NS: {ns} | Key: {pub} | IP: {ip}{W}")
            input("\nPress Enter...")
        elif c == '5':
            ip = input(f"{Y}SS IP: {W}")
            port = input(f"{Y}Port: {W}")
            pw = input(f"{Y}Pass: {W}")
            method = input(f"{Y}Method (aes-256-gcm): {W}") or "aes-256-gcm"
            ss_str = f"{method}:{pw}@{ip}:{port}"
            ss_link = "ss://" + base64.b64encode(ss_str.encode()).decode()
            print(f"\n{G}[✔] SS Link: {W}{ss_link}")
            input("\nPress Enter...")
        elif c == '0':
            break

# --- MAIN MENU ---
def main():
    while True:
        banner()
        print(f"{G}[1]{W} Cloudflare IP Checker (Speed Test)")
        print(f"{G}[2]{W} Multi-Operator Bug Scanner & V2Ray Gen")
        print(f"{G}[3]{W} All-In-One VPN Maker (HA/Injector/SSH/DNS)")
        print(f"{R}[0]{W} Exit")
        
        choice = input(f"\n{C}Choice > {W}")
        
        if choice == '1':
            cf_ip_checker()
        elif choice == '2':
            bug_scanner_gen()
        elif choice == '3':
            vpn_config_maker()
        elif choice == '0':
            print(f"{R}GGMU! Victory for United! 🔴{W}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
