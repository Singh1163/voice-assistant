# Personal Voice Assistant

## Overview
This project is a **Personal Voice Assistant** built using **Streamlit**, **LangChain**, and **OpenAI APIs**. 
It allows users to interact via voice input, transcribes audio using **Whisper**, processes responses with **GPT-4o-mini**, 
and converts responses back to speech using OpenAI's **Text-to-Speech (TTS)** model.

## Features
- **Voice Input**: Users can speak their queries instead of typing.
- **AI Response**: Uses OpenAI's GPT-4o-mini model to generate human-like responses.
- **Voice Output**: Converts AI-generated responses into speech for seamless interaction.
- **Chat History**: Maintains a history of user-bot interactions within the session.
- **Personalized Responses**: The chatbot answers in a predefined personality style.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Singh1163/voice-assistant.git
cd voice-assistant
```

### 2. Create and Activate a Virtual Environment
**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required packages using:
```bash
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key
Create a `.env` file in the project root and add:
```
OPENAI_API_KEY=your_api_key_here
```
Alternatively, replace `'your_api_key_here'` in the script with your actual API key.

### 5. Run the Application
```bash
streamlit run main.py
```

---

## File Structure
```
voice-assistant/
│── main.py            # Main Streamlit app
│── requirements.txt  # Required dependencies
│── .env              # API keys (not included in repo)
│── README.md         # Project documentation
```

---

## Dependencies
- **Python 3.8+**
- `streamlit`
- `openai`
- `langchain`
- `st_audiorec`
- `dotenv`

---

## Troubleshooting
1. **Invalid API Key**: Ensure the correct API key.
2. **Audio Not Recording**: Check if microphone permissions are enabled.
3. **Module Not Found**: Run `pip install -r requirements.txt` to ensure all dependencies are installed.

For further queries, feel free to reach out!

---

# `requirements.txt`
```
streamlit
langchain
langchain-openai
openai
st-audiorec
dotenv
```

