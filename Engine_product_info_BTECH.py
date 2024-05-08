import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    details_div = soup.find('div', {'class': 'additional-attributes-wrapper table-wrapper'})
    product_details = []

    if details_div:
        table = details_div.find('table', {'class': 'data table additional-attributes'})
        for row in table.find_all('tr'):
            cols = [col.text.strip() for col in row.find_all('th')] + [col.text.strip() for col in row.find_all('td')]
            if len(cols) == 2:
                product_details.append(f"{cols[0]}: {cols[1]}")
    else:
        product_details = ["No product details found."]

    return product_details

def save_to_json(product_details, filename):
    with open(filename, 'w') as f:
        json.dump(product_details, f, indent=4)

def main():
    product_url = input("Enter the BTECH product URL: ")
    product_details = scrape_product_details(product_url)

    today = datetime.date.today().strftime('%Y-%m-%d')
    filename = f'BTECH_product_details_{today}.json'

    save_to_json(product_details, filename)
    print(f"Product details saved to {filename}")

if __name__ == "__main__":
    main()