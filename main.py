import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

all_links_set = set()  # initialize an empty set

for x in range(1, 8):
    r = requests.get(f'https://www.urlhere/page:{x}')
    soup = BeautifulSoup(r.content, 'lxml')
    company = soup.find_all('tr')
    for links in company:
        for link in links.find_all('a', href=True):
            all_links_set.add(baseurl + link['href'])  # add each link to the set

all_links = list(all_links_set)

# create a list to store the data
data_list = []

for link in all_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    # find table on business page
    table = soup.find('table', class_='info_table info_table_wrapper')

    # create a dictionary to store the data for each business
    data = {'Title': soup.find('h1').text.strip()}

    # loop through each row in the table
    for row in table.find_all('td'):
        # check if the label is one of the desired values
        label = row.findNext('td', class_='info_table_label').text.strip()
        if label in ['Contact Person:', 'Phone:', 'Mobile:', 'E-mail:', 'Location:', 'Website:']:
            value = row.findNext('td', class_='info_table_value').text.strip()
            data[label] = value

    # append the dictionary to the list
    data_list.append(data)

# convert the list of dictionaries to a DataFrame and write to a CSV file
df = pd.DataFrame(data_list)
df.to_csv('business_data.csv', index=False)
