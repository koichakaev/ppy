from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []

    # Extract all links matching the pattern
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/resume/'):
            full_url = "https://hh.ru" + href
            links.append(full_url)

    return links

def main():
    # Set up Firefox options
    firefox_options = Options()
    firefox_options.headless = True  # Run in headless mode

    # Specify the path to the GeckoDriver executable
    gecko_driver_path = "geckodriver.exe"

    # Initialize the WebDriver
    service = Service(gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # URL to navigate to
        url = "https://hh.ru/search/resume?area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&from=employer_index_header&text=python"

        # Navigate to the URL
        driver.get(url)

        # Sleep for a few seconds to ensure the page is fully loaded
        time.sleep(5)

        # Extract the page source (HTML)
        html_content = driver.page_source

        # Extract links from the HTML content
        links = extract_links(html_content)

        # Print the extracted links
        for link in links:
            print(link)

        # Optional: Save the links to a file
        with open('extracted_links.txt', 'w') as f:
            for link in links:
                f.write(link + '\n')

        # Sleep for 30 seconds (if needed for debugging purposes)
        # time.sleep(30)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()

#не работает оставлю просто так)