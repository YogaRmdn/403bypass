# 403 Bypass Sakti

Tool untuk bypass 403 Forbidden dengan berbagai teknik.

## Installation

```bash
git clone https://github.com/yourusername/403bypass.git
cd 403bypass
pip install requests
```

## Usage

```bash
python3 403bypass.py -u <target_url>
```

### Options

| Flag | Description |
|------|-------------|
| `-u`, `--url` | Target URL (e.g., `https://example.com/admin`) |
| `-p`, `--proxy` | Proxy (e.g., `http://127.0.0.1:8080`) |
| `-t`, `--threads` | Thread count (default: 30) |
| `--timeout` | Request timeout in seconds (default: 5) |
| `--cookie` | Cookie string |
| `--headers` | Additional headers (`key:value,key2:value2`) |
| `--all` | Run all bypass techniques |
| `--headers-only` | Only test header bypass |
| `--path-only` | Only test path bypass |
| `--method-only` | Only test HTTP method bypass |
| `--payload-only` | Only test payload bypass |

### Examples

```bash
# Basic
python3 403bypass.py -u https://target.com/admin

# With proxy
python3 403bypass.py -u https://target.com/admin -p http://127.0.0.1:8080

# With cookie
python3 403bypass.py -u https://target.com/admin --cookie "session=abc123"

# Run all techniques
python3 403bypass.py -u https://target.com/admin --all

# Specific module only
python3 403bypass.py -u https://target.com/admin --headers-only
python3 403bypass.py -u https://target.com/admin --path-only
```

## Techniques

### Header Bypass (30+)
- `X-Forwarded-For`, `X-Real-IP`, `X-Client-IP` - IP spoofing
- `X-Original-URL`, `X-Rewrite-URL` - URL override
- `X-Custom-IP-Authorization` - Custom auth bypass
- `X-HTTP-Method-Override` - Method override
- Various forward headers

### Path Bypass (30+)
- `..;/` - Path traversal
- `%2e`, `%2e%2e/` - URL encoding
- `//`, `/./` - Path normalization
- `*`, `?.js`, `.json` - Extension bypass
- Null byte, tab, newline injection

### Method Bypass (9)
- GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD, CONNECT, TRACE

### Payload Bypass (15+)
- Query string injections
- Fragment tricks
- Combined path manipulations

## Disclaimer

For educational purposes and authorized testing only.
