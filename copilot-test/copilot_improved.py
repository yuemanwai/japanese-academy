#!/usr/bin/env python3
"""
改進版的 Copilot 聊天腳本
添加反檢測和更好的錯誤處理
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import subprocess
import os
import random

class CopilotChat:
    def __init__(self, chrome_driver_path, chrome_binary_path="/usr/bin/google-chrome", debug=False, show_browser=False):
        self.debug = debug
        self.show_browser = show_browser
        
        # 只在不需要顯示瀏覽器時才啟動虛擬顯示器
        if not show_browser:
            try:
                from pyvirtualdisplay import Display
                self.display = Display(visible=0, size=(1920, 1080))
                self.display.start()
            except ImportError:
                if self.debug:
                    print("⚠️  pyvirtualdisplay 未安裝，使用 headless 模式")
                self.display = None
        else:
            self.display = None
            
        options = webdriver.ChromeOptions()
        
        # 反檢測設置
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if not show_browser:
            options.add_argument('--headless')  # 無頭模式
        
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--window-size=1920,1080')
        
        # 更真實的 User-Agent
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.7258.66 Safari/537.36')
        
        # 語言設置
        options.add_argument('--lang=en-US')
        
        if chrome_binary_path:
            options.binary_location = chrome_binary_path

        # 設置 ChromeDriver 的路徑
        self.service = Service(executable_path=chrome_driver_path)
        
        if self.debug:
            print(f"Using Chrome binary: {chrome_binary_path}")
            print(f"Using ChromeDriver: {chrome_driver_path}")
            print(f"Show browser: {show_browser}")
            
        self.driver = webdriver.Chrome(service=self.service, options=options)
        
        # 執行反檢測腳本
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def human_like_delay(self, min_delay=0.5, max_delay=2.0):
        """模擬人類操作的隨機延遲"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def chat(self, input_text, word_limit=50, condition="answer using only text"):
        driver_closed = False
        try:
            # 打開網頁
            if self.debug:
                print("🌐 Opening Copilot webpage...")
            self.driver.get("https://copilot.microsoft.com/chats")
            
            # 人類化延遲
            self.human_like_delay(3, 5)
            
            if self.debug:
                print(f"📄 Current URL: {self.driver.current_url}")
                print(f"📄 Page title: {self.driver.title}")

            # 檢查是否需要處理 Cloudflare 或其他檢查
            if "challenge" in self.driver.current_url.lower() or "cf-" in self.driver.page_source:
                if self.debug:
                    print("⚠️  檢測到 Cloudflare 挑戰，等待...")
                time.sleep(10)  # 等待挑戰完成

            # 檢查登入狀態
            page_source = self.driver.page_source.lower()
            if "sign in" in page_source and "userInput" not in page_source:
                if self.debug:
                    print("⚠️  可能需要登入，嘗試繼續...")
                
            # 等待並找到輸入框
            if self.debug:
                print("🔍 Looking for input box...")
            
            # 多種輸入框選擇器
            input_selectors = [
                (By.ID, "userInput"),
                (By.CSS_SELECTOR, "textarea[placeholder*='Message Copilot']"),
                (By.CSS_SELECTOR, "textarea[placeholder*='Ask me anything']"),
                (By.CSS_SELECTOR, "textarea.font-ligatures-none"),
                (By.CSS_SELECTOR, "[data-testid='input-turn-counter']")
            ]
            
            input_box = None
            for selector_type, selector in input_selectors:
                try:
                    if self.debug:
                        print(f"  Trying: {selector}")
                    input_box = WebDriverWait(self.driver, 10).until(  # 增加等待時間
                        EC.element_to_be_clickable((selector_type, selector))
                    )
                    if self.debug:
                        print(f"✅ Found input box: {selector}")
                    break
                except Exception as e:
                    if self.debug:
                        print(f"  Failed: {str(e)[:50]}...")
                    continue
            
            if not input_box:
                if self.debug:
                    print("❌ 找不到輸入框，保存截圖進行診斷...")
                    try:
                        self.driver.save_screenshot("input_box_not_found.png")
                    except:
                        pass
                raise Exception("❌ 找不到輸入框，可能需要登入或網站結構已改變")
            
            # 確保輸入框可見和可用
            self.driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
            self.human_like_delay(0.5, 1.0)
                
            # 點擊輸入框以確保焦點
            try:
                input_box.click()
                if self.debug:
                    print("✅ Clicked input box")
            except Exception as e:
                if self.debug:
                    print(f"⚠️  Click failed, trying JS click: {e}")
                self.driver.execute_script("arguments[0].click();", input_box)
            
            self.human_like_delay(0.5, 1.0)
            
            # 準備訊息
            message = f"(Please answer in no more than {word_limit} words, {condition}) {input_text}"
            if self.debug:
                print(f"📝 Sending message: {message}")
            
            # 清空輸入框（如果有內容）
            try:
                input_box.clear()
            except:
                pass
            
            # 使用更穩定的輸入方式
            try:
                # 方法1: 直接輸入所有文字
                input_box.send_keys(message)
                if self.debug:
                    print("✅ Message typed successfully")
            except Exception as e:
                if self.debug:
                    print(f"⚠️  Direct typing failed: {e}, trying JS input...")
                # 方法2: 使用 JavaScript 輸入
                self.driver.execute_script("arguments[0].value = arguments[1];", input_box, message)
                # 觸發輸入事件
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_box)
            
            self.human_like_delay(1, 2)

            # 尋找發送按鈕
            if self.debug:
                print("🔍 Looking for send button...")
            
            send_selectors = [
                (By.CSS_SELECTOR, "button[aria-label*='Submit']"),
                (By.CSS_SELECTOR, "button[aria-label*='Send']"),
                (By.CSS_SELECTOR, "button[data-testid='send-button']"),
                (By.XPATH, "//button[contains(@aria-label, 'Submit') or contains(@aria-label, 'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]
            
            send_button = None
            for selector_type, selector in send_selectors:
                try:
                    if self.debug:
                        print(f"  Trying send button: {selector}")
                    send_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector))
                    )
                    if self.debug:
                        print(f"✅ Found send button: {selector}")
                    break
                except Exception as e:
                    if self.debug:
                        print(f"  Send button selector failed: {str(e)[:50]}...")
                    continue
            
            # 發送訊息
            message_sent = False
            if send_button:
                try:
                    # 方法1: 使用 JavaScript 點擊
                    self.driver.execute_script("arguments[0].click();", send_button)
                    if self.debug:
                        print("✅ Message sent via button click (JS)")
                    message_sent = True
                except Exception as e:
                    if self.debug:
                        print(f"⚠️  JS click failed: {e}")
                    try:
                        # 方法2: 普通點擊
                        send_button.click()
                        if self.debug:
                            print("✅ Message sent via button click")
                        message_sent = True
                    except Exception as e2:
                        if self.debug:
                            print(f"⚠️  Normal click failed: {e2}")
            
            if not message_sent:
                try:
                    # 方法3: 按 Enter 鍵
                    if self.debug:
                        print("🔄 Trying Enter key...")
                    input_box.send_keys(Keys.ENTER)
                    if self.debug:
                        print("✅ Message sent via Enter key")
                    message_sent = True
                except Exception as e:
                    if self.debug:
                        print(f"⚠️  Enter key failed: {e}")
            
            if not message_sent:
                if self.debug:
                    print("❌ 無法發送訊息，保存截圖...")
                    try:
                        self.driver.save_screenshot("send_failed.png")
                    except:
                        pass
                raise Exception("無法發送訊息")

            # 等待回應 - 增加等待時間和更好的檢測
            if self.debug:
                print("⏳ Waiting for response...")
            
            # 給系統更多時間處理
            time.sleep(5)
            
            # 檢查是否有載入指示器
            loading_indicators = [
                (By.CSS_SELECTOR, ".loading"),
                (By.CSS_SELECTOR, "[data-testid='loading']"),
                (By.CSS_SELECTOR, ".typing"),
                (By.XPATH, "//*[contains(text(), 'typing') or contains(text(), 'loading')]")
            ]
            
            # 等待載入完成
            max_wait_time = 30  # 最多等待30秒
            wait_count = 0
            while wait_count < max_wait_time:
                loading_found = False
                for selector_type, selector in loading_indicators:
                    try:
                        loading_elem = self.driver.find_element(selector_type, selector)
                        if loading_elem.is_displayed():
                            loading_found = True
                            if self.debug and wait_count % 5 == 0:
                                print(f"  Still loading... ({wait_count}s)")
                            break
                    except:
                        continue
                
                if not loading_found:
                    break
                    
                time.sleep(1)
                wait_count += 1
            
            # 額外等待讓回應完全載入
            time.sleep(3)
            
            # 尋找回應
            response_selectors = [
                (By.CSS_SELECTOR, "[data-testid='conversation-turn'] p"),
                (By.CSS_SELECTOR, ".ac-textBlock p"),
                (By.CSS_SELECTOR, "[role='article'] p"),
                (By.TAG_NAME, "p")
            ]
            
            response_text = ""
            for selector_type, selector in response_selectors:
                try:
                    response_elements = self.driver.find_elements(selector_type, selector)
                    if response_elements:
                        # 取最後幾個段落作為回應
                        recent_responses = response_elements[-5:]
                        for elem in recent_responses:
                            text = elem.text.strip()
                            if text and len(text) > 10:  # 過濾太短的文字
                                response_text += text + " "
                        break
                except Exception as e:
                    if self.debug:
                        print(f"Response selector failed: {e}")
                    continue
            
            if response_text.strip():
                if self.debug:
                    print("✅ Response received")
                return response_text.strip()
            else:
                if self.debug:
                    print("⚠️  No response found, saving screenshot for debugging")
                    try:
                        self.driver.save_screenshot("no_response_debug.png")
                    except:
                        pass
                return "沒有收到回應，請檢查網站狀態"

        except Exception as e:
            if self.debug:
                print(f"❌ Error occurred: {e}")
                print(f"❌ Error type: {type(e).__name__}")
                try:
                    print(f"❌ Current URL: {self.driver.current_url}")
                    self.driver.save_screenshot("error_debug.png")
                    if self.debug:
                        print("🔍 Error screenshot saved: error_debug.png")
                except Exception as screenshot_error:
                    if self.debug:
                        print(f"⚠️  Could not save screenshot: {screenshot_error}")
            return f"發生錯誤: {str(e)}"

    def cleanup(self):
        """清理資源的獨立方法"""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                if self.debug:
                    print("🔚 WebDriver closed")
        except Exception as e:
            if self.debug:
                print(f"⚠️  Error closing WebDriver: {e}")
        
        try:
            if hasattr(self, 'display') and self.display:
                self.display.stop()
                if self.debug:
                    print("🔚 Virtual display stopped")
        except Exception as e:
            if self.debug:
                print(f"⚠️  Error stopping display: {e}")

    def __del__(self):
        """確保資源被清理"""
        try:
            self.cleanup()
        except:
            pass

