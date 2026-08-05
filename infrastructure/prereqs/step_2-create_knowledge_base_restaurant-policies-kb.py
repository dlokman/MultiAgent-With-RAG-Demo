
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock
from create_or_retrieve_knowledge_base_helper import create_or_retrieve_knowledge_base

pp = pprint.PrettyPrinter(indent=2)

if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    #Knowledge Base Name and Description
    knowledge_base_name = "restaurant-policies-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Policies"

    #Knowledge Base will be created for these Files (Vector Embeddings Will be stored in OpenSearch Serverless Vector Index)
    kb_files_path = "kb_files/restaurant_policies"

    create_or_retrieve_knowledge_base(region_name, collection_group_name, collection_name, knowledge_base_name, knowledge_base_description,
                                      kb_files_path, run_upload_directory = True)



