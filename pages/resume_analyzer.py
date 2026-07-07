import streamlit as st
import json

from utils.pdf_reader import extract_text
from utils.ats_engine import calculate_ats_score
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

# Store analysis in session so we don't call Gemini repeatedly
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_name" not in st.session_state:
    st.session_state.resume_name = None

if uploaded_file:

    # Reset cache if a different file is uploaded
    if st.session_state.resume_name != uploaded_file.name:
        st.session_state.analysis = None
        st.session_state.resume_name = uploaded_file.name

    resume_text = extract_text(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):

        if st.session_state.analysis is None:

            with st.spinner("Analyzing Resume..."):

                try:

                    # ---------- Python ATS Engine ----------
                    ats_result = calculate_ats_score(resume_text)

                    score = ats_result["overall_score"]

                    # ---------- Gemini Feedback ----------
                    response = analyze_resume(
                        resume_text,
                        score
                    )

                    response = response.replace("```json", "")
                    response = response.replace("```", "")

                    ai_feedback = json.loads(response)

                    st.session_state.analysis = {
                        "score": score,
                        "sections": ats_result["section_scores"],
                        "feedback": ai_feedback
                    }

                except Exception as e:

                    st.error(f"Error: {e}")
                    st.stop()

        result = st.session_state.analysis

        score = result["score"]
        sections = result["sections"]
        feedback = result["feedback"]

        # ==========================
        # SCORE
        # ==========================

        st.subheader("⭐ ATS Resume Score")

        st.metric("Overall Score", f"{score}/100")

        st.progress(score / 100)

        st.divider()

        # ==========================
        # SECTION SCORES
        # ==========================

        st.subheader("📊 Section Scores")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Contact", sections["contact_information"])
            st.metric("Education", sections["education"])
            st.metric("Skills", sections["skills"])
            st.metric("Projects", sections["projects"])

        with col2:
            st.metric("Experience", sections["experience"])
            st.metric("ATS Keywords", sections["ats_keywords"])
            st.metric("Formatting", sections["formatting"])

        st.divider()

        # ==========================
        # FEEDBACK
        # ==========================

        st.header("📝 Feedback")
        st.write(feedback.get("feedback", ""))

        st.header("✅ Strengths")

        for item in feedback.get("strengths", []):
            st.success(item)

        st.header("❌ Weaknesses")

        for item in feedback.get("weaknesses", []):
            st.error(item)

        st.header("🔍 Missing Keywords")

        for item in feedback.get("missing_keywords", []):
            st.warning(item)

        st.header("📄 Formatting Feedback")

        for item in feedback.get("formatting_feedback", []):
            st.write("•", item)

        st.header("🚀 Action Items")

        for item in feedback.get("action_items", []):
            st.write("✅", item)