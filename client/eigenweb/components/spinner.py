import streamlit as st

SPINNER_HTML = """
<div style="display: flex; align-items: center; justify-content: center;">
    <div class="spinner-eigen" style="border: 4px solid rgba(0, 0, 0, 0.1); display: inline-flex; border-left-color: #09f; border-radius: 50%; width: 24px; height: 24px; animation: spin 1s linear infinite;"></div>
</div>
<style>
.spinner-eigen {
    border: 4px solid rgba(0, 0, 0, 0.1);
    display: inline-flex;
    border-left-color: #09f;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
"""

def spinner():
    """
    A spinner such as in streamlit but without blocking the UI.
    """
    st.markdown(SPINNER_HTML, unsafe_allow_html=True)
