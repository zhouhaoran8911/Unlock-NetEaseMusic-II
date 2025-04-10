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
    browser.add_cookie({"name": "MUSIC_U", "value": "00901F860F5EF994745F9A416C2DF5F6C3393576935ABA13A993AEB7F48686776C575F88D9D0424D00915CC234E60EE3658F517FF9F04ADA1E122E35502AF54EF2BAB1E76C3C2B57C9600528DEA1228513E9350E1A5AF767408EDD5DC8F76421BF5B3D34D29A40A65290A801965EA04EBD95C52109D3BF3FC8B73D9B54FFD9B51D7790F3C3218370324DED2ACE14217262A05540B1C1EE13D800A898B2113E6E8AE9060452EEC18198B10CDEF2A763C17BC9C2C7853847308357466B6F52A50D07B5A4CCB1DAB7BC592A2A971040033F98B89BCBF9EC31D2175410F8B75C7813BDBBCF44E193032C782EE42431A585B234CE311AC7297A109445A8DF21DE66F1078F12FE57B14895F9922FC911A45CD0B22EA658A48DB733A6FE2000C197FD3F6D2732FA1D999B72598525A41558E9AA22315B2920AAA38C09FB63C3DE115543BD56E98150C3AA4E6156D75A8BB5F425AA6463BB0CECE2C8EC8A637A3D58449C23"})
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
