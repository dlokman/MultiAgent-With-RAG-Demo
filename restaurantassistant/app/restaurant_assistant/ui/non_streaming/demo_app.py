"""The presentation layer for the Streamlit app"""

import uuid
import streamlit as st
import chat_helper as chathelper

st.set_page_config(page_title="Restaurant Chatbot")

st.title("Restaurant Chatbot")
st.caption("Built With Amazon Bedrock AgentCore + Strands Agents")

# Initialize chat history
if "chat_history" not in st.session_state: # see if the chat history hasn't been created yet
    st.session_state.chat_history = [] # initialize the chat history


# Create one AgentCore Runtime session ID for this Streamlit session
if "agentcore_session_id" not in st.session_state:
    st.session_state.agentcore_session_id = str(uuid.uuid4())

chat_container = st.container()

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:
    with chat_container.chat_message(message.role):
        st.markdown(message.text)


input_text = st.chat_input("Chat with your bot here")    # display a chat input box


if input_text:

    # Immediately display user's message
    with chat_container.chat_message("user"):
        st.markdown(input_text)

    with st.spinner("Thinking..."):
        response = chathelper.chat_with_agent(
            message_history=st.session_state.chat_history,
            session_id=st.session_state.agentcore_session_id,
            new_text=input_text
        )

        with chat_container.chat_message("assistant"):
          	st.markdown(response)
