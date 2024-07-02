# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
# from selenium.common.exceptions import NoSuchElementException
import time
from search import read_args
from webdriver import wait_for_element

current_dir = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')
prefs = {"download.default_directory": current_dir}
options.add_experimental_option("prefs", prefs)

def page_login(driver, username, password, url):
    driver.get(url)

    username_element =driver.find_element(By.CSS_SELECTOR, 'input[type="text"][autocomplete="username"].el-input__inner')
    username_element.send_keys(username)

    password_element =driver.find_element(By.CSS_SELECTOR, 'input[type="password"][autocomplete="password"].el-input__inner')
    password_element.send_keys(password)

    try:
        button = wait_for_element(driver, (By.CSS_SELECTOR, 'button[data-v-1915e4d0][type="submit"].el-button.login-submit-button'))
        button.click()
        print("已成功登录EzeeShip")
    except:
        print("EzeeShip账号或密码输入错误，请重新输入")
        driver.quit()


def in_transit(driver):

    shipments_element = wait_for_element(driver, (By.XPATH, '//span[contains(text(), "Shipments")]'))
    shipments_element.click()
    print("EzeeShip - 已成功转入“Shipment”页面")


    in_transit_element =  wait_for_element(driver, (By.XPATH, '//span[contains(text(), "In Transit")]'))
    in_transit_element.click()
    print("EzeeShip - 选择“In Transit”订单")


    all_element = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[1]/ul/div/li[3]/ul/div/li[1]/span'))
    all_element.click()
    print('EzeeShip - 点击“All”')


def advanced_search(driver, address):

    advanced_search = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/section/i[1]')
    advanced_search.click()
    print('EzeeShip - 进入Advanced Search')


    address_input = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/section/div/form/div[2]/div[2]/div/div/div/input'))
    address_input.send_keys(address)
    print('EzeeShip - 输入“Recipient Address"仓库地址：', address)


    confirm = wait_for_element(driver, (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/section/div/div/button[1]'))
    confirm.click()
    print('EzeeShip - 点击确认')


def export_table(driver):
    export_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[7]/div/div/button')
    export_button.click()


    try:

        by_order = wait_for_element(driver, (By.XPATH, "//ul[contains(@id, 'dropdown-menu-')]/li[1]/span[contains(text(), 'By Order')]"))
        by_order.click()
        print('EzeeShip - 选择“By Order”，正在尝试导出文件')
    except:
        print("EzeeShip - 导出文件失败")

def wait_for_file_download(prefix, timeout=100):

    end_time = time.time() + timeout
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while time.time() < end_time:
        for filename in os.listdir(script_dir):
            if filename.startswith(prefix):
                print(f"EzeeShip - 已查找到下载文件: {filename}")
                return True
        time.sleep(1)  # Wait before checking again

    print(f"EzeeShip - 下载超时，未能在当前目录找到以 '{prefix}' 为前缀的文件名")

def ezeeship_driver():

    params = read_args()

    ezeeship_url = params.get('ezeeship_url')
    ezeeship_username = params.get('ezeeship_username')
    ezeeship_password = params.get('ezeeship_password')
    ezeeship_address = params.get('ezeeship_recipient_address')

    driver = webdriver.Chrome(options = options)
    
    page_login(driver, ezeeship_username, ezeeship_password, ezeeship_url)

    in_transit(driver)

    advanced_search(driver, ezeeship_address)

    export_table(driver)

    prefix = "Shipment_Information(by order)(all).xls"

    wait_for_file_download(prefix)

    driver.quit()

# if __name__ == "__main__":
#     ezeeship_driver()

    


