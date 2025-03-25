import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from st_audiorec import st_audiorec
from openai import OpenAI
import io
import time
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
api_key = 'your_api_key_here'
client = OpenAI(api_key=api_key)
model = ChatOpenAI(api_key=api_key, model='gpt-4o-mini')
history = []

# Custom CSS for chat interface
st.markdown("""
<style>
    .stApp {
        max-width: 500px;
        margin: 0 auto;
        padding: 0.5rem !important;
    }
    /* Remove space around title */
    .stMarkdown h1 {
        margin: 0 0 1rem 0 !important;
        padding: 0 !important;
    }
    
    .chat-container {
        height: calc(80vh - 60px);
        overflow-y: auto;
        padding: 1rem;
        background: #f0f2f5;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .user-message {
        background: #DCF8C6;
        padding: 8px 12px;
        border-radius: 7.5px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }

    .bot-message {
        background: white;
        padding: 8px 12px;
        border-radius: 7.5px;
        margin: 5px 0;
        max-width: 80%;
    }

    .timestamp {
        font-size: 0.75rem;
        color: #667781;
        margin-top: 2px;
    }

    .audio-input {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        background: white;
        padding: 0.5rem;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Personal response profile
system_prompt = """
You are answering as Shubham. Respond in a way that reflects your personality and real-life experiences.
Here are personal details about you:
- Life story: A passionate AI developer specializing in automation and chatbot development.
- Superpower: Problem-solving with AI and automation.
- Growth areas: Mastering Generative AI, business strategy, and leadership.
- Misconception: People think you are always serious, but you enjoy humor.
- How you push limits: Taking on extreme challenges like trekking in -15°C and building high-tech AI systems.
"""

history.append(SystemMessage(system_prompt))


def process_audio(audio_data):
    """Process audio input and generate response"""
    with st.spinner(""):
        # Transcribe audio
        wav_file = io.BytesIO(audio_data)
        wav_file.name = "recording.wav"
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=wav_file
        )
        user_input = transcription.text

        # Add user message
        st.session_state.messages.append({
            "type": "user",
            "content": user_input,
            "timestamp": time.strftime("%H:%M"),
            "audio": wav_file
        })
        history.append(HumanMessage(user_input))
        res = model.invoke(history)
        # Generate GPT response in personal style
        bot_response = res.content
        history.append(AIMessage(bot_response))

        # Convert response to speech
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="nova",
            input=bot_response
        )

        # Add bot message with its own audio
        st.session_state.messages.append({
            "type": "bot",
            "content": bot_response,
            "timestamp": time.strftime("%H:%M"),
            "audio": speech.content  # Store audio with message
        })


def main():
    st.title("Personal Voice Assistant")

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed' not in st.session_state:
        st.session_state.processed = False

    # Chat container
    chat_container = st.container()

    # Audio input at bottom
    with st.container():
        st.markdown('<div class="audio-input">', unsafe_allow_html=True)
        audio_data = st_audiorec()
        st.markdown('</div>', unsafe_allow_html=True)

    # Process audio when recorded
    if audio_data and not st.session_state.processed:
        process_audio(audio_data)
        st.session_state.processed = True
        st.rerun()
    elif not audio_data:
        st.session_state.processed = False

    # Display messages
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["type"] == "user":

                st.markdown(f"""
                <div class="user-message">
                </div>
                """, unsafe_allow_html=True)
                st.audio(msg['audio'], format="audio/mp3")

            else:
                st.markdown(f"""
                <div class="bot-message">
                </div>
                """, unsafe_allow_html=True)
                # Play individual audio for each message
                st.audio(msg['audio'], format="audio/mp3")

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()