import streamlit as st

from selenium.common.exceptions import InvalidArgumentException

from back_end import (
    init_driver,
    login
)


def config_session_state_vals(is_headless : bool = False, on_deploy : bool = True):
    
    # 表示ページを管理する変数
    if "driver" not in st.session_state:
        
        # ドライバの初期化
        driver = init_driver(
            is_headless=is_headless,
            on_deploy=on_deploy
        )
        
        st.session_state["driver"] = driver
    
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    
    if "user_password" not in st.session_state:
        st.session_state["user_password"] = ""
        
        
def is_valid_login_info(user_email : str, user_password : str) -> bool:
    
    if user_email == "" or user_password == "":
        return False
    
    return True


def main(on_deploy : bool = True):
    
    # セッション変数の初期化
    config_session_state_vals(
        is_headless=True,
        on_deploy=on_deploy
    )
    
    # ----------------------------------------------------------------------
    
    # タイトル
    st.title("LIVE POCKETS 自動購入bot")
    
    # ----------------------------------------------------------------------
    
    # チケットを取得する回の情報
    st.subheader("TICKETS URL")
    tickets_url = st.text_input("チケットを買いたい回のURL", placeholder="https://example.com")
    
    # ドライバを用いてURLにアクセス
    if tickets_url != "":
        try :
            st.session_state.driver.get(tickets_url)
        except InvalidArgumentException :
            st.warning("※無効でないURLを入力してください")
            st.stop()
    else :
        # チケットを買う回のURLが入力されていない場合それ以降の処理を行わない
        st.warning("※まずチケットを買う回のURLを入力してください")
        st.stop()
        
    # -----------------------------------------------------------------------
    
    # ログイン情報の登録
    st.subheader("ログイン情報")
    
    USER_EMAIL    = st.text_input("メールアドレス")
    USER_PASSWORD = st.text_input("パスワード")
    
    login_info_register_button = st.button("ログイン情報を登録")
    
    if not login_info_register_button:
        # ログインボタンが押されていない場合それ以降の処理を行わない
        st.stop()
    
    if login_info_register_button and is_valid_login_info(USER_EMAIL, USER_PASSWORD):
        
        # チケット購入回固有のページでログイン
        is_logined_correctly = login(
            driver=st.session_state.driver,
            user_email=USER_EMAIL,
            user_password=USER_PASSWORD
        )
        
        if is_logined_correctly:
            st.success("ログイン情報の確認に成功しました")
            
            # ログインに成功したときのみログイン情報を登録
            st.sesiion_state["user_email"]    = USER_EMAIL
            st.session_state["user_password"] = USER_PASSWORD
    
    # ----------------------------------------------------------------------
    
    

    


if __name__ == "__main__":
    main(
        on_deploy=True
    )