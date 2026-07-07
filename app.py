import streamlit as st

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerPilot AI")

st.subheader("Your Personal AI Career Assistant")

st.write(
"""
CareerPilot AI helps you:

✅ Analyze Resume

✅ Improve ATS Score

✅ Prepare Interviews

✅ Build Career Roadmaps

✅ Optimize LinkedIn

✅ Match Resume with Jobs

Use the sidebar to explore the tools.
"""
)

st.divider()

col1,col2,col3=st.columns(3)

with col1:

    st.info("📄 Resume Analyzer")

with col2:

    st.info("🎤 Interview Coach")

with col3:

    st.info("🛣 Career Roadmap")