import requests
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    """Fetches the HTML content from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

def parse_table(html_content: str, table_id: str) -> list[list[str]]:
    """
    Parses HTML content and extracts data from a specified table.

    Args:
        html_content (str): The HTML content of the page.
        table_id (str): The ID of the table to parse (e.g., "tablepress-2").

    Returns:
        list[list[str]]: A list of lists representing the table data,
                         where the first sublist is the header.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': table_id})

    if not table:
        print(f"Table with ID '{table_id}' not found.")
        return []

    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    data = [headers] # Start with headers

    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        data.append(row_data)

    return data

def get_escooter_data(url: str, include_deprecated: bool = False) -> dict[str, list[list[str]]]:
    """
    Fetches and parses e-scooter data from the specified URL.

    Args:
        url (str): The URL of the e-scooter table page.
        include_deprecated (bool): Whether to include the deprecated models table.

    Returns:
        dict[str, list[list[str]]]: A dictionary containing raw table data.
                                    Keys are 'current' and optionally 'deprecated'.
    """
    html = fetch_html(url)
    if not html:
        return {}

    all_data = {}
    current_models_data = parse_table(html, "tablepress-2")
    if current_models_data:
        all_data['current'] = current_models_data

    if include_deprecated:
        deprecated_models_data = parse_table(html, "tablepress-6")
        if deprecated_models_data:
            # The deprecated table has slightly fewer columns.
            # We'll need to handle this in data_processor, so for now, just store it.
            all_data['deprecated'] = deprecated_models_data

    return all_data

# Example usage (for testing)
if __name__ == "__main__":
    ESCOOTER_URL = "https://www.escooter-treff.de/tabelle/"
    
    print("--- Scraping Current Models ---")
    data = get_escooter_data(ESCOOTER_URL, include_deprecated=False)
    if 'current' in data:
        print(f"Found {len(data['current']) - 1} current e-scooters.")
        # for row in data['current'][:5]: # Print first 5 rows including header for verification
        #     print(row)
    else:
        print("No current e-scooter data found.")

    print("\n--- Scraping All Models (including deprecated) ---")
    all_data = get_escooter_data(ESCOOTER_URL, include_deprecated=True)
    if 'current' in all_data:
        print(f"Found {len(all_data['current']) - 1} current e-scooters.")
    if 'deprecated' in all_data:
        print(f"Found {len(all_data['deprecated']) - 1} deprecated e-scooters.")
        # for row in all_data['deprecated'][:5]: # Print first 5 rows including header for verification
        #     print(row)
    else:
        print("No deprecated e-scooter data found.")