#!/usr/bin/env python3
"""
測試 Copilot 連接的腳本
用於診斷 Copilot 網站連接問題
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def test_copilot_connection():
    print("=== Copilot 連接測試 ===")
    
    # ChromeDriver 路徑
    chrome_driver_path = "../chromedriver-linux64/chromedriver"
    
    # 檢查檔案權限
    if not os.access(chrome_driver_path, os.X_OK):
        print(f"❌ ChromeDriver 沒有執行權限: {chrome_driver_path}")
        return False
    
    print("✅ ChromeDriver 權限正常")
    
    # 設置 Chrome 選項
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 無頭模式
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.7258.66 Safari/537.36')
    
    # 設置 ChromeDriver 服務
    service = Service(executable_path=chrome_driver_path)
    
    try:
        print("🚀 啟動 Chrome...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("🌐 訪問 Copilot 網站...")
        driver.get("https://copilot.microsoft.com/chats")
        
        # 等待頁面載入
        time.sleep(5)
        
        print(f"📄 當前 URL: {driver.current_url}")
        print(f"📄 頁面標題: {driver.title}")
        
        # 檢查是否被重定向
        if "copilot.microsoft.com" not in driver.current_url:
            print(f"⚠️  頁面被重定向到: {driver.current_url}")
        
        # 保存頁面截圖（如果可能）
        try:
            driver.save_screenshot("copilot_page.png")
            print("📸 已保存頁面截圖: copilot_page.png")
        except:
            print("❌ 無法保存截圖")
        
        # 檢查頁面內容
        page_source = driver.page_source
        print(f"📄 頁面內容長度: {len(page_source)} 字符")
        
        # 檢查是否包含關鍵字
        keywords = ["copilot", "microsoft", "chat", "input", "textarea", "login", "sign in"]
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in page_source.lower():
                found_keywords.append(keyword)
        
        print(f"🔍 找到的關鍵字: {found_keywords}")
        
        # 查找可能的輸入元素
        print("\n🔍 查找輸入元素...")
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        textarea_elements = driver.find_elements(By.TAG_NAME, "textarea")
        
        print(f"找到 {len(input_elements)} 個 input 元素")
        print(f"找到 {len(textarea_elements)} 個 textarea 元素")
        
        for i, elem in enumerate(input_elements[:5]):  # 只顯示前5個
            print(f"  Input {i}: id='{elem.get_attribute('id')}', class='{elem.get_attribute('class')}', placeholder='{elem.get_attribute('placeholder')}'")
        
        for i, elem in enumerate(textarea_elements[:5]):  # 只顯示前5個
            print(f"  Textarea {i}: id='{elem.get_attribute('id')}', class='{elem.get_attribute('class')}', placeholder='{elem.get_attribute('placeholder')}'")
        
        # 查找按鈕
        print("\n🔍 查找按鈕元素...")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"找到 {len(buttons)} 個按鈕")
        
        for i, btn in enumerate(buttons[:10]):  # 只顯示前10個
            text = btn.text.strip()[:20]  # 截取前20個字符
            aria_label = btn.get_attribute('aria-label') or ''
            print(f"  Button {i}: text='{text}', aria-label='{aria_label[:30]}'")
        
        # 檢查是否需要登入
        if "sign in" in page_source.lower() or "login" in page_source.lower():
            print("⚠️  網站可能需要登入")
        
        # 檢查是否有錯誤信息
        error_indicators = ["error", "blocked", "forbidden", "unauthorized"]
        for indicator in error_indicators:
            if indicator in page_source.lower():
                print(f"⚠️  可能的錯誤指示器: {indicator}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False
        
    finally:
        try:
            driver.quit()
            print("🔚 瀏覽器已關閉")
        except:
            pass

if __name__ == "__main__":
    success = test_copilot_connection()
    if success:
        print("\n✅ 測試完成，請檢查上述輸出來診斷問題")
    else:
        print("\n❌ 測試失敗")
