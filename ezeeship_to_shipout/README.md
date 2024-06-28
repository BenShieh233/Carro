# 一键检索EzeeShip未登记退货单脚本使用说明
本工具用于自动检索EzeeShip平台上的未登记至Shipout的在途退货单。以下是使用说明，包括运行脚本，安装依赖以及处理常见问题。

- [一键检索EzeeShip未登记退货单脚本使用说明](#一键检索ezeeship未登记退货单脚本使用说明)
  - [项目结构](#项目结构)
  - [脚本文件说明](#脚本文件说明)
    - [webdriver.py](#webdriverpy)
      - [1. wait\_for\_element()](#1-wait_for_element)
      - [2. wait\_until\_visible()](#2-wait_until_visible)
    - [shipout.py](#shipoutpy)
      - [1. page\_login()](#1-page_login)
      - [2. export\_table()](#2-export_table)
      - [3. wait\_for\_file\_download()](#3-wait_for_file_download)
      - [4. shipout\_driver()](#4-shipout_driver)
      - [5. 动图示例](#5-动图示例)
    - [EzeeShip.py](#ezeeshippy)

## 项目结构
确保项目结构如下：
```
dist/
main/
├── main.exe
├── _internal/
    ├── webdriver.py
    ├── EzeeShip.py
    ├── shipout.py
    ├── search.py
    ├── args.txt
    └── other_files.dll
```

## 脚本文件说明

### webdriver.py
用于控制脚本访问页面上某个元素的进程。具体来说，它包括了两种访问函数，`wait_for_element（driver, selector, timout）`与`wait_until_visible(driver, locator, timeout)`，以下是这两种函数的详细功能：

#### 1. wait_for_element()

<details>
  <summary>展开查看代码</summary>

```
def wait_for_element(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        return element
    except Exception as e:
        print("访问超时")
```

- `wait_for_element(driver, selector, timeout)`：创建一个WebDriverWait对象，用于在指定的时间内等待某个条件的发生。
  -  `driver`：这是一个WebDriver实例，通常用于控制浏览器。
  -  `selector`: 这是一个选择器，告诉Selenium需要在页面上找到哪个元素以及如何找到它。
  - `timeout`：这是等待该元素出现的最长时间，如果未能等到该元素加载完成，将会抛出超时异常。
</details>

_________________


#### 2. wait_until_visible()

<details>
  <summary>展开查看代码</summary>

```
def wait_until_visible(driver, locator, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element
    
    except Exception as e:
        print("访问超时")
```
- `wait_until_visible(driver, locator, timeout)`：功能同上，用于等待页面上某个元素变得可见，并在元素可见后执行操作（例如点击）。输入参数与`wait_for_element()`功能一致

</details>

_________________


### shipout.py  
用于执行Shipout中导出退货订单的功能。包括登录、导航到退货管理页面、导出数据以及下载 Excel 表格等步骤。以下为各函数的具体功能：

#### 1. page_login()

<details>
  <summary>展开查看代码</summary>

```
def page_login(driver, username, password, url):
    driver.get(url)

    username_element = driver.find_element(By.CLASS_NAME, 'ez-input__inner')
    username_element.send_keys(username)

    password_element = driver.find_element(By.XPATH, '//input[@type="password" and @autocomplete="off" and contains(@class, "ez-input__inner")]')
    password_element.send_keys(password)


    try:
        button = wait_for_element(driver, (By.CSS_SELECTOR, '.ez-button.login-submit.ez-button--primary.ez-button--medium'))
        button.click()
        print("已成功登陆Shipout")

    except:
        print("Shipout账号或密码输入错误，请重新输入")
        driver.quit()

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
            rt = wait_for_element(driver, (By.XPATH, '/html/body/div[2]/ul/li[1]/div/span')) #'//div[@class="ez-menu-item__content"]//span[contains(text(), "Return Order")]'
            rt.click()
            print("Shipout - 已成功跳转至“退货管理-退货单”页面")
            break
        except:
            retries +=1
            print("Shipout - 当前页面请求失败，重试次数：", retries)
            time.sleep(sleep_interval)
    else:
        print("Shipout - 页面请求已超时，请重新执行文件")
        driver.quit()
```

- `page_login(driver, username, password, url)`：用于访问Shipout登录界面并输入用户名和密码，选择仓库地址，以及跳转至“退货管理-退货单”页面。
</details>

_________________


#### 2. export_table()

<details>
  <summary>展开查看代码</summary>

```
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
        except:
            retries +=1
            print("Shipout - 请求失败，正在尝试重新下载表格，重试次数：", retries)
            time.sleep(sleep_interval)
    else:
        print("Shipout - 页面请求已超时，请重新执行文件")   
        driver.quit() 
```

- `export_table(driver)`：定位至“全部”退货单页面并导出所有数据。由于该页面加载所需时间较长，可能会导致导出文件的请求失败。在这种情况下，该函数会重复执行并记录失败次数直至导出文件，若请求超时，请联系技术人员处理。
</details>

_________________


#### 3. wait_for_file_download()

<details>
  <summary>展开查看代码</summary>

```
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
```
- `wait_for_file_download(prefix, timeout=100)`：遍历当前路径内文件，查询是否已下载生成的Excel表格。
  - `prefix`：读取该路径内文件的前缀，如“WMS_Return_Export”为Shipout输出文件的固定前缀。
  - 
</details>

_________________


#### 4. shipout_driver()

<details>
  <summary>展开查看代码</summary>

```
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
```

- `shipout_driver()`：读取同路径内<u>**args.txt**</u>内的登录账户名和密码，执行上述所有操作，并退出浏览器控制。
</details>

_________________


#### 5. 动图示例
以下为<u>**shipout.py**</u>的自动操作动图示例：
<div style="text-align: center;">
  <img src="Shipout演示.gif" alt="Shipout.py">
</div>

_________________

### EzeeShip.py


  
