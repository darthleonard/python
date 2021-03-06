import subprocess
import re
import argparse
import threading
import random

def get_arguments():
    parser = argparse.ArgumentParser(description='periodic macchanger')
    parser.add_argument('-i', '--interface', help = 'interface to edit', default = 'wlp6s0', required = False)
    parser.add_argument('-m', '--mac', help = 'new mac address', default = '00:11:22:33:44:55', required = False)
    parser.add_argument('-t', '--time_interval', help = 'time interval in seconds', type=int, default = 0, required = False)
    return parser.parse_args()

def execute_change_mac_commands(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw","ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(b"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)

    print("[-] Could not read MAC address.")
    return None

def change_mac(new_mac, interface):
    current_mac = get_current_mac(interface)
    print("   Attempting to change %s > %s" % (current_mac, new_mac))
    if current_mac == new_mac:
        print("[-] Interface %s address already is %s" % (interface, new_mac))
    else:
        execute_change_mac_commands(interface, new_mac)
        print("Current MAC = %s" % current_mac)

def random_mac():
    return ":".join(map(str, (hex(random.randrange(16,255)).lstrip('0x') for _ in range(6))))

def start_loop(args):
    threading.Timer(args.time_interval, start_loop, [args]).start()
    change_mac(random_mac(), args.interface)

def main():
    args = get_arguments()
    if args.time_interval == 0:
        change_mac(random_mac(), args.interface)
    else:
        start_loop(args)

if __name__ == '__main__':
    main()
