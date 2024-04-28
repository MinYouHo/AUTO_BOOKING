from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import time

# Edge Webdriver路徑 
PATH = r'.\msedgedriver.exe'


# Edge Webdriver初始化
options = EdgeOptions()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# options.add_argument()
# options.use_chromium = True
options.add_argument("--enable-chrome-browser-cloud-management")

# options.add_experimental_option("useAutomationExtension", False)

service = EdgeService(executable_path=PATH)
driver = webdriver.Edge(options, service)

# =========== start ==========

# driver = webdriver.Edge(EdgeChromiumDriverManager().install())
driver.get("https://iportal.ntnu.edu.tw/ntnu/")

id = driver.find_element(By.NAME, "muid")
password = driver.find_element(By.NAME, "mpassword")
login = driver.find_element(By.NAME, "Submit22")
id.clear()
password.clear()

# 登入
id.send_keys("41047023S")
password.send_keys("bb123456")
login.click()

# alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
# alert = driver.switch_to.alert
# alert.accept()

# 琴房系統
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.LINK_TEXT, "練習琴房預約系統（限音樂系學生）")))
# element.click()
driver.get(element.get_attribute("href"))

# 琴房狀態
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div")))
element.click()

# 下拉選單
# element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown')))
# print(element.text)
# element.click()
# element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/span[2]/span/ul/li[4]/a')
# element.click()

input("Press Enter to exit...")
# driver.quit()