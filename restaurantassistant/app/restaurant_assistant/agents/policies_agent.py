"""Policies Agent for Restaurant Queries"""

import json
import os
from datetime import datetime

import boto3
from constants.constants import POLICIES_KB_NAME
from model.model import get_rerank_model_arn, load_model, get_model_arn
from strands import Agent, tool
from strands.models import BedrockModel
from utils import utils
import logging

log = logging.getLogger(__name__)

POLICIES_KNOWLEDGE_BASE_ID = utils.get_kb_id(kb_name=POLICIES_KB_NAME)

bedrock_runtime = boto3.client('bedrock-agent-runtime')

@tool()
def restaurant_policies_kb_retrieve(query: str) -> str:
    """Use this tool to retrieve restaurant policies data from restaurant policies Knowledge Base.

       Args:
      	 query: The user's question about restaurant policies.

       Returns:
       	 A response containing relevant restaurant policy information retrieved from the Knowledge Base.
    """

    if not POLICIES_KNOWLEDGE_BASE_ID:
        log.error("POLICIES_KNOWLEDGE_BASE_ID is not set up. Please check the configuration.")
        return "POLICIES_KNOWLEDGE_BASE_ID is not set up. Please check the configuration."

    params = {
				"input": {"text": query},
				"retrieveAndGenerateConfiguration": {
					'type': 'KNOWLEDGE_BASE',
					'knowledgeBaseConfiguration': {
						'knowledgeBaseId': POLICIES_KNOWLEDGE_BASE_ID,
						'modelArn': get_model_arn(),
						'retrievalConfiguration': {
							'vectorSearchConfiguration': {
								'numberOfResults': 7,
								"overrideSearchType": "HYBRID",
                                "rerankingConfiguration": {
									"type": "BEDROCK_RERANKING_MODEL",
									"bedrockRerankingConfiguration": {
										"modelConfiguration": {
											"modelArn": get_rerank_model_arn()
										},
										"numberOfRerankedResults": 3
									}
								}
							 }
						  }
					}
				}
    		}

    try:
        response = bedrock_runtime.retrieve_and_generate(**params)
        return response.get("output", {}).get("text", "No relevant information found in the restaurant policies Knowledge Base.")
    except Exception as e:
        log.error(f"Failed to retrieve information from policies knowledge base: {type(e).__name__}: {str(e)}", exc_info=True)
        return f"Failed to retrieve information from policies knowledge base"


policies_agent = Agent(
    name="policies_agent",
    description="An agent that specializes in answering questions about restaurant policies.",
    model=load_model(),
    system_prompt= """
		You are the Policies Agent, a specialized agent responsible for restaurant policy information.

		## Instructions
		- Answer questions about restaurant policies.
		- Retrieve restaurant policy information from the restaurant policies knowledge base.
		- Only handle restaurant policy-related tasks.
		- Only answer using information obtained using available tools. Do not use your own knowledge or invent policy information.
		- If the knowledge base does not contain enough information, clearly indicate what information could not be found or what additional information is needed.
		- If a request is outside restaurant policies, indicate that it is outside your scope so the orchestrator can route it appropriately.

		## Output Instructions
		- Return relevant policy information needed by the orchestrator.
		- Clearly indicate when retrieval fails or the requested information cannot be found.
		- Do not add introductions, greetings, or unnecessary conversational language.
		""",
    tools=[restaurant_policies_kb_retrieve],
)
