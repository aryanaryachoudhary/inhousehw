# main.py
import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils import generate_description
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)



class Website(BaseModel):
    url: str

app = FastAPI()

@app.post("/scrape/")
async def scrape_website(website: Website):
    # Setup the webdriver
    webdriver_service = Service(ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=webdriver_service)
    driver.get(website.url)

    def find_element(driver, by, value):
        try:
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        except NoSuchElementException:
            return None

    # def get_meta_content(driver, name):
    #     element = find_element(driver, By.XPATH, f'//meta[@name="{name}"]')
    #     return element.get_attribute('content') if element else None

    # def get_itemprop_content(driver, itemprop):
    #     element = find_element(driver, By.XPATH, f'//*[@itemprop="{itemprop}"]')
    #     return element.get_attribute('content') if element else None

    def get_link_href(driver, link_texts):
        # First, try to find the footer element
        footer = find_element(driver, By.TAG_NAME, 'footer')

        if footer is not None:
            for link_text in link_texts:
                try:
                    element = WebDriverWait(footer, 5).until(
                        EC.presence_of_element_located((By.LINK_TEXT, link_text))
                    )
                    return element.get_attribute('href')
                except (NoSuchElementException, TimeoutException):
                    continue
        return None

    # product_description = get_meta_content(driver, 'description')
    company_name = driver.title  # Get the title of the webpage

    privacy_policy = get_link_href(driver, ['Privacy Policy', 'Privacy', 'Privacy Notice', 'Privacy Statement'])
    terms_of_use = get_link_href(driver, ['Terms of Use', 'Terms and Conditions', 'Terms', 'Conditions'])

    driver.quit()

    # # use Google to search for the legal name of the company
    # driver = webdriver.Chrome(service=webdriver_service)
    # driver.get(f'https://www.google.com/search?q={company_name} legal name')

    # # Try to get the legal name from the first search result
    # legal_name = find_element(driver, By.CSS_SELECTOR, '.g .rc .s .st').text

    driver.quit()

    scraped_info = {
        # "product_description": product_description if product_description else "Not found",
        "company_name": company_name if company_name else "Not found",
        # "legal_name": legal_name if legal_name else "Not found",
        "privacy_policy": privacy_policy if privacy_policy else "Not found",
        "terms_of_use": terms_of_use if terms_of_use else "Not found",
    }

    return generate_description(scraped_info)


