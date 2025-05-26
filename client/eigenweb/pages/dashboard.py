import streamlit as st
from eigenweb.components import service
from eigenweb import get_eigen
from eigen import Eigen
import time

eigen: Eigen = get_eigen()

def dashboard():
    st.markdown("# Dashboard")
    for slug, _service in eigen.services.items():
        service(slug, _service)

dashboard()
