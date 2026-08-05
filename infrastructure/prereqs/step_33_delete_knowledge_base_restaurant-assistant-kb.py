
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock
from delete_knowledge_base_helper import delete_knowledge_base

pp = pprint.PrettyPrinter(indent=2)

def verify_knowledge_base_exists(region_name, knowledge_base_name):
    bedrock_agent_client = boto3.client("bedrock-agent", region_name=region_name)

    kbs_available = bedrock_agent_client.list_knowledge_bases(
        maxResults=100,
    )

    kb_id = None

    for kb in kbs_available["knowledgeBaseSummaries"]:
        if knowledge_base_name == kb["name"]:
            kb_id = kb["knowledgeBaseId"]

    if kb_id is None:
        raise ValueError(
            f"Knowledge Base: '{knowledge_base_name}' does not exist."
        )

# To Delete a specific Knowledge Base

if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    # Delete This Knowledge Base Name
    knowledge_base_name = "restaurant-assistant-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Assistant Application"

    delete_knowledge_base(region_name, collection_group_name, collection_name, knowledge_base_name, knowledge_base_description)
