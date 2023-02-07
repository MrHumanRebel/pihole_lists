import requests

with open("temp/urls.txt") as file:
    urls = [line.strip() for line in file]


with open("complete_blocklist.txt", "w") as outfile:
    for url in urls:
        response = requests.get(url)
        outfile.write(response.text)
