import streamlit as st
from openai import OpenAI

# Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["API_KEY"])

st.title("Chat with GPT-5.2")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# Input box
prompt = st.chat_input("Ask me anything!")
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🦉").markdown(prompt)

    # Get completion
    completion = client.chat.completions.create(
        model="gpt-5.2",
        messages=st.session_state.messages
    )

    reply = completion.choices[0].message.content

    # Add assistant reply (fixed role)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)