import requests
import warnings
from bs4 import BeautifulSoup

url = 'https://mediabiasfactcheck.com/fake-news/'

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    response = requests.get(url, verify=False)

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

with open('temp/questionable_sources.txt', 'w') as file:
    for link in soup.find_all('a'):
        if '(' in link.text:
            link_name = link.text.split('(')[-1].replace(')', '').replace('www.', '').lower()
            if '.' in link_name:
                link_name = link_name.replace('https://', '')
                file.write(link_name + '\n')
