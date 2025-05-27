from typing import Callable
import streamlit as st

@st.dialog("Please Confirm")
def are_you_sure(message: str, confirm: str, callback: Callable, key: str = "are_you_sure"):
    st.markdown(message)
    _, col1, _ = st.columns([3, 2, 3])
    with col1:
        if st.button(confirm, key=f"yes_{key}", type="primary", use_container_width=True):
            st.session_state.callback_queue.append(callback)
            st.rerun()
