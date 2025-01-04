from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import timeit

class CopilotChat:
    def __init__(self, chrome_driver_path, chrome_binary_path="/usr/bin/google-chrome", debug=False, headless=True):
        self.debug = debug
        # 初始化 WebDriver
        options = webdriver.ChromeOptions()
        if headless:
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
        options.binary_location = chrome_binary_path  # 確保 Chrome 瀏覽器的路徑正確

        # 設置 ChromeDriver 的路徑
        self.service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def chat(self, input_text, word_limit, condition):
        # 打开网页
        if self.debug:
            print("Opening webpage...")
        self.driver.get("https://copilot.microsoft.com/chats")

        try:
            # 等待并找到输入框
            if self.debug:
                print("Waiting for input box...")
            input_box = WebDriverWait(self.driver, 10).until(  # 增加等待時間到10秒
                EC.presence_of_element_located((By.ID, "userInput"))
            )
            if self.debug:
                print("Input box found.")
            message = f"{input_text} ({condition}, ans within {word_limit} words)"
            if self.debug:
                print("Message to send:", message)
            input_box.send_keys(message)

            # 使用 aria-label 定位并点击发送按钮
            if self.debug:
                print("Waiting for send button...")
            send_button = WebDriverWait(self.driver, 5).until(  # 增加等待時間到10秒
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit message']"))
            )
            if self.debug:
                print("Send button found.")
            self.driver.execute_script("arguments[0].click();", send_button)

            # 等待5秒
            time.sleep(5)

            # 等待并找到所有响应元素中的 <p> 标签
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
                        print(f"Attempt {attempts + 1} failed, retrying in 5 seconds...")
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
            # 关闭 WebDriver
            self.driver.quit()

def test_runtime():
    chrome_driver_path = "./chromedriver-linux64/chromedriver"
    copilot = CopilotChat(chrome_driver_path, debug=False, headless=True)
    input_text = "How to install python?"
    word_limit = 30
    condition = "answer using only text"
    runtime = timeit.timeit(lambda: copilot.chat(input_text, word_limit, condition), number=1)
    print("Runtime:", runtime)

if __name__ == "__main__":
    chrome_driver_path = "./chromedriver-linux64/chromedriver"
    copilot = CopilotChat(chrome_driver_path, debug=False, headless=True)
    input_text = "How to install python?"
    word_limit = 30
    condition = "answer using only text"
    response_text = copilot.chat(input_text, word_limit, condition)
    print("Response Text:", response_text)
    test_runtime()