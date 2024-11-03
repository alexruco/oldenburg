# main.py

import requests
from bs4 import BeautifulSoup
import time
import random
import csv

# List of user-agent strings to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
]

YOUR_SITE = "suittest.com"
NUM_PAGES = 3  # Number of pages to retrieve
RESULTS_PER_PAGE = 10  # Bing typically shows 10 results per page
CSV_FILENAME = "suittest.csv"

def save_urls_to_csv(urls, filename=CSV_FILENAME):
    """Save a list of URLs to a CSV file, appending without duplicating."""
    # Load existing URLs if the file exists
    existing_urls = set()
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_urls = {row[0] for row in reader}  # Assuming URLs are in the first column
    except FileNotFoundError:
        pass  # File does not exist yet

    # Append new URLs that aren't already in the file
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for url in urls:
            if url not in existing_urls:
                writer.writerow([url])
                print(f"URL saved to CSV: {url}")  # Confirmation of saved URL

def get_search_results(query, num_pages=NUM_PAGES):
    """Performs a multi-page search query on Bing and returns the top result URLs."""
    headers = {'User-Agent': random.choice(user_agents)}  # Randomize user-agent
    results = []

    for page in range(num_pages):
        start_index = page * RESULTS_PER_PAGE + 1
        search_url = f"https://www.bing.com/search?q={query}&first={start_index}"
        response = requests.get(search_url, headers=headers)
        print(f"Response status for page {page + 1}: {response.status_code}")  # Debugging line
        print("Search URL:", search_url)  # Debugging line

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for search results within Bing's result container
        for result_item in soup.find_all('li', {'class': 'b_algo'}):
            a_tag = result_item.find('a', href=True)
            if a_tag:
                link = a_tag['href']
                if link.startswith("http") and 'bing.com' not in link and 'microsoft.com' not in link:
                    results.append(link)
                    print(f"Clean URL extracted: {link}")  # Show cleaned URL

        time.sleep(2)  # Pause to avoid rate limiting

    print(f"Final extracted URLs: {results}")  # Show all extracted URLs
    return list(set(results))  # Remove duplicates

def find_potential_backlink_sites():
    """Find sites to target for backlinks by searching for directory-style queries."""
    query = "no-code testing tools site:.es"  # Updated for broader results
    print(f"Searching potential backlink sites with query: {query}")  # Debugging line
    potential_sites = get_search_results(query)
    print(f"Potential sites found: {potential_sites}")  # Show found potential sites
    return potential_sites

def check_backlink(site_url, target_url):
    """Check if a site mentions a target URL by running a Bing search."""
    query = f"site:{site_url} {target_url}"
    print(f"Checking backlink with query: {query}")  # Debugging line
    results = get_search_results(query, num_pages=1)  # Only need the first page for backlink check
    print(f"Results for backlink check on {site_url}: {results}")  # Show backlink check results
    return any(target_url in result for result in results)

# Step 1: Search for potential backlink sites
print("Step 1: Finding potential backlink sites...")
potential_sites = find_potential_backlink_sites()

# Step 2: Save potential backlink sites to CSV
print("Step 2: Saving potential backlink sites to CSV...")
save_urls_to_csv(potential_sites)

# Step 3: Check each site for existing backlinks
print("Step 3: Checking for existing backlinks...")
not_linking_to_you = []
for site in potential_sites:
    print(f"Checking if {site} links to {YOUR_SITE}")  # Debugging line for each site
    if not check_backlink(site, YOUR_SITE):
        not_linking_to_you.append(site)
        print(f"No backlink found for {YOUR_SITE} on {site}")  # Debugging output
    else:
        print(f"Backlink found for {YOUR_SITE} on {site}")  # Debugging output
    time.sleep(2)  # Avoid triggering rate limits

# Output sites without backlinks
print("Sites not yet linking to your site:")
for site in not_linking_to_you:
    print(site)