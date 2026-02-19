import streamlit as st
from translang import translate_text

st.set_page_config(page_title="Translingua", page_icon="🌍")

st.title("🌍 Translingua")
st.subheader("AI Powered Language Translation Tool")

input_text = st.text_area("Enter text to translate:")

source_language = st.selectbox(
    "Select source language",
    ["English", "Hindi", "Telugu", "Tamil", "French", "German"]
)

target_language = st.selectbox(
    "Select target language",
    ["English", "Hindi", "Telugu", "Tamil", "French", "German"]
)

if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("Please enter text.")
    else:
        with st.spinner("Translating..."):
            result = translate_text(input_text, source_language, target_language)
            st.success("Translation:")
            st.write(result)