def main():
    print("=== Copilot 聊天測試 ===")
    
    chrome_driver_path = "../chromedriver-linux64/chromedriver"
    
    if not os.access(chrome_driver_path, os.X_OK):
        print(f"❌ ChromeDriver 沒有執行權限: {chrome_driver_path}")
        print(f"執行: chmod +x {chrome_driver_path}")
        return
    
    print("選擇運行模式：")
    print("1. 正常模式 (headless)")
    print("2. Debug 模式 (顯示瀏覽器，如果環境支持)")
    
    copilot = None
    try:
        mode = input("請選擇 (1 或 2，預設 1): ").strip() or "1"
        show_browser = (mode == "2")
        
        question = input("請輸入您的問題: ").strip()
        if not question:
            question = "Hello, how are you?"
        
        print(f"\n🚀 啟動 Copilot，模式: {'顯示瀏覽器' if show_browser else '無頭模式'}")
        
        copilot = CopilotChat(
            chrome_driver_path=chrome_driver_path,
            debug=True,
            show_browser=show_browser
        )
        
        print("✅ Copilot 初始化完成，開始對話...")
        
        response = copilot.chat(question, word_limit=50, condition="be helpful and concise")
        
        print(f"\n💬 問題: {question}")
        print(f"🤖 回應: {response}")
        
        if show_browser:
            input("\n按 Enter 鍵關閉瀏覽器...")
        
    except KeyboardInterrupt:
        print("\n👋 已取消")
    except Exception as e:
        print(f"\n❌ 程序錯誤: {e}")
        import traceback
        print("詳細錯誤信息:")
        traceback.print_exc()
    finally:
        # 確保清理資源
        if copilot:
            try:
                copilot.cleanup()
            except Exception as cleanup_error:
                print(f"⚠️  清理過程中發生錯誤: {cleanup_error}")
        print("🔚 程序結束")

if __name__ == "__main__":
    main()
