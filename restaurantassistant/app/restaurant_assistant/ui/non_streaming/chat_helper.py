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


def chat_with_agent(message_history, session_id, new_text=None):
    """Sends a message to the Orchestrator in AgentCore Runtime"""

    new_text_message = ChatMessage("user", text=new_text)
    message_history.append(new_text_message)

    payload = json.dumps({"prompt": new_text}).encode("utf-8")

    response = agentcore_client.invoke_agent_runtime(
        agentRuntimeArn=AGENT_RUNTIME_ARN,
        runtimeSessionId=session_id,
        qualifier="DEFAULT",
        payload=payload
    )

    # Read AgentCore response
    response_body = response["response"].read()
    result = json.loads(response_body)

    # Extract assistant text
    assistant_text = result["content"][0]["text"]

    # Store assistant response in chat history
    response_message = ChatMessage("assistant", text=assistant_text)
    message_history.append(response_message)

    return assistant_text
