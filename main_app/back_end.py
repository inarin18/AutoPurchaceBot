import os, time, sys, csv

from pathlib import Path

# Selenium の基本モジュール
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Selenium4 からの新警告への対処
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 例外処理
from selenium.common.exceptions import NoSuchElementException


__ALL__ = [
    "init_driver",
]


# 大域変数の定義
URL_LIVE_POCKETS : str = "https://www.livepocket.jp/login"


def init_driver(is_headless : bool = False) -> webdriver.Chrome:
    
    """ ドライバオプションの設定 """
    options = Options()
    
    # ブラウザを非表示で動かすかどうか
    if is_headless: 
        options.add_argument('--headless')
        
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # ブラウザ制御コメントを非表示化
    options.add_experimental_option( 
        'excludeSwitches', 
        ['enable-logging']
    )
    
    # WebDriverのテスト動作をTrueに
    options.use_chromium = True      


    """ クロームドライバパスの取得 """  
    CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    CHROMEDRIVER = Path(__file__).parent / "Chromedriver" / "chromedriver.exe"


    """ ドライバーの初期化 """
    # ドライバー指定でChromeブラウザを開く
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    
    # ドライバの定義
    driver = webdriver.Chrome(
        service=chrome_service, 
        options=options
    )

    return driver


def login(driver : webdriver.Chrome, user_email : str, user_password : str) -> None:
    
    # user_email
    email = driver.find_element(By.CSS_SELECTOR, "#email")
    email.send_keys(user_email)
    
    # password
    pass_word = driver.find_element(By.CSS_SELECTOR, "#password")
    pass_word.send_keys(user_password)
    
    # login
    login_css_selector = "#form > p.pull-left.btn-flat.btn-flat-input.btn-large.btn-arrow.btn-large.btn-green > button"
    login = driver.find_element(By.CSS_SELECTOR, login_css_selector)
    login.click()
    
    # ログイン完了まで待機
    time.sleep(10)
    

def test():
    
    USER_EMAIL    = input("email    >>")
    USER_PASSWORD = input("password >>")
    
    # ドライバの初期化   
    driver = init_driver(
        is_headless=False
    )
    
    # URLにアクセス
    driver.get(URL_LIVE_POCKETS)
    
    login(
        driver=driver,
        user_email=USER_EMAIL,
        user_password=USER_PASSWORD
    )
    
    # ドライバを明示的に終了
    # driver.close()
    


if __name__ == "__main__":
    test()