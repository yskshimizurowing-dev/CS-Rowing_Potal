# utils.py
import streamlit as st
from config import SECRET_TOKEN

def get_url(item):
    """URL構築の共通処理"""
    if "key" in item:
        url = st.secrets.get(item["key"])
        if item["type"] == "gas":
            return f"{url}?token={SECRET_TOKEN}"
        return url
    return item.get("url")
