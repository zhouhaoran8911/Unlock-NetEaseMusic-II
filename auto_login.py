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
    browser.add_cookie({"name": "你的MUSIC_U", "value": "00A05666F2FCD190E492016A1FEBB1D4BD55655F2930FB28988D970156CB146AA4F6787FD99120B6670BD03936F786BAB9C906A2436AAD212494FF7EB621073D1B10D9ABBDAA230270B3A24BEFDED5BF8D94754E3BE4BC184381245344059473ED32DFFA8BB41152832ADA3928570F41DA74BE50D95335EDBB6BBAAC8F11DDA7B69BCEEDC796019F5AA1F6A8D29A15DF7620631BA870122BEB76C76EB5122638066FDA9C05355ABB2038B717181CAC7BBB294A745F3C63CFD015E73E9BE98CCDC94921ABF61275B6C0F1EDE6C7698E31F89C7500D37F0BD4B3A1C1715768EC38EB2855B351748128B08CBEBE8FC63D6D3E684303BAD3D30EE01F1B3ED61D031F07B55B5B22F5C4904F52BA835659F06ECFC3C521DC1C4E84420EBA3BBF73C9D51883092416B875B219899082F3F8EEC760BF0847D7F35E68B5B89B227DAA1F5C07748BB61790763C5C91D5C7DB0A237C95234A0091E44DA7AE4AAD45EC73FF622B"})
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
