
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock

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


if __name__ == "__main__":

    region_name="us-east-2"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    # Delete This Knowledge Base Name
    knowledge_base_name = "restaurant-assistant-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Assistant Application"

    #Knowledge Base will be created for these Files (Vector Embeddings Will be stored in OpenSearch Serverless Vector Index)
    kb_files_path = "kb_files"

    verify_knowledge_base_exists(region_name, knowledge_base_name)

    kb = KnowledgeBasesForAmazonBedrock(region_name=region_name, collection_name=collection_name)

    # If KB already exsts, it will be retrieved
    kb_id, ds_id = kb.create_or_retrieve_knowledge_base(knowledge_base_name, knowledge_base_description)

    print(f"Knowledge Base ID: {kb_id}")
    print(f"Data Source ID: {ds_id}")


    kb.delete_kb(knowledge_base_name)

    smm_client = boto3.client("ssm") # Systems Manager
    smm_client.delete_parameter(Name=f"{knowledge_base_name}-id")