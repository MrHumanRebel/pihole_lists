import requests


def get_raw_external():

    folder_url = "https://api.github.com/repos/MrHumanRebel/pihole_lists/contents/external"
    response = requests.get(folder_url)

    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files]

        raw_urls = []
        for name in file_names:
            raw_urls.append(
                f"https://raw.githubusercontent.com/MrHumanRebel/pihole_lists/main/external/{name}")

        with open("external_raw_urls.txt", "w+") as file:
            for url in raw_urls:
                file.write(url + "\n")
    else:
        print("Could not retrieve the contents of the folder.")


def get_raw_custom():
    folder_url = "https://api.github.com/repos/MrHumanRebel/pihole_lists/contents/custom"
    response = requests.get(folder_url)

    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files]

        raw_urls = []
        for name in file_names:
            raw_urls.append(
                f"https://raw.githubusercontent.com/MrHumanRebel/pihole_lists/main/custom/{name}")

        with open("custom_raw_urls.txt", "w+") as file:
            for url in raw_urls:
                file.write(url + "\n")
    else:
        print("Could not retrieve the contents of the folder.")
        
        
def get_raw_final():
    folder_url = "https://api.github.com/repos/MrHumanRebel/pihole_lists/contents/final"
    response = requests.get(folder_url)

    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files]

        raw_urls = []
        for name in file_names:
            raw_urls.append(
                f"https://raw.githubusercontent.com/MrHumanRebel/pihole_lists/main/final/{name}")

        with open("final_raw_urls.txt", "w+") as file:
            for url in raw_urls:
                file.write(url + "\n")
    else:
        print("Could not retrieve the contents of the folder.")
