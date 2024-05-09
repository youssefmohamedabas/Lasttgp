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

        product_details = []

        # Look for 'product attribute overview'
        overview = soup.find('div', {'class': 'product attribute overview'})
        if overview:
            print("Found product details section")
            value_div = overview.find('div', {'class': 'value'})
            if value_div:
                # Split the text into lines and strip whitespace
                details = value_div.text.strip().split('\n')
                # Remove any empty strings from the list
                details = [detail for detail in details if detail]
                # Append the details to the product_details list
                product_details.extend(details)

        return product_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)


def main():
    product_url = input("Enter the EGY_GAMER_product URL: ")
    product_details = parse_product_page(product_url)

    if product_details:
        save_to_json(product_details, "EGY_GAMER_product_details.json")
        print("Product details saved to EGY_GAMER_product_details.json")
    else:
        print("No product details found.")


if __name__ == "__main__":
    main()
