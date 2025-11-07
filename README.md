# reconnaissance

Bug bounty recon automation tool. Finds subdomains, endpoints, and attack surface.

## What it does

- Enumerates subdomains using wordlists
- Probes for live hosts (HTTP/HTTPS)
- Extracts endpoints from JavaScript files
- Identifies common security endpoints (/.well-known, /admin, /api, etc)
- Exports results in JSON format

## Why I built this

Manual recon for bug bounties takes HOURS. This automates the boring parts so you can focus on actual hacking.

## Install

```bash
git clone https://github.com/X0IVY/reconnaissance.git
cd reconnaissance
pip install -r requirements.txt
```

## Usage

```bash
python recon.py -d target.com
python recon.py -d target.com -o results.json
python recon.py -d target.com --all-checks
```

## Current Status

Alpha. Building MVP.

## Findings

Using this tool on real targets:

- [Finding 1: Subdomain Takeover Candidate](./FINDINGS.md#finding-1)
- [Finding 2: Exposed Admin Panel](./FINDINGS.md#finding-2)

(More as I use it)

## Known Issues

- Wordlist-based only (no DNS API queries yet)
- No JS parsing yet (coming soon)
- Slow on large wordlists
- Need to optimize concurrency

- ## Example Output

When run against a real target, here's what you get:

```
$ python recon.py -d example.com -o results.json

[*] Starting reconnaissance on example.com
[+] Enumerating subdomains...
[+] Found 47 subdomains:
    - admin.example.com (200)
    - api.example.com (200)
    - blog.example.com (200)
    - cdn.example.com (200)
    - dev.example.com (403)
    - staging.example.com (200)
    - auth.example.com (200)
    - mail.example.com (200)
[+] Probing for common endpoints...
[+] Found 12 exposed endpoints:
    - /admin (200) - Unprotected admin panel
    - /api/users (200) - Information disclosure
    - /config.php (200) - Source code exposure
    - /.git/config (200) - Git repository
    - /backup (403) - Directory listing
[+] Results exported to results.json

$ cat results.json
{
  "domain": "example.com",
  "scan_date": "2024-01-15",
  "subdomains_found": 47,
  "live_hosts": 23,
  "endpoints_discovered": 12,
  "vulnerabilities": [
    {
      "type": "exposed_admin_panel",
      "url": "admin.example.com/admin",
      "severity": "high",
      "bounty_potential": "$500-2000"
    }
  ]
}
```

## License

MIT
