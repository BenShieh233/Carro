# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
# from selenium.common.exceptions import NoSuchElementException
import time
from run import read_args

current_dir = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
#options.add_argument('--headless')
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


def page_login(driver, username, password, url):
    driver.get(url)

    username_element =driver.find_element(By.CSS_SELECTOR, 'input[type="text"][autocomplete="username"].el-input__inner')
    username_element.send_keys(username)

    password_element =driver.find_element(By.CSS_SELECTOR, 'input[type="password"][autocomplete="password"].el-input__inner')
    password_element.send_keys(password)

    button = wait_for_element(driver, (By.CSS_SELECTOR, 'button[data-v-1915e4d0][type="submit"].el-button.login-submit-button'))
    button.click()


def in_transit(driver):

    shipments_element = wait_for_element(driver, (By.XPATH, '//span[contains(text(), "Shipments")]'))
    shipments_element.click()

    in_transit_element =  wait_for_element(driver, (By.XPATH, '//span[contains(text(), "In Transit")]'))
    in_transit_element.click()

    all_element = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[1]/ul/div/li[3]/ul/div/li[1]/span'))
    all_element.click()

def advanced_search(driver, address):

    advanced_search = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/section/i[1]')
    advanced_search.click()

    address_input = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/section/div/form/div[2]/div[2]/div/div/div/input'))
    address_input.send_keys(str(address))

    confirm = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/section/div/div/button[1]'))
    confirm.click()

def export_table(driver):
    export_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[7]/div/div/button')
    export_button.click()

    try:

        by_order = wait_for_element(driver, (By.XPATH, "//ul[contains(@id, 'dropdown-menu-')]/li[1]/span[contains(text(), 'By Order')]"))
        by_order.click()
    except:
        print("导出文件失败")

if __name__ == "__main__":

    params = read_args()

    ezeeship_url = params.get('ezeeship_url')
    ezeeship_username = params.get('ezeeship_username')
    ezeeship_password = params.get('ezeeship_password')

    driver = webdriver.Chrome(options = options)
    
    page_login(driver, ezeeship_username, ezeeship_password, ezeeship_url)

    in_transit(driver)

    advanced_search(driver, 1037)

    export_table(driver)

    expected_filename = "Shipment_Information(by order)(all).xls"

    # Wait for the file to be downloaded
    timeout = 120  # Timeout in seconds
    end_time = time.time() + timeout
    while time.time() < end_time:
        if expected_filename in os.listdir(current_dir):  # Check the current directory
            print("成功下载文件")
            break
        time.sleep(1)

    driver.quit()

    


