# 403 Bypass Tool

Tool untuk bypass halaman HTTP 403 (Forbidden) / 401 (Unauthorized) dengan berbagai teknik.

**Develop By Bangyog**

## Installation

```bash
git clone https://github.com/yourusername/403bypass.git
cd 403bypass
pip install requests
```

## Usage

```bash
python3 403by.py -u <URL> <mode>
```

### Example

```bash
python3 403by.py -u http://target.com/admin --exploit
```

## Modes

| Mode | Description |
|------|-------------|
| `--header` | HTTP Header Bypass (51+ header payloads) |
| `--protocol` | Protocol Based Bypass (HTTP/HTTPS scheme) |
| `--port` | Port Based Bypass (X-Forwarded-Port) |
| `--HTTPmethod` | HTTP Method Bypass (11 methods) |
| `--encode` | URL Encode Bypass (path traversal) |
| `--SQLi` | ModSecurity & libinjection Bypass |
| `--exploit` | Run all bypass modes (full scan) |

## Features

- **Header Injection** — X-Forwarded-For, X-Originating-IP, X-Custom-IP-Authorization, X-Original-URL, X-Rewrite-URL, and 45+ more headers
- **Protocol Switch** — HTTP ↔ HTTPS, X-Forwarded-Scheme
- **Port Manipulation** — X-Forwarded-Port (80, 443, 8080, 8443, 4443)
- **HTTP Method Fuzzing** — GET, POST, PUT, HEAD, OPTIONS, TRACE, PATCH, TRACK, CONNECT, UPDATE, LOCK
- **URL Encoding** — 245+ path traversal and encoding bypass payloads
- **SQLi Bypass** — ModSecurity & libinjection filter evasion
- **Plain Output** — Status code tanpa warna

## Output

```
[+] X-Rewrite-URL Payload: Status: 200, Length : 13292 👌
  curl -ks -H 'X-Rewrite-URL: /admin' -X GET 'http://target.com/admin'
[x] X-Forwarded-For Payload: Status: 403, Length : 31
```

| Prefix | Status | Description |
|--------|--------|-------------|
| `[+]` | 2xx | Success |
| `[x]` | 4xx | Denied |
| `[x]` | 3xx | Redirect |
| `[x]` | 5xx | Error |

## License

MIT
