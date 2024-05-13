import requests
from bs4 import BeautifulSoup
import json

def parse_2b_product_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the discounted price element
        price_container = soup.find('span', {'class': 'special-price'})
        if price_container:
            price_element = price_container.find('span', {'class': 'price-wrapper'})
            if price_element:
                product_price = price_element.span.text.strip()
                return product_price
            else:
                print("No discounted price found on the page.")
                return None
        else:
            print("No discounted price found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def main():
    product_url = input("Enter the 2B product URL: ")
    product_price = parse_2b_product_page(product_url)

    if product_price:
        # Save the price to a JSON file
        price_data = {"price": product_price}
        with open("2B_product_price.json", 'w') as f:
            json.dump(price_data, f, indent=4)
        print(f"Product price saved to 2B_product_price.json: {product_price}")
    else:
        print("No price found for the given URL.")

if __name__ == "__main__":
    main()