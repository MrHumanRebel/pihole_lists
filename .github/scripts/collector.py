import requests
import os

with open("docs/urls.txt") as file:
    urls = [line.strip() for line in file]

parent_dir = "external"
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)

for url in urls:
    filename = f"{parent_dir}/{url.replace('/', '_')}"
    filename = filename.replace("https:__", "")
    with open(filename, "w") as f:
        response = requests.get(url)
        f.write(response.text)

for url in urls:
    filename = f"{parent_dir}/{url.replace('/', '_')}"
    filename = filename.replace("https:__", "")
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            if not line.startswith("#"):
                f.write(line)
