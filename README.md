# Translingua - AI Powered Multi-Language Translator

## Project Overview

Translingua is an AI-powered multi-language translator that allows users to input text and get translations in multiple languages.  
The project uses **Streamlit** for an interactive web interface and is structured to separate code, documentation, and demo files for clarity.

---

## Project Structure

- **Project_Files/**  
  Contains all Python code and dependencies:
  - `app.py` – Main application script  
  - `translang.py` – Translation logic module (Streamlit app)  
  - `requirements.txt` – Required Python packages  

- **Documentation/**  
  Contains project documentation.  

- **Video Demo/**  
  Contains demonstration videos showcasing the project in action.  

- **.gitignore**  
  Ensures unnecessary files are not uploaded.  

---

## How to Run

1. **Set up and run the project**:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r Project_Files/requirements.txt

# Run the main app script
python Project_Files/app.py

# Or launch the interactive Streamlit app
streamlit run Project_Files/translang.py
---



