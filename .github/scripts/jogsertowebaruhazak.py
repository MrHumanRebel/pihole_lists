import requests
from selenium import webdriver

def extract_urls_from_server_response(base_url, page_start, file_name):
    page_end = None  # Initialize page_end as None

    def scrape_website(url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)
            # Extract data from the loaded webpage using Selenium

            # Close the browser
            driver.quit()
        except Exception as e:
            print(f"An error occurred while scraping the website: {str(e)}")

    while page_end is None or page_start <= page_end:
        url = f"{base_url}&page={page_start}"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if page_end is None:
                page_end = data.get("total_pages", 0)
            urls = [entry['url'] for entry in data['content']]
            texts = []
            for text in urls:
                try:
                    index_slash = text.index("/")
                    cleaned_text = text[:index_slash]
                except ValueError:
                    cleaned_text = text
                try:
                    index_bracket = cleaned_text.index("(")
                    texts.append(cleaned_text[:index_bracket].strip())
                except ValueError:
                    texts.append(cleaned_text.strip())

            with open(file_name, "a") as file:
                for text in texts:
                    file.write(text + "\n")
            
            # Call the web scraping function for this URL
            scrape_website(url)
        else:
            print(f"Failed to retrieve data from the server. Status code: {response.status_code}")

        page_start += 1

def main():
    base_url = 'https://jogsertowebaruhazak.kormany.hu/api/ios/search?page=1&size=100'
    page_start = 1
    file_name = "custom/jogsertowebaruhazak.txt"

    print(f"Loading {file_name}...")
    extract_urls_from_server_response(base_url, page_start, file_name)

if __name__ == "__main__":
    main()
