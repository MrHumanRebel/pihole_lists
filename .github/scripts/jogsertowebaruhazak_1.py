import requests
import warnings
from bs4 import BeautifulSoup

base_url = 'https://jogsertowebaruhazak.kormany.hu/index.html?potolva=0&sulyos_elerhetoseg=1&sulyos_szallitas=1&page='
texts = []

for page in range(1, 39):
    url = base_url + str(page)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.get(url, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        if "www." in link.text:
            texts.append(link.text.replace("www.", "").replace("https://", ""))

cleaned_texts = []
for text in texts:
    try:
        index_slash = text.index("/")
        cleaned_text = text[:index_slash]
    except ValueError:
        cleaned_text = text
    try:
        index_bracket = cleaned_text.index("(")
        cleaned_texts.append(cleaned_text[:index_bracket].strip())
    except ValueError:
        cleaned_texts.append(cleaned_text.strip())

with open("jogsertowebaruhazak_1.txt", "w+") as file:
    for text in cleaned_texts:
        print(text)
        file.write(text + "\n")
