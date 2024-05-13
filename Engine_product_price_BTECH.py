import requests
import json
from bs4 import BeautifulSoup

def parse_btech_product_price(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the product price element
        price_element = soup.find('span', {'data-price-type': 'finalPrice'})
        if not price_element:
            # If the specific element is not found, try to find it based on class names and attributes
            price_element = soup.find('span', {'data-price-type': 'finalPrice', 'class': 'price'})

        if price_element:
            product_price = price_element.text.strip()
            product_price_with_currency = f"{product_price} EGP"
            return product_price_with_currency
        else:
            print("No price found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def main():
    product_url = input("Enter the BTech product URL: ")
    product_price = parse_btech_product_price(product_url)

    if product_price:
        # Save the price to a JSON file
        price_data = {"price": product_price}
        with open("btech_product_price.json", 'w') as f:
            json.dump(price_data, f, indent=4)
        print(f"Product price saved to btech_product_price.json: {product_price}")
    else:
        print("No price found for the given URL.")

if __name__ == "__main__":
    main()
