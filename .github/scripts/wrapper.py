import requests

def get_addresses_to_block(urls):
    addresses_to_block = set()
    for url in urls:
        lines = process_url(url)
        [addresses_to_block.add(line) for line in lines]
        
    return addresses_to_block
        
def process_url(url):
    response = requests.get(url)
    
    lines = response.text.split("\n")
    return lines


def main():
    with open("temp/urls.txt") as file:
        urls = [line.strip() for line in file]
    
    addresses_to_block = get_addresses_to_block(urls)
    
    with open("complete_blocklist.txt", "w+") as outfile:
        for line in addresses_to_block:
            file.write(line)
        
main()
