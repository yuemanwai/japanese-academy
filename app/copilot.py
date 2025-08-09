from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import os
from pyvirtualdisplay import Display

class CopilotChat:
    def __init__(self, chrome_driver_path, chrome_binary_path="/usr/bin/google-chrome", debug=False, show_browser=False):
        self.debug = debug
        self.show_browser = show_browser
        
        # 只在不需要顯示瀏覽器時才啟動虛擬顯示器
        if not show_browser:
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()
        else:
            self.display = None
            
        options = webdriver.ChromeOptions()
        
        if not show_browser:
            options.add_argument('--headless')  # 無頭模式
        
        options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        options.add_argument('--no-sandbox')  # 禁用沙盒模式
        options.add_argument('--disable-software-rasterizer')  # 禁用軟件光柵化器
        options.add_argument('--disable-dev-shm-usage')  # 避免共享內存問題
        options.add_argument('--window-size=1920,1080')  # 設定視窗大小
        
        if chrome_binary_path:
            options.binary_location = chrome_binary_path  # 確保 Chrome 瀏覽器的路徑正確

        # 設置 ChromeDriver 的路徑
        self.service = Service(executable_path=chrome_driver_path)
        
        if self.debug:
            print(f"Using Chrome binary: {chrome_binary_path}")
            print(f"Using ChromeDriver: {chrome_driver_path}")
            print(f"Show browser: {show_browser}")
            
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def chat(self, input_text, word_limit, condition):
        # 打開網頁
        if self.debug:
            print("Opening webpage...")
        self.driver.get("https://copilot.microsoft.com/chats")
        
        if self.debug:
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")

        try:
            # 等待頁面完全載入
            time.sleep(3)
            
            # 檢查是否有登入要求或其他阻擋
            if self.debug:
                print("Checking page content...")
                page_source_snippet = self.driver.page_source[:1000]
                print(f"Page source snippet: {page_source_snippet}")
            
            # 等待並找到輸入框
            if self.debug:
                print("Waiting for input box...")
            
            # 嘗試多種可能的輸入框選擇器
            input_selectors = [
                (By.ID, "userInput"),
                (By.CSS_SELECTOR, "textarea[placeholder*='Ask me anything']"),
                (By.CSS_SELECTOR, "textarea"),
                (By.CSS_SELECTOR, "[data-testid='input-turn-counter']"),
                (By.CSS_SELECTOR, ".ck-editor__editable")
            ]
            
            input_box = None
            for selector_type, selector in input_selectors:
                try:
                    if self.debug:
                        print(f"Trying selector: {selector_type}, {selector}")
                    input_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((selector_type, selector))
                    )
                    if self.debug:
                        print(f"Found input box with selector: {selector}")
                    break
                except:
                    if self.debug:
                        print(f"Selector failed: {selector}")
                    continue
            
            if not input_box:
                if self.debug:
                    print("No input box found. Available elements:")
                    elements = self.driver.find_elements(By.TAG_NAME, "input")
                    elements.extend(self.driver.find_elements(By.TAG_NAME, "textarea"))
                    for i, elem in enumerate(elements):
                        print(f"Element {i}: tag={elem.tag_name}, id={elem.get_attribute('id')}, class={elem.get_attribute('class')}")
                raise Exception("找不到輸入框")
                
            if self.debug:
                print("Input box found.")
            message = f"(Please MUST answer me no more than {word_limit} words, and {condition}.) {input_text}"
            if self.debug:
                print("Message to send:", message)
            input_box.send_keys(message)

            # 使用多種方式定位並點擊發送按鈕
            if self.debug:
                print("Waiting for send button...")
            
            send_selectors = [
                (By.CSS_SELECTOR, "button[aria-label='Submit message']"),
                (By.CSS_SELECTOR, "button[data-testid='send-button']"),
                (By.CSS_SELECTOR, "button[title='Send']"),
                (By.CSS_SELECTOR, "button:contains('Send')"),
                (By.XPATH, "//button[contains(@aria-label, 'Send') or contains(@aria-label, 'Submit')]")
            ]
            
            send_button = None
            for selector_type, selector in send_selectors:
                try:
                    if self.debug:
                        print(f"Trying send button selector: {selector_type}, {selector}")
                    send_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector))
                    )
                    if self.debug:
                        print(f"Found send button with selector: {selector}")
                    break
                except:
                    if self.debug:
                        print(f"Send button selector failed: {selector}")
                    continue
            
            if not send_button:
                if self.debug:
                    print("No send button found. Available buttons:")
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for i, btn in enumerate(buttons):
                        print(f"Button {i}: text='{btn.text}', aria-label='{btn.get_attribute('aria-label')}', class='{btn.get_attribute('class')}'")
                raise Exception("找不到發送按鈕")
                
            if self.debug:
                print("Send button found.")
            self.driver.execute_script("arguments[0].click();", send_button)

            # 等待5秒
            time.sleep(5)

            # 等待並找到所有響應元素中的 <p> 標籤
            if self.debug:
                print("Waiting for response elements...")
            # 等待並找到回應元素
            attempts = 0
            response_elements = []
            while attempts < 3 and not response_elements:
                try:
                    response_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
                    )
                except:
                    if self.debug:
                        print(f"Attempt {attempts + 1}/3 failed, retrying in 5 seconds...")
                    time.sleep(5)
                    attempts += 1
            if self.debug:
                print("Response elements found.")
            if response_elements:
                combined_response = ""
                for response in response_elements:
                    combined_response += response.text + "<br />"
                    if self.debug:
                        print("Combined Response:", combined_response)
                return combined_response.strip()

        except Exception as e:
            print("An error occurred:", e)
            print("Error details:", e.__class__.__name__, e)
            if hasattr(e, 'msg'):
                print("Error message:", e.msg)
            return None

        finally:
            # 關閉 WebDriver
            self.driver.quit()
            # 只在使用虛擬顯示器時才停止它
            if self.display:
                self.display.stop()

if __name__ == "__main__":
    # 更新 chrome_driver_path 以指向新的 ChromeDriver 路徑
    chrome_driver_path = "./chromedriver-linux64/chromedriver"  # 確保這裡指向下載的匹配版本的 ChromeDriver
    
    # 確保 ChromeDriver 文件具有可執行權限
    if not os.access(chrome_driver_path, os.X_OK):
        print(f"PermissionError: 無法訪問 {chrome_driver_path}，請手動設置可執行權限：")
        print(f"sudo chmod +x {chrome_driver_path}")
    else:
        print("選擇運行模式：")
        print("1. 正常模式 (無頭瀏覽器)")
        print("2. Debug 模式 (顯示瀏覽器)")
        
        mode = input("請選擇模式 (1 或 2，預設為 1): ").strip()
        show_browser = (mode == "2")
        
        if show_browser:
            print("⚠️  Debug 模式：瀏覽器視窗將會顯示")
            print("⚠️  注意：在 Codespaces 環境中可能無法正常顯示瀏覽器視窗")
        
        copilot = CopilotChat(chrome_driver_path, debug=True, show_browser=show_browser)
        input_text = input("Enter your question: ")
        word_limit = 30
        condition = "answer using only text"
        response_text = copilot.chat(input_text, word_limit, condition)
        print("Response Text:", response_text)