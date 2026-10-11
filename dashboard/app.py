import os
import requests
import pandas as pd
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="Discovery Hub", layout="wide")
st.title("Discovery Research Hub")

@st.cache_data(ttl=15)
def fetch(path):
    return requests.get(f"{API}{path}").json()

interviews = pd.DataFrame(fetch("/api/interviews"))
insights = pd.DataFrame(fetch("/api/insights"))
clusters = pd.DataFrame(fetch("/api/insights/clusters"))

c1, c2, c3 = st.columns(3)
c1.metric("Интервью", len(interviews))
c2.metric("Инсайтов", len(insights))
c3.metric("Кластеров", len(clusters) if not clusters.empty else 0)

st.subheader("Новое интервью")
with st.form("new"):
    participant = st.text_input("Участник")
    segment = st.selectbox("Сегмент", ["enterprise", "smb", "consumer"])
    transcript = st.text_area("Транскрипт", height=200)
    if st.form_submit_button("Сохранить"):
        r = requests.post(f"{API}/api/interviews", json={
            "participant": participant, "segment": segment,
            "transcript": transcript})
        if r.ok:
            st.success(f"Сохранено id={r.json()['id']}")
            st.cache_data.clear()

if st.button("Перекластеризовать"):
    st.json(requests.post(f"{API}/api/insights/recluster").json())
    st.cache_data.clear()

if st.button("Сгенерировать JTBD"):
    st.json(requests.post(f"{API}/api/jtbd/generate").json())
    st.cache_data.clear()

st.subheader("Кластеры инсайтов")
if not clusters.empty:
    st.dataframe(clusters)
