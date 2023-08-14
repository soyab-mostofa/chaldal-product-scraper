import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


def setup_logger():
    current_date = time.strftime('%Y-%m-%d')
    log_filename = f'price_log_{current_date}.txt'
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )


def scrape():
    setup_logger()

    # Get the html of the page
    url = "https://chaldal.com/popular"
    driver.get(url)

    # Give the page some time to load

    prev_height = 0
    new_height = driver.execute_script("return document.body.scrollHeight")

    while new_height > prev_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(.5)

        prev_height = new_height
        new_height = driver.execute_script("return document.body.scrollHeight")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get all individual product containers
    all_products = soup.find_all('div', {'class': 'product'})

    # Create a list to hold product information

    for product in all_products:
        name = product.find('div', {'class': 'name'}).text.strip()
        price = product.find('div', {'class': 'price'}).text.strip()

        # Log product information
        logging.info(f"Product Name: {name}")
        logging.info(f"Product Price: {price}")
        logging.info("--------------------------------------------------")

        # Print for verification
        print(f"Product Name: {name}")
        print(f"Product Price: {price}")
        print("--------------------------------------------------")


if __name__ == '__main__':
    scrape()
