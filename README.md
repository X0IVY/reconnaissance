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

## License

MIT
