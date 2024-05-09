import requests
import json
from bs4 import BeautifulSoup

def parse_dubaiphone_product_page(url):
    print("Fetching URL:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Page fetched successfully")

        soup = BeautifulSoup(response.content, 'html.parser')

        product_details = []

        # Look for both 'ty-product-feature' and 'ty-product-feature-group'
        for feature_class in ['ty-product-feature', 'ty-product-feature-group']:
            features = soup.find_all('div', {'class': feature_class})
            for feature in features:
                label = feature.find('div', {'class': 'ty-product-feature__label'})
                value = feature.find('div', {'class': 'ty-product-feature__value'})

                if label and value:
                    detail_name = label.text.strip()
                    detail_value = value.text.strip()

                    # Append the formatted detail to the list
                    formatted_detail = f'"{detail_name}" : "{detail_value}"'
                    product_details.append(formatted_detail)

        return product_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)


def main():
    product_url = input("Enter the EGYlaptop  product URL: ")
    product_details = parse_dubaiphone_product_page(product_url)

    if product_details:
        save_to_json(product_details, "Egylaptop_product_details.json")
        print("Product details saved to Egylaptop_product_details.json")
    else:
        print("No product details found.")


if __name__ == "__main__":
    main()
