from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 初始化 WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# 打开网页
driver.get("https://copilot.microsoft.com/chats")

try:
    # 等待并找到输入框
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userInput"))
    )
    input_box.send_keys("Hello, World!"+"(ans within 10 words)")

    # 使用 aria-label 定位并点击发送按钮
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit message']"))
    )
    driver.execute_script("arguments[0].click();", send_button)

    # 等待5秒
    time.sleep(5)

    # 等待并找到输入框 2
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userInput"))
    )
    input_box.send_keys("apple is red!"+"(ans within 10 words)")

    # 使用 aria-label 定位并点击发送按钮 2
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit message']"))
    )
    driver.execute_script("arguments[0].click();", send_button)

    # 等待5秒
    time.sleep(5)

    # 等待并找到所有响应元素中的 <p> 标签
    response_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id$='-content-0'] p"))
    )
    if response_elements:
        last_response = response_elements[-1]
        print("Last Response Text:", last_response.text)


except Exception as e:
    print("An error occurred:", e)
finally:
    # 等代 user 輸入 Enter 关闭 WebDriver
    input("Press Enter to close the browser...")
    driver.quit()