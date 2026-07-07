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
st.caption("Analyze your resume, calculate ATS score and receive AI-powered feedback.")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_name" not in st.session_state:
    st.session_state.resume_name = None

if uploaded_file:

    if st.session_state.resume_name != uploaded_file.name:
        st.session_state.analysis = None
        st.session_state.resume_name = uploaded_file.name

    resume_text = extract_text(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("🚀 Analyze Resume"):

        if st.session_state.analysis is None:

            with st.spinner("Analyzing your Resume..."):

                ats = calculate_ats_score(resume_text)

                score = ats["overall_score"]

                response = analyze_resume(
                    resume_text,
                    score
                )

                response = response.replace("```json", "")
                response = response.replace("```", "")

                feedback = json.loads(response)

                st.session_state.analysis = {
                    "score": score,
                    "sections": ats["section_scores"],
                    "feedback": feedback
                }

    if st.session_state.analysis:

        result = st.session_state.analysis

        score = result["score"]
        sections = result["sections"]
        feedback = result["feedback"]

        st.divider()

        col1, col2 = st.columns([1,2])

        with col1:

            st.metric(
                "⭐ ATS Score",
                f"{score}/100"
            )

            st.progress(score/100)

        with col2:

            st.subheader("Resume Health")

            if score >= 80:

                st.success("Excellent Resume")

            elif score >= 60:

                st.info(
                    "Good Resume\n\nA few improvements can make it stronger."
                )

            elif score >= 40:

                st.warning(
                    "Needs Improvement\n\nSeveral ATS improvements are recommended."
                )

            else:

                st.error(
                    "Poor ATS Resume\n\nMajor improvements are required."
                )

        st.divider()

        # ===============================
        # SECTION SCORES
        # ===============================

        st.subheader("📊 Section Scores")

        for section, value in sections.items():

            st.write(
                f"**{section.replace('_',' ').title()}**"
            )

            maximum = 20

            if section == "ats_keywords":
                maximum = 10

            if section == "formatting":
                maximum = 10

            st.progress(value/maximum)

            st.caption(f"{value}/{maximum}")

        st.divider()

        # ===============================
        # FEEDBACK
        # ===============================

        st.header("📝 AI Feedback")

        st.write(
            feedback.get(
                "feedback",
                "No feedback generated."
            )
        )

        st.divider()

        left,right = st.columns(2)

        with left:

            st.subheader("✅ Strengths")

            for item in feedback.get(
                "strengths",
                []
            ):

                st.success(item)

        with right:

            st.subheader("❌ Weaknesses")

            for item in feedback.get(
                "weaknesses",
                []
            ):

                st.error(item)

        st.divider()
                # ===============================
        # MISSING KEYWORDS
        # ===============================

        st.header("🔍 Missing Keywords")

        missing = feedback.get("missing_keywords", [])

        if missing:

            cols = st.columns(3)

            for i, keyword in enumerate(missing):

                cols[i % 3].warning(keyword)

        else:

            st.success("No missing keywords found!")

        st.divider()

        # ===============================
        # FORMATTING SUGGESTIONS
        # ===============================

        st.header("📑 Formatting Suggestions")

        formatting = feedback.get(
            "formatting_feedback",
            []
        )

        if formatting:

            for item in formatting:

                st.write("•", item)

        else:

            st.success("Formatting looks good!")

        st.divider()

        # ===============================
        # ACTION ITEMS
        # ===============================

        st.header("🚀 Recommended Action Plan")

        actions = feedback.get(
            "action_items",
            []
        )

        if actions:

            for i, item in enumerate(actions, start=1):

                st.checkbox(
                    f"{i}. {item}",
                    value=False
                )

        else:

            st.success("No action items!")

        st.divider()

        # ===============================
        # DOWNLOAD REPORT
        # ===============================

        report = f"""
===============================
CareerPilot AI Resume Report
===============================

ATS Score : {score}/100

--------------------------------

AI Feedback

{feedback.get("feedback","")}

--------------------------------

Strengths

"""

        for item in feedback.get("strengths", []):

            report += f"- {item}\n"

        report += "\nWeaknesses\n\n"

        for item in feedback.get("weaknesses", []):

            report += f"- {item}\n"

        report += "\nMissing Keywords\n\n"

        for item in feedback.get("missing_keywords", []):

            report += f"- {item}\n"

        report += "\nFormatting Suggestions\n\n"

        for item in feedback.get("formatting_feedback", []):

            report += f"- {item}\n"

        report += "\nAction Items\n\n"

        for item in feedback.get("action_items", []):

            report += f"- {item}\n"

        st.download_button(
            label="📄 Download Resume Report",
            data=report,
            file_name="CareerPilot_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.success("✅ Resume analysis completed successfully!")