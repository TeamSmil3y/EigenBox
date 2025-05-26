import streamlit as st

def main():
    dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="🎈")
    login = st.Page("pages/login.py", title="Login", icon="🔑")
    nav = st.navigation([dashboard, login])
    nav.run()

if __name__ == "__main__":
    main()
