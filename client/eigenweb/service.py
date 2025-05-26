from eigen import Eigen
from pathlib import Path
import streamlit as st

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "eigen/config.toml"

@st.cache_resource
def get_eigen():
    """
    Create and return an instance of the Eigen class with the default configuration path.
    """
    return Eigen(DEFAULT_CONFIG_PATH)
