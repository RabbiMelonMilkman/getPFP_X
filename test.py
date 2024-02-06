from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests

# Setting up WebDriver with webdriver-manager and Service object
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Optional: runs Chrome in headless mode
options.add_argument('--disable-gpu')  # Optional on Windows, required on Linux
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Target Twitter URL
target_url = "https://twitter.com/Rabbi_Melon/photo"  # Replace with your target Twitter URL

try:
    # Opening the page
    driver.get(target_url)

    # Waiting for the dynamic content to load
    time.sleep(5)

    # Retrieving page source
    page_source = driver.page_source

    # Parsing the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Finding all images
    images = soup.find_all('img')

    # Filtering for the 400x400 image
    target_image_src = None
    for img in images:
        if '400x400' in img.get('src'):  # Adjusted to look for '400x400' in the image URL
            target_image_src = img['src']
            break

    if target_image_src:
        print(f"Found 400x400 Image URL: {target_image_src}")

        # Downloading the image
        response = requests.get(target_image_src)
        if response.status_code == 200:
            # Save the file
            with open("target_image_400x400.jpg", "wb") as file:
                file.write(response.content)
            print("Image successfully downloaded and saved as target_image_400x400.jpg")
        else:
            print("Failed to download the image.")

    else:
        print("No 400x400 image found.")

finally:
    # Closing the browser
    driver.quit()
