import streamlit as st

from back_end import (
    init_driver,
    login
)


def config_session_state_vals():
    
    # 表示ページを管理する変数
    if "app_page" not in st.session_state:
        st.session_state["app_page"] = None
        
        
def is_valid_login_info(user_email : str, user_password : str) -> bool:
    
    if user_email == "" or user_password == "":
        return False
    
    return True


def main():
    
    config_session_state_vals()
    
    driver = init_driver(
        is_headless=True
    )
    
    st.title("LIVE POCKETS 自動購入bot")
    st.write("## ログイン情報") 
    
    USER_EMAIL    = st.text_input("メールアドレス")
    USER_PASSWORD = st.text_input("パスワード")
    
    login_button = st.button("ログイン")
    
    if login_button and is_valid_login_info(USER_EMAIL, USER_PASSWORD):
        login(
            driver=driver,
            user_email=USER_EMAIL,
            user_password=USER_PASSWORD
        )
    
    


if __name__ == "__main__":
    main()