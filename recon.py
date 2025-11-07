#!/usr/bin/env python3
import requests
import argparse
import json
import sys
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

init(autoreset=True)

class ReconTool:
    def __init__(self, domain, wordlist_file=None):
        self.domain = domain
        self.found_subs = []
        self.live_hosts = []
        self.endpoints = set()
        self.wordlist = wordlist_file or self.default_wordlist()
        self.timeout = 3
        
    def default_wordlist(self):
        """common subs to try"""
        return [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1',
            'admin', 'test', 'portal', 'api', 'staging', 'dev', 'development',
            'uat', 'qa', 'demo', 'staging', 'beta', 'app', 'web', 'mail2',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'webdisk'
        ]
    
    def check_subdomain(self, subdomain):
        """probe single subdomain"""
        full_domain = f"{subdomain}.{self.domain}"
        try:
            # try http
            resp = requests.get(f"http://{full_domain}", timeout=self.timeout, allow_redirects=False)
            if resp.status_code < 400:
                self.found_subs.append(full_domain)
                print(f"{Fore.GREEN}[+] {full_domain} ({resp.status_code})")
                return full_domain
        except:
            pass
        
        try:
            # try https
            resp = requests.get(f"https://{full_domain}", timeout=self.timeout, allow_redirects=False, verify=False)
            if resp.status_code < 400:
                if full_domain not in self.found_subs:
                    self.found_subs.append(full_domain)
                    print(f"{Fore.GREEN}[+] {full_domain} (https, {resp.status_code})")
                    return full_domain
        except:
            pass
        
        return None
    
    def enumerate_subs(self, threads=10):
        """threaded subdomain enumeration"""
        print(f"\n{Fore.CYAN}[*] Enumerating subdomains for {self.domain}...")
        print(f"{Fore.CYAN}[*] Using {threads} threads\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_subdomain, sub) for sub in self.wordlist]
            for future in as_completed(futures):
                future.result()
        
        print(f"\n{Fore.GREEN}[+] Found {len(self.found_subs)} subdomains")
        return self.found_subs
    
    def check_common_endpoints(self):
        """probe for common endpoints"""
        print(f"\n{Fore.CYAN}[*] Checking common endpoints...\n")
        
        common = [
            '/.well-known/security.txt',
            '/admin', '/admin/', '/admin/login',
            '/api', '/api/', '/api/v1',
            '/login', '/signin', '/auth',
            '/config', '/config.php', '/config.json',
            '/backup', '/backup.zip',
            '/.git/config', '/.env',
            '/robots.txt', '/sitemap.xml'
        ]
        
        for host in self.found_subs[:5]:  # check first 5 hosts
            for endpoint in common:
                try:
                    url = f"https://{host}{endpoint}"
                    resp = requests.head(url, timeout=2, verify=False)
                    if resp.status_code < 400:
                        print(f"{Fore.YELLOW}[!] Found: {url} ({resp.status_code})")
                        self.endpoints.add(url)
                except:
                    pass
    
    def export_json(self, filename="results.json"):
        """save results to json"""
        data = {
            'domain': self.domain,
            'subdomains': self.found_subs,
            'endpoints': list(self.endpoints),
            'total_subs': len(self.found_subs),
            'timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{Fore.GREEN}[+] Results saved to {filename}")
        return filename
    
    def run(self, check_endpoints=False):
        """run full recon"""
        self.enumerate_subs()
        if check_endpoints and self.found_subs:
            self.check_common_endpoints()
        return {
            'subdomains': self.found_subs,
            'endpoints': list(self.endpoints)
        }


def main():
    parser = argparse.ArgumentParser(description='bug bounty recon tool')
    parser.add_argument('-d', '--domain', required=True, help='target domain')
    parser.add_argument('-o', '--output', help='output file (json)')
    parser.add_argument('--all-checks', action='store_true', help='run all checks')
    parser.add_argument('-t', '--threads', type=int, default=10, help='number of threads')
    
    args = parser.parse_args()
    
    try:
        tool = ReconTool(args.domain)
        results = tool.run(check_endpoints=args.all_checks)
        
        if args.output:
            tool.export_json(args.output)
        else:
            print(f"\n{Fore.CYAN}Results:")
            print(json.dumps(results, indent=2))
    
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
