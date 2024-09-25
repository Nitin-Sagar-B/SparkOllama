import streamlit as st
import ollama
from typing import Dict, Generator

# Set wide mode
st.set_page_config(layout="wide")

# Load custom CSS for styling
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Generator function for streaming chat responses from Ollama
def ollama_generator(model_name: str, messages: Dict) -> Generator:
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk['message']['content']

# Page title
st.title("🤖 SparkOllama: Made By Sparkience AI Lab")

# Initialize session state variables
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Model Selection Dropdown (dark themed)
st.session_state.selected_model = st.selectbox(
    "Please select the model:", [model["name"] for model in ollama.list()["models"]])

# Clear chat history functionality
if st.button("Clear Chat History"):
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f'<div class="chat-box user-message">{message["content"]}</div>',
                        unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f'<div class="chat-box assistant-message">{message["content"]}</div>',
                        unsafe_allow_html=True)

# Chat input functionality
if prompt := st.chat_input("How can I assist you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-box user-message">{prompt}</div>', unsafe_allow_html=True)


    with st.chat_message("assistant"):
        response = st.write_stream(ollama_generator(st.session_state.selected_model, st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": response})
