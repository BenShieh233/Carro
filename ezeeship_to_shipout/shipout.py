from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from search import read_args
from webdriver import wait_for_element, wait_until_located, show_screen
from selenium.common.exceptions import StaleElementReferenceException

current_dir = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')
prefs = {"download.default_directory": current_dir}
options.add_experimental_option("prefs", prefs)

def page_login(driver, username, password, url):
    driver.get(url)
    
    username_element = driver.find_element(By.CLASS_NAME, 'ez-input__inner')
    username_element.send_keys(username)
    
    password_element = driver.find_element(By.XPATH, '//input[@type="password" and @autocomplete="off" and contains(@class, "ez-input__inner")]')
    password_element.send_keys(password)
    
    try:
        button = wait_for_element(driver, (By.CSS_SELECTOR, '.ez-button.login-submit.ez-button--primary.ez-button--medium'))
        button.click()
        print("已成功登录Shipout")

    except Exception as e:
        print(f"Shipout账号或密码输入错误，请重新输入。错误信息：{e}")
        show_screen(driver)
        driver.quit()
    
    retries = 5
    while retries > 0:
        try:
            warehouse_element = wait_until_located(driver, (By.XPATH, '//div[contains(text(), "Upland，CA")]'))
            warehouse_element.click()
            print("Shipout - 已成功进入仓库页面：“Upland Warehouse”")
            break
        except StaleElementReferenceException as e:
            print(f"Shipout - 未能锁定该页面，重试中。错误信息：{e}")
            retries -= 1
        except Exception as e:
            print(f"Shipout - 未能锁定该页面。错误信息：{e}")
            show_screen(driver)
            break
    else:
        print("Shipout - 无法定位仓库页面，跳过此步骤")

    # Click on the parent element to expand the submenu
    max_retries = 10
    sleep_interval = 2
    retries = 0
    while retries < max_retries:
        try:
            parent_element = wait_for_element(driver, (By.XPATH, '//*[@id="app-root-wrap"]/section/aside/div/div[1]/div/ul/li[3]/div/div/div'))
            parent_element.click()
            rt = wait_for_element(driver, (By.XPATH, '/html/body/div[2]/ul/li[1]/div/span')) #'//div[@class="ez-menu-item__content"]//span[contains(text(), "Return Order")]'
            rt.click()
            print("Shipout - 已成功跳转至“退货管理-退货单”页面")
            break
        except:
            retries +=1
            print("Shipout - 当前页面请求失败，重试次数：", retries)
            show_screen(driver)
            time.sleep(sleep_interval)
    else:
        print("Shipout - 页面请求已超时，请重新执行文件")
        driver.quit()
  

def export_table(driver):
    max_retries = 10
    sleep_interval = 2
    retries = 0
    while retries < max_retries:
        try: 
            all_button = wait_for_element(driver, (By.XPATH, '//*[@id="tab-0"]'))
            all_button.click()
            
            print("Shipout - 已选择查看“全部”退货单，正在尝试导出所有表格")

            export_button = wait_for_element(driver, (By.XPATH, '//*[@id="app-root-wrap"]/section/section/main/div/header/div/div[2]/div[2]/button'))
            export_button.click()
            print("Shipout - 已选择“导出”")
            

            all_filtered = wait_for_element(driver, (By.XPATH, "//ul[contains(@id, 'dropdown-menu-')]/li[2][normalize-space()='Export All Filtered Orders' or normalize-space()='导出当前所有数据']"))
            all_filtered.click()
            
            print("Shipout - 已选择“导出当前所有数据”")
            print("Shipout - 已导出退货单表格")
            break
        except Exception as e:
            retries +=1
            print(f"Shipout - 请求失败，正在尝试重新下载表格，重试次数：{retries}。错误信息：{e}")
            show_screen(driver)
            time.sleep(sleep_interval)
    else:
        print("Shipout - 页面请求已超时，请重新执行文件")   
        driver.quit() 


def wait_for_file_download(prefix, timeout=100):

    end_time = time.time() + timeout
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while time.time() < end_time:
        for filename in os.listdir(script_dir):
            if filename.startswith(prefix):
                print(f"Shipout - 已查找到下载文件: {filename}")
                return True
        time.sleep(1)  # Wait before checking again

    print(f"Shipout - 下载超时，未能在当前目录找到以 '{prefix}' 为前缀的文件名")
    return False

def shipout_driver():

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

# if __name__ == "__main__":
#     shipout_driver()

