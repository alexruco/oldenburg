import csv

def save_urls_to_csv(urls, filename):
    """Save a list of URLs to a CSV file, appending without duplicating."""
    existing_urls = set()
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_urls = {row[0] for row in reader}  # Assuming URLs are in the first column
    except FileNotFoundError:
        pass  # File does not exist yet

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for url in urls:
            if url not in existing_urls:
                writer.writerow([url])
                print(f"URL saved to CSV: {url}")

def remove_domain_from_results(results, domain):
    """Filters out URLs from a specific domain."""
    filtered_results = [url for url in results if not url.startswith("http") or (domain not in url)]
    print(f"Filtered results (without domain '{domain}'): {filtered_results}")
    return filtered_results
