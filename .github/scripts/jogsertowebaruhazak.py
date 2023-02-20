import re
import requests
import warnings
from bs4 import BeautifulSoup
import os


def jogserto_webaruhazak(base_url, page_start, page_end, file_name):
    texts = []
    print(base_url)

    for page in range(page_start, page_end + 1):
        url = base_url + str(page)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = requests.get(url, verify=False)

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            if "www." in link.text:
                texts.append(link.text.replace(
                    "www.", "").replace("https://", ""))

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

    with open(file_name, "w+") as file:
        for text in cleaned_texts:
            file.write(text + "\n")


def main():
    print("Loading jogsertowebaruhazak_1.txt...")
    jogserto_webaruhazak(
        'https://jogsertowebaruhazak.kormany.hu/index.html?potolva=0&sulyos_elerhetoseg=1&sulyos_szallitas=1&page=',
        1, 39, "custom/jogsertowebaruhazak_1.txt"
    )
    print("Loading jogsertowebaruhazak_2.txt...")
    jogserto_webaruhazak(
        'https://jogsertowebaruhazak.kormany.hu/?sulyos_csoda=1&sulyos_szallitas=1&page=',
        1, 11, "custom/jogsertowebaruhazak_2.txt"
    )


main()
