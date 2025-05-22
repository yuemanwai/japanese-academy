# Install allure command line tool
sudo apt update
sudo apt install default-jre
java -version
sudo update-alternatives --config java

echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
which java

wget https://github.com/allure-framework/allure2/releases/download/2.23.0/allure-2.23.0.tgz
tar -xvzf allure-2.23.0.tgz
sudo rm allure-2.23.0.tgz
sudo mv allure-2.23.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure

allure --version



# 產生 Allure 測試結果
# pytest --alluredir=allure-results        

# 產生 Allure 報告
# allure generate allure-results --clean -o allure-report   

# 啟動本地伺服器瀏覽 Allure 報告
# allure serve allure-results               

