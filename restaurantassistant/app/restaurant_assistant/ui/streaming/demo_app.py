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
    st.session_state.agentcore_session_id = str(uuid.uuid4())  # eg 550e8400-e29b-41d4-a716-446655440000

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

	# will stream the response chunk by chunk from AgentCore Runtime
    response_stream = chathelper.chat_with_agent(
        message_history=st.session_state.chat_history,
        session_id=st.session_state.agentcore_session_id,
        new_text=input_text
    )

    # control moves here immediately after the above call

    # Spinner exists only while waiting for first response chunk
    with st.spinner("Thinking..."):
        try:
            first_chunk = next(response_stream) # block/wait until response_stream yields its first value
        except StopIteration:
            first_chunk = None

    # Spinner is gone at this point
    with chat_container.chat_message("assistant"):

        if first_chunk:

            def stream_response():
                yield first_chunk           # Yield the first chunk
                yield from response_stream  # Yield the remaining chunks as they arrive

            st.write_stream(stream_response())