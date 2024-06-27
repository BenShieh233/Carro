from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from IPython.display import display, Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')

def page_login(driver, username, password, url, wait):
    driver.get(url)
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
    except Exception:
        pass

    username_element = driver.find_element(By.CLASS_NAME, 'ez-input__inner')
    username_element.send_keys(username)


    password_element = driver.find_element(By.XPATH, '//input[@type="password" and @autocomplete="off" and contains(@class, "ez-input__inner")]')
    password_element.send_keys(password)


    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ez-button.login-submit.ez-button--primary.ez-button--medium')))
    button.click()


    try: 
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Upland，CA")]')))
        element.click()

        time.sleep(1)
    except NoSuchElementException:
        print('No such element')   

    # Click on the parent element to expand the submenu
    parent_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "ez-submenu__title") and contains(., "Return")]/..')))
    parent_element.click()            


def return_order(driver, wait):

    try:
        # Wait for 'Return Order' element to be clickable and click it
        rt = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ez-menu-item__content"]//span[contains(text(), "Return Order")]')))
        rt.click()

        # Wait for dropdown toggle element to be clickable and click it
        dropdown_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ez-input-group__prepend"]')))
        dropdown_toggle.click()

        # Find all list options and click on 'RMA #' option if found
        list_options = driver.find_elements(By.CSS_SELECTOR, 'li.ez-select-dropdown__item')
        for option in list_options:
            if option.text == 'RMA #':
                option.click()
                break
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Handle the error as needed

    finally:
        # Ensure to handle cleanup or necessary actions after completion
        pass

def scrape_table(driver, wait):
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.vxe-table--body')))
    # Initialize lists to store table data
    
    data = []

    # Extract fixed left columns
    fixed_left_rows = driver.find_elements(By.CSS_SELECTOR, '.vxe-table--fixed-left-wrapper tbody tr')
    fixed_left_data = []
    for row in fixed_left_rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        row_data = [cell.text for cell in cells]
        fixed_left_data.append(row_data)

    # Extract main table columns
    main_table_rows = driver.find_elements(By.CSS_SELECTOR, '.vxe-table--body tbody tr')
    main_table_data = []
    for row in main_table_rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        row_data = [cell.text for cell in cells]
        main_table_data.append(row_data)

    # Combine the data from fixed columns and main table columns
    for i in range(len(fixed_left_data)):
        combined_row = fixed_left_data[i] + main_table_data[i]
        data.append(combined_row)


    return data

if __name__ == "__main__":

    url = 'https://wms.shipout.com/z/#/dashboard'

    username = 'support@carrohome.com'

    password = 'Carrohome#23'

    driver = webdriver.Chrome(options=options) # options=options
    wait = WebDriverWait(driver, 10)

    page_login(driver, username, password, url, wait)

    return_order(driver, wait)

    all_data = []

    all_data.extend(scrape_table(driver, wait))

    next_button_selector = 'button.btn-next'
    next_button =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, next_button_selector)))
    while True:
        try:          
            # next_button =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, next_button_selector)))

            # Check if the 'Next' button is disabled
            if next_button.get_attribute('disabled'):
                print("Reached the last page.")
                break
            
            # Click the 'Next' button
            next_button.click()
            print("successfully load in the next page")
            # Wait for the new page to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.vxe-table--body')))
            print('successfully find the table')
            # Scrape data from the current page
            all_data.extend(scrape_table(driver, wait))

        except Exception as e:
            print(f"Error occurred during pagination: {e}")
            break

    all_data = [[item for item in row if item] for row in all_data]
    df = pd.DataFrame(all_data)

    df = df.reset_index(drop=True)
    column_names = ["Return Order #", "RMA  #", "Type", "Tracking", "Rcv/Total", "SKU Qty", "SKU","Received Time", "Create Time"]
    df.columns = column_names

    df = df.astype(str)
    df.to_excel('output.xlsx',index=False, header=True)

