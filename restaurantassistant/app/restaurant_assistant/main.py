from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client

app = BedrockAgentCoreApp()
log = app.logger

# Define a Streamable HTTP MCP Client
mcp_clients = [get_streamable_http_mcp_client()]

 ### <=============== TODOOOOOOOOOOOOOOOOOOOOOO
DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant. Use tools when appropriate.
"""


# Define a collection of tools used by the model
tools = [] # TODOOOOO Add Agent as Tools here


#TODOOOOO Remove
# Define a simple function tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Return the sum of two numbers"""
    return a+b

tools.append(add_numbers)


# Add MCP client to tools if available
for mcp_client in mcp_clients:
    if mcp_client:
        tools.append(mcp_client)


_agent = None

def get_agent():
    """
    Create one Strands Agent for this AgentCore Runtime session's
    microVM and reuse it for subsequent invocations.

    AgentCore provides a dedicated microVM per runtimeSessionId,
    so different AgentCore sessions have isolated Agent instances.
    """
    global _agent

    if _agent is None:
        _agent = Agent(
            model=load_model(),
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            tools=tools
        )

    return _agent


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

    session_id = context.session_id

    print(f"sessionid: {session_id}")

    if not session_id:
        raise ValueError("session_id is required. Pass --session-id when invoking.")

    # Validate chatbot input
    prompt = payload.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")

    # Reuse the Agent within this AgentCore session's microVM
    agent = get_agent()


  # Stream Strands events back through AgentCore
    async for event in agent.stream_async(prompt):

        if not isinstance(event, dict) or "event" not in event:
            continue

        cbs = event["event"].get("contentBlockStart")

        if cbs is not None and not cbs.get("start"):
            continue

        yield event



if __name__ == "__main__":
    app.run()
