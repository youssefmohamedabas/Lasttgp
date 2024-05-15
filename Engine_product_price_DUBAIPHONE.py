import requests
import json
from bs4 import BeautifulSoup

def parse_dubai_phone_store_product_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the sale price element
        sale_price_element = soup.find('ins', {'class': 'highlight'})
        if sale_price_element:
            sale_price = sale_price_element.find('span', {'class': 'woocommerce-Price-amount amount'}).text.strip()
            return sale_price
        else:
            print("No sale price found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def main():
    product_url = input("Enter the Dubai Phone Store product URL: ")
    product_price = parse_dubai_phone_store_product_page(product_url)

    if product_price:
        # Save the price to a JSON file
        price_data = {"price": product_price}
        with open("Dubai_phone_store_price.json", 'w') as f:
            json.dump(price_data, f, indent=4)
        print(f"Product price saved to Dubai_phone_store_price.json: {product_price}")
    else:
        print("No price found for the given URL.")

if __name__ == "__main__":
    main()