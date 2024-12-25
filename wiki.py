import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_content = response.text
else:
    raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table', {'class': 'wikitable'})
if not table:
    raise Exception("Could not find the table in the page.")

data = []


for row in table.find_all('tr')[1:]:  
    cols = row.find_all('td')
    if len(cols) > 4:
        state_name = cols[0].get_text(strip=True)
        population = cols[-3].get_text(strip=True).replace(',', '')  
        data.append([state_name, population])

csv_file = "us_states_population.csv"


with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["State", "Population"])  # Write header
    writer.writerows(data)