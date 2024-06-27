from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from IPython.display import display, Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from selenium.common.exceptions import NoSuchElementException
import time
from run import read_args

current_dir = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
# options.add_argument('--headless')
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
    max_retries = 10
    sleep_interval = 2
    retries = 0
    while retries < max_retries:
        try:
            parent_element = wait_for_element(driver, (By.XPATH, '//*[@id="app-root-wrap"]/section/aside/div/div[1]/div/ul/li[3]/div/div/div'))
            parent_element.click()
            rt = wait_for_element(driver, (By.XPATH, '//div[@class="ez-menu-item__content"]//span[contains(text(), "Return Order")]'))
            rt.click()
            print("已成功跳转至下一页面")
            break
        except:
            retries +=1
            print("当前页面请求失败，重试次数：", retries)
            time.sleep(sleep_interval)
  

def export_table(driver):
    export_button = wait_for_element(driver, (By.XPATH, '//*[@id="app-root-wrap"]/section/section/main/div/header/div/div[2]/div[2]/button'))
    export_button.click() 

    all_filtered = wait_for_element(driver, (By.XPATH, "//ul[contains(@id, 'dropdown-menu-')]/li[2][normalize-space()='Export All Filtered Orders']"))
    all_filtered.click()


def wait_for_file_download(prefix, timeout=100):

    end_time = time.time() + timeout
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while time.time() < end_time:
        for filename in os.listdir(script_dir):
            if filename.startswith(prefix):
                print(f"已查找到下载文件: {filename}")
                return True
        time.sleep(1)  # Wait before checking again

    print(f"下载超时，未能在当前目录找到以 '{prefix}' 为前缀的文件名")
    return False

if __name__ == "__main__":

    params = read_args()

    shipout_url = params.get('shipout_url')
    shipout_username = params.get('shipout_username')
    shipout_password = params.get('shipout_password')

    driver = webdriver.Chrome(options=options) 

    page_login(driver, shipout_username, shipout_password, shipout_url)

    export_table(driver)

    prefix = "WMS_Return_Export"

    wait_for_file_download(prefix)

    driver.quit()

