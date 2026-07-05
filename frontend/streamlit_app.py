import json
import os
import urllib.request
from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def call_backend(path: str, payload: dict | None = None) -> dict:
    url = f"{BACKEND_URL.rstrip('/')}{path}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


st.set_page_config(page_title="Autonomous Self-Correcting Data Validation", layout="wide")
st.title("Autonomous Self-Correcting Data Validation")

sample_input = "Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad"
raw_input = st.text_area("Paste messy data", value=sample_input, height=180)

if st.button("Validate"):
    with st.spinner("Running validation pipeline..."):
        try:
            result = call_backend("/validate", {"raw_input": raw_input})
        except Exception as exc:
            st.error(f"Backend request failed: {exc}")
            st.stop()

    st.subheader("Original Input")
    st.code(raw_input)

    st.subheader("Extracted & Corrected JSON")
    st.json(result["corrected_data"])

    st.subheader("Validation Errors")
    st.json(result["validation_errors"])

    st.subheader("Corrections")
    st.json(result["correction_log"])

    st.subheader("Confidence Score")
    st.metric("Overall confidence", f"{result['final_report']['overall_confidence']:.2%}")
    st.caption(result["final_report"]["summary"])

    st.subheader("Final Report")
    st.write(result["final_report"]["report_text"])

st.subheader("Recent Validation History")
try:
    history = call_backend("/history?limit=5")
except Exception as exc:
    st.caption(f"Unable to load history from backend: {exc}")
    st.stop()

for item in history:
    with st.expander(f"{item['timestamp']} — {item['status']}"):
        st.write("Corrected data")
        st.json(item["corrected_data"])
        st.caption(f"Confidence: {item['confidence']:.2%}")
