import streamlit as st
st.set_page_config(page_title="AI Video Generator", page_icon="🎬", layout="centered")
st.set_page_config(
    page_title=" AI Video Generator ",
    page_icon="🎬"
)

st.markdown("""
<h1 style='text-align: center;'>🎬 AI Video Generator</h1>
<p style='text-align: center;'>حوّل أي سكربت لفيديو تلقائي</p>
""", unsafe_allow_html=True)
generate = st.button("🚀 Generate Video")
st.info("🔒Coming soon: You'll need to create an account after 2 videos. قريبًا: لازم تعمل حساب بعد 2 فيديو")
