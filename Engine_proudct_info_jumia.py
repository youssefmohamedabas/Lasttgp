import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    details_div = soup.find('div', {'class': 'markup -pam'})
    product_details = []

    if details_div:
        if details_div.find_all('li'):
            # Case 1: Product details are in a list
            product_details = [li.text.strip() for li in details_div.find_all('li')]
        elif details_div.find('table'):
            # Case 2: Product details are in a table
            table = details_div.find('table')
            for row in table.find_all('tr'):
                cols = [col.text.strip() for col in row.find_all('td')]
                if len(cols) == 2:
                    product_details.append(f"{cols[0]}: {cols[1]}")
        elif details_div.find_all('p'):
            # Case 3: Product details are in paragraphs
            product_details = [p.text.strip().replace('\n', ' ') for p in details_div.find_all('p')]
        else:
            # Case 4: Product details are in a single paragraph
            product_details = [details_div.get_text(separator=' ').strip()]
    else:
        # Case 5: No product details found
        product_details = ["No product details found."]

    return product_details

def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)

def main():
    product_url = input("Enter the Jumia product URL: ")
    product_details = scrape_product_details(product_url)

    today = datetime.date.today().strftime('%Y-%m-%d')
    filename = f'jumia_product_details_{today}.json'

    save_to_json(product_details, filename)
    print(f"Product details saved to {filename}")

if __name__ == "__main__":
    main()