import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import logging

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

logging.basicConfig(level=logging.INFO)

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Korean": "ko"
}

def translate_text(text, source_language, target_language):
    if source_language == "Auto Detect":
        prompt = f"Detect the source language and translate to {target_language}. Only return translated text. Text: {text}"
    else:
        prompt = f"Translate from {source_language} to {target_language}. Only return translated text. Text: {text}"

    logging.info(f"Translating from {source_language} to {target_language}")
    response = model.generate_content([prompt])
    return response.text


if "history" not in st.session_state:
    st.session_state.history = []

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto Detect"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "English"

st.set_page_config(page_title="TransLingua", page_icon="🌍", layout="wide")

st.markdown("""
<style>
body {
    background-color: #f5f5f7;
}

.main {
    background: transparent;
}

.title {
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #1d1d1f, #6e6e73);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 500;
    background: linear-gradient(90deg, #0071e3, #42a5f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 40px;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.stTextArea textarea {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 18px;
    font-size: 1rem;
    border: 2px solid #d1d1d6;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.stTextArea textarea:focus {
    border: 2px solid #0071e3;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.2);
}

.stButton>button {
    background-color: #0071e3;
    color: white;
    border-radius: 14px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #005bb5;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">TransLingua</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Powered Text Translator</div>', unsafe_allow_html=True)

language_names = list(LANGUAGES.keys())

col_lang1, col_lang2 = st.columns(2)

with col_lang1:
    st.session_state.source_lang = st.selectbox(
        "Source Language",
        language_names,
        index=language_names.index(st.session_state.source_lang)
    )

with col_lang2:
    st.session_state.target_lang = st.selectbox(
        "Target Language",
        language_names[1:],
        index=language_names[1:].index(st.session_state.target_lang)
    )

col_swap, col_translate = st.columns(2)

with col_swap:
    if st.button("Swap"):
        if st.session_state.source_lang != "Auto Detect":
            st.session_state.source_lang, st.session_state.target_lang = (
                st.session_state.target_lang,
                st.session_state.source_lang,
            )
            st.rerun()

with col_translate:
    translate_clicked = st.button("Translate")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    text = st.text_area("Enter Text", height=280)

with col2:
    translated_output = st.session_state.get("latest_translation", "")
    st.text_area("Translated Text", value=translated_output, height=280)

if translate_clicked:
    if text.strip() == "":
        st.warning("Please enter text")
    else:
        try:
            with st.spinner("Translating..."):
                translated = translate_text(
                    text,
                    st.session_state.source_lang,
                    st.session_state.target_lang
                )

            st.session_state.latest_translation = translated

            st.session_state.history.append({
                "input": text,
                "output": translated,
                "from": st.session_state.source_lang,
                "to": st.session_state.target_lang
            })

            st.rerun()

        except Exception as e:
            st.error("API quota exceeded or service temporarily unavailable. Please try again later.")
            logging.error(str(e))

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.history:
    st.subheader("Recent Translations")
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"**{item['from']} → {item['to']}**")
        st.write("Input:", item["input"])
        st.write("Output:", item["output"])
        st.markdown("---")

if st.button("Clear History"):
    st.session_state.history = []
    st.session_state.latest_translation = ""
    st.rerun()
