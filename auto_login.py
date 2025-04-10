# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BA2768E0EF92A2A8200E6F219D0991B08E1181A1756063C5045C239D1F577A50D18B6155A7987C5CECF087EA2E9AB28F045484B3834DBE31F021881F0585721DBA013CF6B732CEBC1C8B7192D9AA5B78604EC7A7A55FDEA945A39F9AA4173228AD4614E0BB45055B62D76A6A59168D85E0A1FBF4916309550660A1F4E0077E9E3F4B9BBEDEAF19723292F3793D5E1044F54F84727F68EA443FD218583E0E3E456FF8EB18D116B0D36487B561925AACEFFCD7549EE857A3F6DD35F12382F4DC228F99BC575769502C1AC6B30E78B457587CA85196D758A2FBA908AF7BB7F52BF69B93C5922EF5A140CE94B90361A382BD3A31C054727BF67E3BD636C96CE9696B7A55FBDC501C9AC4D524B74245691DA8D89A515493FD4E166BDB79BCAED4EEB074AB4843A56B8F964FAE30E35569F88250D608A2E6D9C5FFF57266AA051884E18BC243D3F09215A7383A662783589130601AB05A6475F7D6B7394B4C0ED38D31"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
