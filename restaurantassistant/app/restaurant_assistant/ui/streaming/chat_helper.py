"""The supporting logic for the Streamlit app"""
import boto3
import json


AWS_REGION = "us-east-1"

AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:742752463290:runtime/restaurantassistant_restaurant_assistant-0zuMLq5kJ2"

agentcore_client = boto3.client("bedrock-agentcore", region_name=AWS_REGION)


class ChatMessage:
    """Stores basic text messages for the Streamlit app"""

    def __init__(self, role, text):
        self.role = role
        self.text = text

def invoke_agent_runtime(agent_arn, payload, session_id):
    """Invokes an Amazon Bedrock AgentCore Runtime."""

    response = agentcore_client.invoke_agent_runtime(
        agentRuntimeArn=agent_arn,
        qualifier="DEFAULT",
        runtimeSessionId=session_id,
        payload=payload
    )

    if "text/event-stream" in response.get("contentType", ""):

        for line in response["response"].iter_lines(chunk_size=10):
            if line:
                line = line.decode("utf-8")

                if line.startswith("data: "):
                    line = line[6:]

                    try:
                        data = json.loads(line)

                        if isinstance(data, dict):
                            event = data.get("event", "")
                            contentBlockDelta = event.get("contentBlockDelta", "")
                            delta = contentBlockDelta.get("delta", "")
                            text = delta.get("text", "")

                            if text:
                                yield text   # yield sends that piece of text back to the caller immediately, then pauses this function at that point.

                    except Exception:
                        pass

def chat_with_agent(message_history, session_id, new_text=None):
    """Sends a message to the Orchestrator in AgentCore Runtime"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    payload = json.dumps({"prompt": new_text}).encode("utf-8")

	# AgentCore returns a StreamingBody.
    # Yield each piece so Streamlit can display it.
    full_response = ""

    # Invoke AgentCore and stream the response
    for text in invoke_agent_runtime(
        AGENT_RUNTIME_ARN,
        payload,
        session_id
    ):
        full_response += text

        # Pause here and yield this text to the caller chunk by chunk
        yield text

	# Below code does not execute until the for loop above is complete, which means the entire response has been received from AgentCore.
    response_message = ChatMessage("assistant", text=full_response)

    # Store complete assistant response in chat history
    message_history.append(response_message)
