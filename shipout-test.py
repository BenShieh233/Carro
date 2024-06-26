from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from IPython.display import display, Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from selenium.common.exceptions import NoSuchElementException
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')
prefs = {"download.default_directory": current_dir}
options.add_experimental_option("prefs", prefs)


def wait_for_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        return element
    except Exception as e:
        return None

def wait_until_visible(driver, locator, timeout=10):
    """
    Wait until an element identified by 'locator' is visible.

    Parameters:
    - driver: WebDriver instance
    - locator: tuple (By, locator_value) identifying the element
    - timeout (optional): maximum time to wait (default: 10 seconds)
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))
    return element

def page_login(driver, username, password, url):
    driver.get(url)

    username_element = driver.find_element(By.CLASS_NAME, 'ez-input__inner')
    username_element.send_keys(username)

    password_element = driver.find_element(By.XPATH, '//input[@type="password" and @autocomplete="off" and contains(@class, "ez-input__inner")]')
    password_element.send_keys(password)


    button = wait_for_element(driver, (By.CSS_SELECTOR, '.ez-button.login-submit.ez-button--primary.ez-button--medium'))
    button.click()

    warehouse_element = wait_for_element(driver, (By.XPATH, '//div[contains(text(), "Upland，CA")]'))
    warehouse_element.click()

    # Click on the parent element to expand the submenu
    time.sleep(2)
    parent_element = wait_for_element(driver, (By.XPATH, '//*[@id="app-root-wrap"]/section/aside/div/div[1]/div/ul/li[3]/div/div/div'))
    parent_element.click() 
  

    rt = wait_until_visible(driver, (By.XPATH, '//div[@class="ez-menu-item__content"]//span[contains(text(), "Return Order")]'))
    rt.click()

def export_table(driver):
    export_button = driver.find_element(By.XPATH, '//*[@id="app-root-wrap"]/section/section/main/div/header/div/div[2]/div[2]/button')
    export_button.click() 

    all_filtered = wait_for_element(driver, (By.XPATH, "//ul[contains(@id, 'dropdown-menu-')]/li[2][normalize-space()='Export All Filtered Orders']"))
    all_filtered.click()


def wait_for_file_download(prefix, timeout=100):
    """
    Wait until a file starting with 'prefix' is downloaded in the current directory.

    Parameters:
    - prefix: Prefix of the filename to search for.
    - timeout (optional): Maximum time to wait in seconds (default: 100).

    Returns:
    - True if the file is found within the timeout period, False otherwise.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        for filename in os.listdir('.'):
            if filename.startswith(prefix):
                print(f"Found downloaded file: {filename}")
                return True
        time.sleep(1)  # Wait before checking again

    print(f"Download timeout reached. File starting with '{prefix}' not found.")
    return False

if __name__ == "__main__":

    url = 'https://wms.shipout.com/z/#/dashboard'

    username = 'support@carrohome.com'

    password = 'Carrohome#23'

    driver = webdriver.Chrome(options=options) # options=options

    page_login(driver, username, password, url)

    export_table(driver)

    prefix = "WMS_Return_Export"

    wait_for_file_download(prefix)

    driver.quit()

