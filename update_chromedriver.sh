#!/bin/bash

# ChromeDriver 版本更新腳本
# 檢查 Chrome 和 ChromeDriver 版本是否一致，若不一致則自動更新

set -e  # 遇到錯誤時停止執行

echo "=== ChromeDriver 版本檢查與更新腳本 ==="
echo ""
echo "💡 如需查看可用的 Chrome 和 ChromeDriver 版本，請訪問："
echo "   🔗 https://googlechromelabs.github.io/chrome-for-testing/"
echo ""

# 檢查 Google Chrome 是否已安裝
if ! command -v google-chrome &> /dev/null; then
    echo "❌ 錯誤: Google Chrome 未安裝"
    echo "請先安裝 Google Chrome"
    exit 1
fi

# 取得 Google Chrome 版本
echo "🔍 檢查 Google Chrome 版本..."
CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
if [ -z "$CHROME_VERSION" ]; then
    echo "❌ 無法取得 Chrome 版本"
    exit 1
fi
echo "📱 Google Chrome 版本: $CHROME_VERSION"

# 檢查 ChromeDriver 是否存在
CHROMEDRIVER_VERSION=""
if [ -f "./chromedriver-linux64/chromedriver" ]; then
    echo "🔍 檢查 ChromeDriver 版本..."
    CHROMEDRIVER_VERSION=$(./chromedriver-linux64/chromedriver --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
    echo "🚗 ChromeDriver 版本: $CHROMEDRIVER_VERSION"
else
    echo "⚠️  ChromeDriver 不存在，將下載最新版本..."
fi

# 比較版本是否一致
if [ "$CHROME_VERSION" = "$CHROMEDRIVER_VERSION" ] && [ -n "$CHROMEDRIVER_VERSION" ]; then
    echo "✅ Chrome 和 ChromeDriver 版本一致 ($CHROME_VERSION)，無需更新"
    exit 0
else
    echo ""
    echo "⚠️  版本不一致，需要更新 ChromeDriver"
    echo "   Chrome: $CHROME_VERSION"
    echo "   ChromeDriver: ${CHROMEDRIVER_VERSION:-'未安裝'}"
    echo ""
fi

# 構建下載 URL
DOWNLOAD_URL="https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"
echo "📥 下載 URL: $DOWNLOAD_URL"

# 下載新版本的 ChromeDriver
echo "📥 正在下載 ChromeDriver 版本 $CHROME_VERSION..."

if ! curl -f -L -O "$DOWNLOAD_URL" 2>/dev/null; then
    echo "❌ 下載失敗，可能的原因："
    echo "   1. 版本號不正確"
    echo "   2. 網路連線問題"
    echo "   3. 該版本的 ChromeDriver 尚未發布"
    echo ""
    echo "🔗 請前往以下網址查看可用的版本："
    echo "   https://googlechromelabs.github.io/chrome-for-testing/"
    echo ""
    echo "💡 使用方法："
    echo "   1. 開啟上述網址"
    echo "   2. 搜尋您的 Chrome 版本: $CHROME_VERSION"
    echo "   3. 確認是否有對應的 ChromeDriver 版本"
    echo "   4. 如果沒有，請等待 Google 發布或使用相近版本"
    echo ""
    echo "🌐 或者在瀏覽器中直接檢查下載連結："
    echo "   $DOWNLOAD_URL"
    exit 1
fi

echo "✅ 下載成功"

# 備份現有的 ChromeDriver（如果存在）
if [ -d "./chromedriver-linux64" ]; then
    echo "💾 備份現有的 ChromeDriver..."
    if [ -d "./chromedriver-linux64.backup" ]; then
        rm -rf ./chromedriver-linux64.backup
    fi
    mv ./chromedriver-linux64 ./chromedriver-linux64.backup
fi

# 解壓縮檔案，自動選擇覆蓋所有檔案
echo "📂 解壓縮 ChromeDriver..."
echo "A" | unzip -q chromedriver-linux64.zip 2>/dev/null || {
    echo "❌ 解壓縮失敗"
    # 恢復備份
    if [ -d "./chromedriver-linux64.backup" ]; then
        mv ./chromedriver-linux64.backup ./chromedriver-linux64
    fi
    rm -f chromedriver-linux64.zip
    exit 1
}

# 設定執行權限
chmod +x ./chromedriver-linux64/chromedriver

# 刪除下載的 zip 檔案
rm chromedriver-linux64.zip
echo "🗑️  清理下載的 zip 檔案"

# 驗證安裝
echo "🔍 驗證新安裝的 ChromeDriver..."
NEW_VERSION=$(./chromedriver-linux64/chromedriver --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')

if [ "$CHROME_VERSION" = "$NEW_VERSION" ]; then
    echo "✅ ChromeDriver 更新成功！"
    echo "   Chrome: $CHROME_VERSION"
    echo "   ChromeDriver: $NEW_VERSION"
    
    # 刪除備份檔案
    if [ -d "./chromedriver-linux64.backup" ]; then
        rm -rf ./chromedriver-linux64.backup
        echo "🗑️  清理備份檔案"
    fi
    
    echo ""
    echo "🎉 版本現在一致，ChromeDriver 可以正常使用！"
else
    echo "❌ 更新失敗，版本仍不一致"
    echo "   預期: $CHROME_VERSION"
    echo "   實際: $NEW_VERSION"
    
    # 恢復備份
    if [ -d "./chromedriver-linux64.backup" ]; then
        rm -rf ./chromedriver-linux64
        mv ./chromedriver-linux64.backup ./chromedriver-linux64
        echo "🔄 已恢復原始 ChromeDriver"
    fi
    exit 1
fi

echo ""
echo "✨ 完成！ChromeDriver 已成功更新"
echo ""
echo "📋 相關資源："
echo "   🔗 Chrome 版本查詢: https://googlechromelabs.github.io/chrome-for-testing/"
echo "   📖 使用說明: 如遇到版本問題，請前往上述網址查看可用版本"
