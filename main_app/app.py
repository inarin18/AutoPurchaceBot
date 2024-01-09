import streamlit as st

from back_end import (
    init_driver,
    login
)


def config_session_state_vals():
    
    # 表示ページを管理する変数
    if "driver" not in st.session_state:
        
        # ドライバの初期化
        driver = init_driver(
            is_headless=False,
            on_deploy=True
        )
        
        st.session_state["driver"] = driver
        
        
def is_valid_login_info(user_email : str, user_password : str) -> bool:
    
    if user_email == "" or user_password == "":
        return False
    
    return True


def main():
    
    URL_LIVE_POCKETS : str = "https://www.livepocket.jp/login"
    
    # セッション変数の初期化
    config_session_state_vals()
    
    # ドライバを用いてURLにアクセス
    st.session_state.driver.get(URL_LIVE_POCKETS)
    
    st.title("LIVE POCKETS 自動購入bot")
    st.write("## ログイン情報") 
    
    USER_EMAIL    = st.text_input("メールアドレス")
    USER_PASSWORD = st.text_input("パスワード")
    
    login_button = st.button("ログイン")
    
    if login_button and is_valid_login_info(USER_EMAIL, USER_PASSWORD):
        login(
            driver=st.session_state.driver,
            user_email=USER_EMAIL,
            user_password=USER_PASSWORD
        )
    
    


if __name__ == "__main__":
    main()