from strands import Agent, tool
from model.model import load_model
from mcp_client.client import get_streamable_http_mcp_client
from orchestrator_agent import orchestrator

import logging
from bedrock_agentcore.runtime import BedrockAgentCoreApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

log = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

_orchestrator_agent = None

def get_orchestrator_agent():
    """
    Create one Strands Orchestrator Agent for this AgentCore Runtime session's microVM and reuse it for subsequent invocations.

    AgentCore provides a dedicated microVM per runtimeSessionId, so different AgentCore sessions have isolated Agent instances.
    """
    global _orchestrator_agent

    if _orchestrator_agent is None:
        _orchestrator_agent = orchestrator

    return _orchestrator_agent


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

    # Validate chatbot input
    prompt = payload.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")

    # Reuse the Agent within this AgentCore session's microVM
    orchestrator_agent = get_orchestrator_agent()


  # Stream Strands events back through AgentCore
    async for event in orchestrator_agent.stream_async(prompt):

        if not isinstance(event, dict) or "event" not in event:
            continue

        cbs = event["event"].get("contentBlockStart")

        if cbs is not None and not cbs.get("start"):
            continue

        yield event



if __name__ == "__main__":
    app.run()
