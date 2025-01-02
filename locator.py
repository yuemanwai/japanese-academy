from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 初始化 WebDriver
options = webdriver.ChromeOptions()
# 使用無界面模式
options.add_argument('--mute-audio')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
options.add_argument('--enable-javascript')
# options.add_argument('--remote-debugging-port=9222')  # 添加遠程調試端口
options.binary_location = "/usr/bin/google-chrome"  # 確保 Chrome 瀏覽器的路徑正確

# 設置 ChromeDriver 的路徑
chrome_driver_path = "./chromedriver-linux64/chromedriver"  # 根據實際情況設置路徑
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 設置超時
# driver.implicitly_wait(50)  # 隱式等待
# driver.set_script_timeout(50)  # 設置腳本超時
# driver.set_page_load_timeout(50)  # 設置頁面加載超時

# 打开网页
print("Opening webpage...")
driver.get("https://copilot.microsoft.com/chats")

try:
    # 等待并找到输入框
    print("Waiting for input box...")
    input_box = WebDriverWait(driver, 10).until(  # 增加等待時間到10秒
        EC.presence_of_element_located((By.ID, "userInput"))
    )
    print("Input box found.")
    input_box.send_keys("Hello, World!"+"(ans within 10 words)")

    # 使用 aria-label 定位并点击发送按钮
    print("Waiting for send button...")
    send_button = WebDriverWait(driver, 10).until(  # 增加等待時間到10秒
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit message']"))
    )
    print("Send button found.")
    driver.execute_script("arguments[0].click();", send_button)

    # 等待5秒
    time.sleep(5)

    # 等待并找到所有响应元素中的 <p> 标签
    print("Waiting for response elements...")
    response_elements = WebDriverWait(driver, 10).until(  # 增加等待時間到10秒
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id$='-content-0'] p"))
    )
    print("Response elements found.")
    if response_elements:
        last_response = response_elements[-1]
        print("Last Response Text:", last_response.text)

except Exception as e:
    print("An error occurred:", e)
    print("Error details:", e.__class__.__name__, e)
    if hasattr(e, 'msg'):
        print("Error message:", e.msg)

finally:
    # 等代 user 輸入 Enter 关闭 WebDriver
    # input("Press Enter to close the browser...")
    driver.quit()