#!/usr/bin/env python3
"""
深度診斷 Copilot 回應結構
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

def analyze_response_structure():
    print("=== Copilot 回應結構分析 ===")
    
    chrome_driver_path = "../chromedriver-linux64/chromedriver"
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 訪問網站
        print("🌐 訪問 Copilot...")
        driver.get("https://copilot.microsoft.com/chats")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        time.sleep(5)
        
        # 找到輸入框
        print("🔍 尋找輸入框...")
        input_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "userInput"))
        )
        
        # 發送簡單測試訊息
        test_message = "Hello"
        print(f"📝 發送測試訊息: {test_message}")
        
        input_box.click()
        time.sleep(1)
        input_box.send_keys(test_message)
        time.sleep(1)
        
        # 發送
        send_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Submit']"))
        )
        driver.execute_script("arguments[0].click();", send_button)
        print("✅ 訊息已發送")
        
        # 等待並分析回應區域
        print("⏳ 等待回應生成...")
        time.sleep(10)  # 給足夠時間讓回應生成
        
        # 保存完整頁面截圖
        driver.save_screenshot("full_page_after_send.png")
        print("📸 已保存完整頁面截圖: full_page_after_send.png")
        
        # 分析頁面結構
        print("\n🔍 分析頁面結構...")
        
        # 查找所有可能包含回應的元素
        potential_response_selectors = [
            "div[data-testid='conversation-turn']",
            "div[role='article']",
            "div.ac-textBlock",
            "div[class*='response']",
            "div[class*='message']",
            "div[class*='turn']",
            "div[class*='conversation']",
            "p",
            "span"
        ]
        
        for selector in potential_response_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\n📋 找到 {len(elements)} 個 '{selector}' 元素:")
                    for i, elem in enumerate(elements[-5:]):  # 只顯示最後5個
                        text = elem.text.strip()[:100]  # 截取前100字符
                        if text:
                            print(f"  {i}: {text}")
                            # 檢查是否包含我們的測試訊息回應
                            if any(word in text.lower() for word in ['hello', 'hi', 'greet', '你好']):
                                print(f"    ✅ 可能的回應: {text}")
            except Exception as e:
                print(f"  ❌ 選擇器 '{selector}' 失敗: {e}")
        
        # 獲取頁面的 HTML 結構（部分）
        print("\n📄 頁面 HTML 結構分析...")
        page_source = driver.page_source
        
        # 查找包含 "Hello" 回應的部分
        if "Hello" in page_source or "hello" in page_source:
            print("✅ 頁面包含 'Hello' 回應")
            # 找到包含回應的 HTML 片段
            lines = page_source.split('\n')
            for i, line in enumerate(lines):
                if 'hello' in line.lower() and len(line.strip()) > 20:
                    print(f"  回應行 {i}: {line.strip()[:200]}")
        else:
            print("❌ 頁面不包含 'Hello' 回應")
        
        # 檢查是否有載入指示器
        loading_selectors = [
            "[class*='loading']",
            "[class*='typing']",
            "[class*='thinking']",
            "[data-testid*='loading']"
        ]
        
        print("\n🔄 檢查載入狀態...")
        for selector in loading_selectors:
            try:
                loading_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if loading_elements:
                    for elem in loading_elements:
                        if elem.is_displayed():
                            print(f"  ⏳ 發現載入中元素: {selector}")
            except:
                pass
        
        # 檢查錯誤訊息
        error_keywords = ['error', 'failed', 'try again', '錯誤', '失敗']
        for keyword in error_keywords:
            if keyword in page_source.lower():
                print(f"⚠️  發現可能的錯誤關鍵字: {keyword}")
        
        return True
        
    except Exception as e:
        print(f"❌ 分析過程中發生錯誤: {e}")
        try:
            driver.save_screenshot("analysis_error.png")
        except:
            pass
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    analyze_response_structure()
