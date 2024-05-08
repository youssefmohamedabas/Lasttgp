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

        details_container = soup.find('div', {'class': 'w-full flex flex-col items-start justify-start gap-0'})
        if details_container:
            print("Found product details section")
            for detail_row in details_container.find_all('div', {'class': 'p-5'}):
                h4_tag = detail_row.find('h4')
                p_tags = detail_row.find_all('p')

                # Check if there is at least one p tag with text
                if any(p.text.strip() for p in p_tags):
                    # Get text from the last non-empty p tag
                    detail_value = None
                    for p_tag in reversed(p_tags):
                        if p_tag.text.strip():
                            detail_value = p_tag.text.strip()
                            break

                    # If h4 is empty, use a default key
                    detail_name = h4_tag.text.strip() if h4_tag else "Attributes"

                    # Append the formatted detail to the list
                    formatted_detail = f'"{detail_name}" : {detail_value}'
                    product_details.append(formatted_detail)

            return product_details
        else:
            print("No product details found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None
def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)


def main():
    product_url = input("Enter the Dubai phone product URL: ")
    product_details = parse_dubaiphone_product_page(product_url)

    if product_details:
        save_to_json(product_details, "dubai_phone_product_details.json")
        print("Product details saved to dubai_phone_product_details.json")
    else:
        print("No product details found.")


if __name__ == "__main__":
    main()
