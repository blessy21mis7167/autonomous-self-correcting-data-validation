from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from autonomous_self_correcting_data_validation_system.database import fetch_validation_history
from autonomous_self_correcting_data_validation_system.validation import run_validation_pipeline


st.set_page_config(page_title="Autonomous Self-Correcting Data Validation", layout="wide")
st.title("Autonomous Self-Correcting Data Validation")

sample_input = "Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad"
raw_input = st.text_area("Paste messy data", value=sample_input, height=180)

if st.button("Validate"):
    with st.spinner("Running validation pipeline..."):
        result = run_validation_pipeline(raw_input)

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
for item in fetch_validation_history(limit=5):
    with st.expander(f"{item['timestamp']} — {item['status']}"):
        st.write("Corrected data")
        st.json(item["corrected_data"])
        st.caption(f"Confidence: {item['confidence']:.2%}")
