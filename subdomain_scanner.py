import requests
import concurrent.futures
import argparse

def check_subdomain(domain, subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:
            print(f"[+] Found: {url}")
            return url
    except requests.exceptions.RequestException:
        pass
    return None

def scan_subdomains(domain, wordlist, threads=10):
    found_subdomains = []
    with open(wordlist, "r") as file:
        subdomains = [line.strip() for line in file.readlines()]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_subdomain = {executor.submit(check_subdomain, domain, sub): sub for sub in subdomains}
        for future in concurrent.futures.as_completed(future_to_subdomain):
            result = future.result()
            if result:
                found_subdomains.append(result)
    
    return found_subdomains

def main():
    parser = argparse.ArgumentParser(description="Subdomain Scanner")
    parser.add_argument("domain", help="Target domain (example.com)")
    parser.add_argument("-w", "--wordlist", default="subdomains.txt", help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-o", "--output", help="Save results to a file")
    
    args = parser.parse_args()
    found = scan_subdomains(args.domain, args.wordlist, args.threads)
    
    if args.output:
        with open(args.output, "w") as file:
            for sub in found:
                file.write(sub + "\n")
        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
