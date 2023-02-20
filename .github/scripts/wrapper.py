import re
import requests
import warnings
from bs4 import BeautifulSoup
import os

def process_url(url):
    response = requests.get(url, verify=False)

    lines = response.text.split("\n")
    return lines

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
    addresses_to_block.sort()

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
    print("Loading complete_blocklist_creator...")
    complete_blocklist_creator()

main()
