import streamlit as st
import os
import random
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

# 🔐 LOGIN SYSTEM
if "user" not in st.session_state:
    username = st.text_input("Enter your name 👤")
    if st.button("Login"):
        st.session_state.user = username

if "user" not in st.session_state:
    st.stop()

st.success(f"Welcome {st.session_state.user} 💙")

# 🌙 DARK MODE
dark_mode = st.toggle("🌙 Dark Mode")

# 🎨 CSS
st.markdown(f"""
<style>
body {{
    background-color: {"#121212" if dark_mode else "#a2c2f3"};
}}
.user-msg {{
    background: #4caf50;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin:5px;
}}
.bot-msg {{
    background: #ff9800;
    padding: 10px;
    border-radius: 10px;
    margin:5px;
}}
</style>
""", unsafe_allow_html=True)

# 🧠 ADVANCED SENTIMENT (MORE STATES)
def analyze_sentiment(text):
    text = text.lower()

    if any(word in text for word in ["happy", "joy", "excited", "good", "great"]):
        return "Happy 😊", 1
    elif any(word in text for word in ["sad", "down", "cry", "upset"]):
        return "Sad 😔", -1
    elif any(word in text for word in ["stress", "stressed", "pressure", "overwhelmed"]):
        return "Stressed 😣", -1
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        return "Angry 😡", -1
    elif any(word in text for word in ["bored", "nothing", "idle"]):
        return "Bored 😐", 0
    elif any(word in text for word in ["anxious", "nervous", "worried"]):
        return "Anxious 😟", -1
    elif any(word in text for word in ["tired", "sleepy", "exhausted"]):
        return "Tired 😴", 0
    elif any(word in text for word in ["lonely", "alone"]):
        return "Lonely 🥺", -1
    elif any(word in text for word in ["confused", "lost"]):
        return "Confused 😕", 0
    elif any(word in text for word in ["motivated", "focused"]):
        return "Motivated 💪", 1
    else:
        return "Neutral 😶", 0

# 💡 COPING STRATEGIES (EXPANDED)
def provide_coping_strategy(sentiment):
    strategies = {
        "Happy 😊": "🌟 Keep enjoying your happiness and spread positivity!",
        "Sad 😔": "💙 Talk to someone you trust or write your feelings.",
        "Stressed 😣": "🌿 Take deep breaths and take small breaks.",
        "Angry 😡": "🔥 Pause and relax. Try a short walk or music.",
        "Bored 😐": "🎮 Try something fun or learn a new skill.",
        "Anxious 😟": "🧘 Practice deep breathing and stay calm.",
        "Tired 😴": "😴 Rest well and recharge your energy.",
        "Lonely 🥺": "🤝 Reach out to a friend or family member.",
        "Confused 😕": "🧠 Take time to think slowly or ask for help.",
        "Motivated 💪": "🚀 Keep going! You’re doing amazing!"
    }
    return strategies.get(sentiment, "🌈 Stay positive!")

# 🤖 RESPONSE SYSTEM (UPGRADED)
def generate_response(prompt):
    text = prompt.lower()

    if "sad" in text:
        return "I'm really sorry you're feeling this way 💙 I'm here to listen."
    elif "happy" in text:
        return "That's wonderful 😊 Keep enjoying these moments!"
    elif "stress" in text:
        return "Take a deep breath 🌿 You can handle this step by step."
    elif "angry" in text:
        return "It's okay to feel angry 😌 Try to relax and pause."
    elif "bored" in text:
        return "Maybe try something creative 🎨 or fun!"
    elif "anxious" in text:
        return "You're safe 🤝 Try slow breathing."
    elif "tired" in text:
        return "Rest is important 😴 Give yourself a break."
    elif "lonely" in text:
        return "You're not alone 💙 I'm here with you."
    elif "confused" in text:
        return "It's okay to feel confused 🤔 Take it one step at a time."
    elif "motivated" in text:
        return "That's amazing 💪 Keep pushing forward!"
    else:
        return "I'm here to listen 🤗 Tell me more."

# 🔊 TEXT TO SPEECH
def speak(text):
    tts = gTTS(text)
    tts.save("voice.mp3")
    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read())

# HEADER
st.title("🧠 Mental Health Support")

