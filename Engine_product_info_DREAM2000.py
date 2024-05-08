import requests
import json
from bs4 import BeautifulSoup

def parse_dream2000_product_page(url):
    print("Fetching URL:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Page fetched successfully")

        soup = BeautifulSoup(response.content, 'html.parser')

        product_details = []

        details_container = soup.find('div', {'class': 'product attribute overview'})
        if details_container:
            print("Found product details section")
            table = details_container.find('table')
            if table:
                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        key = columns[1].find('strong').text.strip() + ":"
                        value = columns[1].text.strip().replace(key, '').strip()
                        product_details.append({key: value})
                    elif len(columns) == 4:
                        key = columns[1].find('strong').text.strip() + ":"
                        value = columns[1].text.strip().replace(key, '').strip()
                        product_details.append({key: value})

                        key = columns[3].find('strong').text.strip() + ":"
                        value = columns[3].text.strip().replace(key, '').strip()
                        product_details.append({key: value})
            else:
                description = details_container.find('div', {'class': 'value', 'itemprop': 'description'})
                if description:
                    for line in description.text.strip().split('<br>'):
                        if line:
                            key, _, value = line.partition(': ')
                            product_details.append({key + ":": value.strip()})
            return product_details
        else:
            print("No product details found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def save_to_json(product_details, filename):
    product_dict = {}
    for item in product_details:
        for key, value in item.items():
            product_dict[key] = value
    with open(filename, 'w') as f:
        json.dump(product_dict, f, indent=4)

def main():
    product_url = input("Enter the Dream 2000 product URL: ")
    product_details = parse_dream2000_product_page(product_url)

    if product_details:
        save_to_json(product_details, "dream2000_product_details.json")
        print("Product details saved to dream2000_product_details.json")
    else:
        print("No product details found.")

if __name__ == "__main__":
    main()