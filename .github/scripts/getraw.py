import re
import requests
import warnings
from bs4 import BeautifulSoup
import os


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


def main():
    print("Loading raw urls for external...")
    get_raw_urls("external")
    print("Loading raw urls for custom...")
    get_raw_urls("custom")
    print("Loading raw urls for final...")
    get_raw_urls("final")

main()