# SESSION
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood" not in st.session_state:
    st.session_state.mood = []
if "journal" not in st.session_state:
    st.session_state.journal = []

# 💬 INPUT
# 💬 INPUT (FIXED - NO DUPLICATE)
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

user_message = st.text_input("Type your mood in one word💬")

if user_message and user_message != st.session_state.last_input:
    st.session_state.last_input = user_message

    sentiment, polarity = analyze_sentiment(user_message)
    response = generate_response(user_message)

    st.session_state.messages.append(("You", user_message))
    st.session_state.messages.append(("Bot", response))
    st.session_state.mood.append(polarity)

    # 🔊 SPEAK
    speak(response)

# 💬 CHAT DISPLAY
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"<div class='user-msg'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 {msg}</div>", unsafe_allow_html=True)

# 📊 MOOD TRACKER
st.subheader("📊 Mood History")
for i, val in enumerate(st.session_state.mood):
    if val == 1:
        st.text(f"{i+1}. 😊 Positive")
    elif val == -1:
        st.text(f"{i+1}. 😔 Negative")
    else:
        st.text(f"{i+1}. 😐 Neutral")

# 📝 JOURNAL
st.subheader("📝 Daily Journal")
journal_input = st.text_area("Write your thoughts...")
if st.button("Save Journal"):
    st.session_state.journal.append(journal_input)
    st.success("Saved!")

# 💡 SUGGESTION
if st.session_state.mood:
    last_sentiment, _ = analyze_sentiment(user_message)
    st.info(f"💡 Suggestion: {provide_coping_strategy(last_sentiment)}")

# 🧘 ACTIVITIES
st.subheader("🧘 Activities")
st.subheader("🧘 Guided Meditation")

if st.button("🌿 Deep Breathing"):
    st.success("Inhale for 4 sec → Hold 4 sec → Exhale 6 sec 🌬️ Repeat 5 times")

if st.button("🧠 Mindfulness"):
    st.success("Focus on your surroundings. Notice 5 things you see 👀")

if st.button("💭 Relax Mind"):
    st.success("Close your eyes and imagine a peaceful place 🌊")

if st.button("💤 Sleep Relaxation"):
    st.success("Slow breathing + calm thoughts 😴")

if st.button("🌸 Gratitude Meditation"):
    st.success("Think of 3 things you're grateful for 🙏")
motivations = [
    "💪 You are stronger than you think.",
    "🔥 Keep going, don’t give up.",
    "🚀 Success is coming your way.",
    "🌟 Believe in yourself.",
    "🏆 Every small step matters.",
    "🌈 Tough times don’t last.",
    "💯 You can do this!",
    "📈 Progress is progress.",
    "⚡ Stay focused and keep pushing.",
    "🎯 Your goals are worth it."
]

st.subheader("💪 Motivation Boost")
if st.button("Get Motivation"):
    st.success(random.choice(motivations))

# 🌈 AFFIRMATION
import random

affirmations = [
    "✨ I am strong and capable.",
    "🌟 I believe in myself.",
    "💖 I deserve happiness and peace.",
    "🌱 I am growing every day.",
    "💫 I can overcome any challenge.",
    "🌈 Better days are coming.",
    "🧘 I am calm and in control.",
    "💪 I am stronger than my struggles.",
    "🌸 I accept myself as I am.",
    "🔥 I have the power to change my story.",
    "🌼 I choose positivity today.",
    "💙 I am worthy of love and care.",
    "🚀 I will achieve my goals.",
    "🌞 Today is a fresh start.",
    "🌿 I release all stress and worry."
]

st.subheader("🌈 Positive Affirmation")
if st.button("Show Affirmation"):
    st.success(random.choice(affirmations))

    # 📥 DOWNLOAD CHAT
st.subheader("📥 Download Chat")

chat_text = ""
for sender, msg in st.session_state.messages:
    chat_text += f"{sender}: {msg}\n"

st.download_button(
    label="Download Chat Receipt 📄",
    data=chat_text,
    file_name="mental_health_chat.txt",
    mime="text/plain"
)

# 🆘 EMERGENCY
if st.button("🆘 Help"):
    st.error("📞 Call: 6361444541")

# FOOTER
st.markdown("<hr><center>🔒 Safe • Supportive</center>", unsafe_allow_html=True)