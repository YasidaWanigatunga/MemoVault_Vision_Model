import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# URL of the Unsplash page
url = "https://www.istockphoto.com/search/2/image?alloweduse=availableforalluses&mediatype=photography&phrase=Vacation%2FTravel&sort=best"

# Set up Chrome options for Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")

# Automatically set up ChromeDriver with webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the Unsplash page
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
images = soup.find("div", class_="DE6jTiCmOG8IPNVbM7pJ").find_all("a",class_="Up7tj_EQVFh6e6sV17Ud")

driver.quit()

# Create output folder for images
output_folder = "Vacation_Travel"
os.makedirs(output_folder, exist_ok=True)

target_resolutions = ["256", "512"]

a=1
# Download each image if it matches the desired resolution
for i, img in enumerate(images, 1):
    img_tag = img.find("img",class_="yGh0CfFS4AMLWjEE9W7v")
    # srcset = img_tag.get("srcset", "") if img_tag else ""
    srcset = img_tag.get("src", "") if img_tag else ""

    # if srcset:
    #     try:
    #         sources = [entry.strip().split(" ") for entry in srcset.split(",")]
    #         img_url = None
    #         for url, size in sources:
    #             if size == "500w":
    #                 img_url = url
    #                 width = "256"
    #                 break

    if srcset:
        file_extension = ".jpg"
        file_name = os.path.join(output_folder, f"{a}{file_extension}")


        img_data = requests.get(srcset).content
        with open(file_name, "wb") as file:
            file.write(img_data)

        print(f"Saved image {a} at 256w as {file_name}")
        a = a + 1
    else:
        print(f"No 256w URL found for image {i}")

        # except requests.RequestException as e:
        #     print(f"Failed to download image {i} from {img_url}: {e}")
    # else:
    #     print(f"Image {i} has no valid srcset attribute.")
