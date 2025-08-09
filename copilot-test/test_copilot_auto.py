#!/usr/bin/env python3
"""
Copilot 自動測試腳本
"""

import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from copilot_improved import CopilotChat

def auto_test():
    print("=== Copilot 自動測試 ===")
    
    chrome_driver_path = "../chromedriver-linux64/chromedriver"
    
    if not os.access(chrome_driver_path, os.X_OK):
        print(f"❌ ChromeDriver 沒有執行權限: {chrome_driver_path}")
        return False
    
    copilot = None
    try:
        print("🚀 啟動 Copilot (headless 模式)...")
        
        copilot = CopilotChat(
            chrome_driver_path=chrome_driver_path,
            debug=True,
            show_browser=False  # 使用 headless 模式
        )
        
        print("✅ Copilot 初始化完成")
        
        # 測試問題
        test_question = "What is 2+2?"
        print(f"🧪 測試問題: {test_question}")
        
        response = copilot.chat(test_question, word_limit=20, condition="be concise")
        
        print(f"🤖 回應: {response}")
        
        if response and "錯誤" not in response:
            print("✅ 測試成功！")
            return True
        else:
            print("❌ 測試失敗 - 沒有收到有效回應")
            return False
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if copilot:
            try:
                copilot.cleanup()
                print("🔚 清理完成")
            except Exception as cleanup_error:
                print(f"⚠️  清理錯誤: {cleanup_error}")

if __name__ == "__main__":
    success = auto_test()
    exit(0 if success else 1)
