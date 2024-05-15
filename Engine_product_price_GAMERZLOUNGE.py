import requests
import json
from bs4 import BeautifulSoup

def parse_gamerzlounge_product_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the price element
        price_element = soup.find('div', {'class': 'product-price'})
        if price_element:
            product_price = price_element.text.strip()
            return product_price
        else:
            print("No price found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def main():
    product_url = input("Enter the GamerzLounge product URL: ")
    product_price = parse_gamerzlounge_product_page(product_url)

    if product_price:
        # Save the price to a JSON file
        price_data = {"price": product_price}
        with open("GamerzLounge_product_price.json", 'w') as f:
            json.dump(price_data, f, indent=4)
        print(f"Product price saved to GamerzLounge_product_price.json: {product_price}")
    else:
        print("No price found for the given URL.")

if __name__ == "__main__":
    main()