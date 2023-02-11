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


def external_url_collector():

    with open("docs/urls.txt") as file:
        urls = [line.strip() for line in file]

    parent_dir = "external"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    for url in urls:
        filename = f"{parent_dir}/{url.replace('/', '_')}"
        filename = filename.replace("https:__", "")
        print(filename)
        with open(filename, "w") as f:
            response = requests.get(url, verify=False)
            text = response.text.rstrip()
            f.write(text)
        with open(filename, "r") as f:
            lines = f.readlines()
        with open(filename, "w") as f:
            for line in lines:
                if not line.startswith("#") and "." in line:
                    line = line.replace("www.", "")
                    line = line.replace("https://", "")
                    line = line.replace("http://", "")
                    f.write(line)



def get_raw_urls(folder):
    folder_url = f"https://api.github.com/repos/MrHumanRebel/pihole_lists/contents/{folder}"
    response = requests.get(folder_url)

    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files]

        raw_urls = []
        for name in file_names:
            raw_urls.append(
                f"https://raw.githubusercontent.com/MrHumanRebel/pihole_lists/main/{folder}/{name}")

        with open(f"{folder}_raw_urls.txt", "w+") as file:
            for url in raw_urls:
                file.write(url + "\n")
    else:
        print("Could not retrieve the contents of the folder.")


def get_addresses_to_block(urls):
    addresses_to_block = set()
    for url in urls:
        lines = process_url(url)
        for line in lines:
            if not line.startswith("#"):
                line = line.replace("www.", "")
                line = line.replace("https://", "")
                line = line.replace("http://", "")
                addresses_to_block.add(line)
    return addresses_to_block


def process_url(url):
    response = requests.get(url, verify=False)

    lines = response.text.split("\n")
    return lines


def complete_blocklist_creator():
    parent_dir = "final"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    custom_raw_urls = []
    external_raw_urls = []
    with open("custom_raw_urls.txt") as custom_file:
        custom_raw_urls = [line.strip() for line in custom_file]
    with open("external_raw_urls.txt") as external_file:
        external_raw_urls = [line.strip() for line in external_file]

    urls = custom_raw_urls + external_raw_urls
    addresses_to_block = list(get_addresses_to_block(urls))
    addresses_to_block.sort()  # Sort addresses_to_block alphabetically

    file_count = 1
    current_file_size = 0
    filename = f"final/complete_blocklist_{file_count}.txt"
    with open(filename, "w+") as outfile:
        for line in addresses_to_block:
            if "." in line:
                line = line.replace("www.", "")
                line = line.replace("https://", "")
                line = line.replace("http://", "")
                current_file_size += len(line.encode())
                if current_file_size >= 5000000:  # 5 MB
                    file_count += 1
                    print(current_file_size)
                    current_file_size = 0
                    filename = f"final/complete_blocklist_{file_count}.txt"
                    outfile.close()
                    outfile = open(filename, "w+")
                outfile.write(line + "\n")


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
    print("Loading questionable_sources...")
    questionable_sources()
    print("Loading external_url_collector...")
    external_url_collector()
    print("Loading complete_blocklist_creator...")
    complete_blocklist_creator()
    print("Loading raw urls for external...")
    get_raw_urls("external")
    print("Loading raw urls for custom...")
    get_raw_urls("custom")
    print("Loading raw urls for final...")
    get_raw_urls("final")


main()
