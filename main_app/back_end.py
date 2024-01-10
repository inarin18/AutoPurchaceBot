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
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import InvalidArgumentException


__ALL__ = [
    "init_driver",
]


def init_driver(is_headless : bool = False, on_deploy : bool = True) -> webdriver.Chrome:
    
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
    if on_deploy: # deploy時
        CHROMEDRIVER = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    else :        # local test時
        CHROMEDRIVER = Path(__file__).parent.parent / "Chromedriver" / "chromedriver.exe"


    """ ドライバーの初期化 """
    # ドライバー指定でChromeブラウザを開く
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    
    # ドライバの定義
    driver = webdriver.Chrome(
        service=chrome_service, 
        options=options
    )

    return driver


def login(driver : webdriver.Chrome, user_email : str, user_password : str) -> bool:
    
    """ チケットを買う回にアクセスした際にログイン
    """
    
    # ログイン画面に遷移
    login_window_css_selector = "#responsiveBaseFrame > header > section > nav > ul > li.buy > a"
    login_window = driver.find_element(By.CSS_SELECTOR, login_window_css_selector)
    try :
        login_window.click()
    except ElementClickInterceptedException: 
        # ログイン画面への遷移ボタンがクリックできない場合 javascript でクリック
        driver.execute_script('arguments[0].click();', login_window)
    
    # user_email
    email = driver.find_element(By.CSS_SELECTOR, "#email")
    email.send_keys(user_email)
    
    # password
    pass_word = driver.find_element(By.CSS_SELECTOR, "#password")
    pass_word.send_keys(user_password)
    
    # login
    login_css_selector = "#form > p.pull-left.btn-flat.btn-flat-input.btn-large.btn-arrow.btn-large.btn-green > button"
    login = driver.find_element(By.CSS_SELECTOR, login_css_selector)
    try :
        login.click()
    except ElementClickInterceptedException: 
        # ログインボタンがクリックできない場合 javascript でクリック
        driver.execute_script('arguments[0].click();', login)
    
    # ログイン待機
    time.sleep(2)
    
    # ログインが成功したか確認
    if driver.current_url == "https://t.livepocket.jp/login":
        return False
    
    return True
    

def local_test():
    
    # 大域変数の定義
    URL_LIVE_POCKETS : str = "https://www.livepocket.jp/login"
    
    USER_EMAIL    = input("email    >>")
    USER_PASSWORD = input("password >>")
    
    # ドライバの初期化   
    driver = init_driver(
        is_headless=False,
        on_deploy=False
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
    local_test()