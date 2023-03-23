import requests
import warnings
from bs4 import BeautifulSoup



def questionable_sources():
    url = 'https://mediabiasfactcheck.com/fake-news/'
    print(url)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.get(url, verify=False)

    response = requests.get(url, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    with open('custom/questionable_sources.txt', 'w+') as file:
        for link in soup.find_all('a'):
            if '(' in link.text:
                link_name = link.text.split(
                    '(')[-1].replace(')', '').replace('www.', '').lower()
                if '.' in link_name:
                    link_name = link_name.replace('https://', '')
                    file.write(link_name + '\n')


def main():
    questionable_sources()

main()