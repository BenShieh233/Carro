import requests
from bs4 import BeautifulSoup
import json

def make_request(url):
    """Make a respectful request to the given URL."""
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "upgrade-insecure-requests": "1",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-site": "none",
        "sec-fetch-dest": "document",
        "referer": "https://www.google.com/",
        "dnt": "1",
        "sec-gpc": "1",
    }
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an HTTPError for bad requests
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return None

def extract_data_from_script(soup):
    """Extract the encoded text within the script element."""
    script_element = soup.find('script', {'id': '__NEXT_DATA__'})
    if script_element:
        return script_element.text
    else:
        print("No hidden web data found.")
        return None

def parse_json(data_text):
    """Translate the script's language into a JSON format."""
    try:
        data_json = json.loads(data_text)
        return {
            'results': data_json['props']['pageProps']['properties'] or data_json["searchResults"]["home_search"]["results"],
            'total': data_json['props']['pageProps']['totalProperties'] or data_json['searchResults']['home_search']['total']
        }
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def find_properties(state, city, max_pages=1):
    """Scrape Realtor.com search for property preview data."""
    search_results = []

    for page_number in range(1, max_pages + 1):
        # Construct the search URL based on state, city, and page number
        search_url = f"https://www.realtor.com/realestateandhomes-search/{city}_{state.upper()}/pg-{page_number}"

        # Make request and parse search results
        search_response = make_request(search_url)
        if search_response:
            search_soup = BeautifulSoup(search_response.text, 'html.parser')
            data_text = extract_data_from_script(search_soup)

            if data_text:
                search_results.append(parse_json(data_text))

    return search_results if search_results else None

def main():
    """Main function to execute the script."""
    search_results = find_properties("CA", "Los-Angeles")
    if search_results:
        print(json.dumps(search_results, indent=2))

if __name__ == "__main__":
    main()