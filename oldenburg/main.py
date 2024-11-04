# oldenburg/main.py

import requests
from bs4 import BeautifulSoup
import time
import random
#from utils import save_urls_to_csv, remove_domain_from_results
from oldenburg.utils import save_urls_to_csv, remove_domain_from_results
# List of user-agent strings to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
]

def get_search_results(query, num_pages=3, results_per_page=10):
    """Performs a multi-page search query on Bing and returns the top result URLs."""
    headers = {'User-Agent': random.choice(user_agents)}
    results = []

    for page in range(num_pages):
        start_index = page * results_per_page + 1
        search_url = f"https://www.bing.com/search?q={query}&first={start_index}"
        response = requests.get(search_url, headers=headers)
        #print(f"Response status for page {page + 1}: {response.status_code}")
        #print("Search URL:", search_url)

        soup = BeautifulSoup(response.text, 'html.parser')
        for result_item in soup.find_all('li', {'class': 'b_algo'}):
            a_tag = result_item.find('a', href=True)
            if a_tag:
                link = a_tag['href']
                results.append(link)
                #print(f"Extracted URL: {link}")

        time.sleep(2)

    print(f"All extracted URLs: {results}")
    return results

def find_potential_backlink_sites(domain, query, num_pages=3, results_per_page=10):
    """Find sites to target for backlinks by searching with the provided query."""
    print(f"Searching potential backlink sites with query: {query}")
    raw_results = get_search_results(query, num_pages, results_per_page)
    potential_sites = remove_domain_from_results(raw_results, domain)
    print(f"Potential sites found: {potential_sites}")
    return potential_sites

def check_backlink(site_url, target_url, query):
    """Check if a site mentions a target URL by running a Bing search with the specified query."""
    print(f"Checking backlink with query: {query}")
    results = get_search_results(query, num_pages=1)
    filtered_results = remove_domain_from_results(results, domain=target_url)
    print(f"Results for backlink check on {site_url}: {filtered_results}")
    return any(target_url in result for result in filtered_results)

def run_backlink_checker(domain, query, backlink_query, num_pages=3, results_per_page=10):
    csv_filename = f"{domain.replace('.', '_')}_backlinks.csv"
    
    print("Step 1: Finding potential backlink sites...")
    potential_sites = find_potential_backlink_sites(domain, query, num_pages, results_per_page)

    print("Step 2: Saving potential backlink sites to CSV...")
    save_urls_to_csv(potential_sites, filename=csv_filename)

    print("Step 3: Checking for existing backlinks...")
    not_linking_to_you = []
    for site in potential_sites:
        site_specific_query = f"site:{site} {backlink_query}"
        print(f"Checking if {site} links to {domain} with query: {site_specific_query}")
        if not check_backlink(site, domain, site_specific_query):
            not_linking_to_you.append(site)
            print(f"No backlink found for {domain} on {site}")
        else:
            print(f"Backlink found for {domain} on {site}")
        time.sleep(2)

    print("Sites not yet linking to your site:")
    for site in not_linking_to_you:
        print(site)

# Usage
#run_backlink_checker(domain="suittest.com", query="no-code testing tools site:.es", backlink_query="your backlink query")