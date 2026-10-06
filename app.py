import streamlit as st
import matplotlib.pyplot as plt
from sklearn .feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# ---------- MODERN UI ----------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
h1 {
    text-align: center;
    color: #38bdf8;
}
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
.stTextArea textarea {
    border-radius: 10px;
}
.stFileUploader {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;'>Upload your resume and compare it with job description using AI ✨</p>",
    unsafe_allow_html=True
)

# Layout (2 columns)
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("🧾 Paste Job Description", height=200)

st.markdown("---")

# Button
if st.button("🔍 Analyze Match"):
    if not uploaded_file:
        st.warning("⚠ Please upload your resume")
    elif not job_description:
        st.warning("⚠ Please paste job description")
    else:
        with st.spinner("🚀 Analyzing... Please wait"):
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                st.error("❌ Could not read PDF")
            else:
                score, res_proc, job_proc = calculate_similarity(resume_text, job_description)

                st.markdown("## 📊 Results")

                # Score Display
                st.progress(int(score))

                st.markdown(f"""
                <h2 style='text-align:center; color:#22c55e;'>
                Match Score: {score}%
                </h2>
                """, unsafe_allow_html=True)

                # Feedback
                if score < 40:
                    st.error("❌ Low Match - Improve your resume")
                elif score < 70:
                    st.warning("⚠ Medium Match - Can be improved")
                else:
                    st.success("✅ Strong Match - Great job!")

                st.markdown("---")

                # Suggestions
                st.markdown("## 💡 Suggestions")
                st.info("👉 Add more relevant keywords from job description")
                st.info("👉 Use action verbs (Developed, Managed, Built)")
                st.info("👉 Highlight skills matching job role")