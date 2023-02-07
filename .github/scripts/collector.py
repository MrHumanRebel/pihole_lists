import requests
import os


with open("docs/urls.txt") as file:
    urls = [line.strip() for line in file]


parent_dir = "external"
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)

for i, url in enumerate(urls):
    filename = f"{parent_dir}/{i+1}_{url.split('/')[-1]}"
    with open(filename, "w") as f:
        response = requests.get(url)
        f.write(response.text)
