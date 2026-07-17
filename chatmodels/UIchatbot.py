import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------- CUSTOM UI ----------------
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at top left, #312e81 0%, transparent 35%),
            radial-gradient(circle at bottom right, #7e22ce 0%, transparent 35%),
            linear-gradient(135deg, #020617, #0f172a);
        color: white;
    }

    /* Main content width */
    .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Header card */
    .header-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 30px 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
    }

    .header-title {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .header-subtitle {
        font-size: 16px;
        color: #cbd5e1;
    }

    /* Mode section */
    .mode-title {
        font-size: 19px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    div[data-testid="stRadio"] {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 15px 20px;
        border-radius: 18px;
        margin-bottom: 25px;
    }

    div[data-testid="stRadio"] label {
        color: white;
        font-weight: 600;
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stChatMessageContent"] {
        color: #f8fafc;
        font-size: 16px;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.14);
    }

    div[data-testid="stChatInput"] textarea {
        color: white;
    }

    /* Reset button */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 12px;
        font-size: 16px;
        font-weight: 700;
        color: white;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        transition: 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.35);
        color: white;
    }

    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.12);
    }

    /* Hide Streamlit menu and footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- MODEL ----------------
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)


# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="header-card">
        <div class="header-title">🤖 AI Mood Chatbot</div>
        <div class="header-subtitle">
            Choose an AI personality and start chatting.
            Type <b>0</b> to stop the conversation.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- MODE SELECTION ----------------
st.markdown(
    '<div class="mode-title">Choose your AI personality</div>',
    unsafe_allow_html=True
)

mode_choice = st.radio(
    "Choose your AI Mode:",
    ["😡 Angry", "😂 Funny", "😢 Sad"],
    horizontal=True,
    label_visibility="collapsed"
)


# ---------------- MAP MODE ----------------
if mode_choice == "😡 Angry":
    mode = (
        "You are an angry AI agent. "
        "You respond aggressively and impatiently."
    )

elif mode_choice == "😂 Funny":
    mode = (
        "You are a very funny AI agent. "
        "You respond with humor and jokes."
    )

else:
    mode = (
        "You are a very sad AI agent. "
        "You respond in a depressed and emotional tone."
    )


# ---------------- SESSION MEMORY ----------------
if (
    "messages" not in st.session_state
    or st.session_state.get("current_mode") != mode
):
    st.session_state.current_mode = mode
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg.content)


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Say something...")


if user_input:

    if user_input == "0":
        st.warning(
            "Conversation ended. Refresh the page or reset the chat to start again."
        )
        st.stop()

    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = model.invoke(
                st.session_state.messages
            )

        st.write(response.content)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )


# ---------------- RESET BUTTON ----------------
st.divider()

if st.button("🔄 Reset Chat"):
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]
    st.rerun()