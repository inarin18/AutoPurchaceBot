import streamlit as st

from back_end import (
    init_driver
)


def main():
    
    st.title("自動購入bot")
    st.write("## ログイン情報") 
    
    USER_EMAIL = st.text_input("メールアドレス")
    
    


if __name__ == "__main__":
    main()