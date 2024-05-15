import requests
import json
from bs4 import BeautifulSoup

def parse_egyptlaptop_product_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the price element
        price_element = soup.find('span', {'class': 'ty-price-num'})
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
    product_url = input("Enter the EgyptLaptop product URL: ")
    product_price = parse_egyptlaptop_product_page(product_url)

    if product_price:
        # Save the price to a JSON file
        price_data = {"price": product_price + " EGP"}
        with open("EgyptLaptop_product_price.json", 'w') as f:
            json.dump(price_data, f, indent=4)
        print(f"Product price saved to EgyptLaptop_product_price.json: {product_price} EGP")
    else:
        print("No price found for the given URL.")

if __name__ == "__main__":
    main()