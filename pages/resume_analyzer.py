import streamlit as st
import json

from utils.pdf_reader import extract_text
from utils.gemini import analyze_resume

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    resume = extract_text(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            try:

                response = analyze_resume(resume)

                # Remove markdown if Gemini returns it
                response = response.replace("```json", "")
                response = response.replace("```", "")
                response = response.strip()

                data = json.loads(response)

                # -----------------------
                # ATS SCORE
                # -----------------------

                st.subheader("⭐ ATS Resume Score")

                score = data.get("overall_score", 0)

                st.markdown(
                    f"<h1 style='color:#4CAF50'>{score}/100</h1>",
                    unsafe_allow_html=True
                )

                st.progress(score / 100)

                st.divider()

                # -----------------------
                # FEEDBACK
                # -----------------------

                st.header("📝 Feedback")
                st.write(data.get("feedback", "No feedback available."))

                st.divider()

                # -----------------------
                # STRENGTHS
                # -----------------------

                st.header("✅ Strengths")

                for item in data.get("strengths", []):
                    st.success(item)

                # -----------------------
                # WEAKNESSES
                # -----------------------

                st.header("❌ Weaknesses")

                for item in data.get("weaknesses", []):
                    st.error(item)

                # -----------------------
                # MISSING KEYWORDS
                # -----------------------

                st.header("🔍 Missing Keywords")

                for item in data.get("missing_keywords", []):
                    st.warning(item)

                # -----------------------
                # ATS KEYWORDS
                # -----------------------

                st.header("🎯 ATS Keywords Found")

                for item in data.get("ats_keywords", []):
                    st.info(item)

                # -----------------------
                # FORMATTING
                # -----------------------

                st.header("📑 Formatting Suggestions")

                for item in data.get("formatting_feedback", []):
                    st.write("•", item)

                # -----------------------
                # ACTION ITEMS
                # -----------------------

                st.header("🚀 Action Items")

                for item in data.get("action_items", []):
                    st.write("✅", item)

            except Exception as e:

                st.error("Error while analyzing resume.")
                st.exception(e)