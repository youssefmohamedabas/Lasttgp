import requests
import json
from bs4 import BeautifulSoup

def parse_product_page(url):
    print("Fetching URL:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Page fetched successfully")

        soup = BeautifulSoup(response.content, 'html.parser')

        product_details = {}

        # Look for 'product-stats'
        stats = soup.find('div', {'class': 'product-stats'})
        if stats:
            print("Found product details section")
            list_items = stats.find_all('li')
            for item in list_items:
                # Split the text into key and value
                key, value = item.text.split(':', 1)
                # Remove any empty strings from the list
                if key and value:
                    # Append the details to the product_details dictionary
                    product_details[key.strip()] = value.strip()

        return product_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)

def main():
    product_url = input("Enter the GAMERSLOUNGE_product URL: ")
    product_details = parse_product_page(product_url)

    if product_details:
        save_to_json(product_details, "GAMERSLOUNGE_product_details.json")
        print("Product details saved to GAMERSLOUNGE_product_details.json")
    else:
        print("No product details found.")

if __name__ == "__main__":
    main()
