
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock
from create_or_retrieve_knowledge_base_helper import create_or_retrieve_knowledge_base

pp = pprint.PrettyPrinter(indent=2)

# Local Dev Process
# 0) Add a file to prereqs/kb_files/restaurant_assistant/ directory
# 1) From Git Bash sync kb_files/xxx/ to its related s3 bucket (add, update, delete)
#    aws s3 sync prereqs/kb_files/xxx/ s3://my-bucket/ --delete
#    aws s3 sync prereqs/kb_files/restaurant_assistant/ s3://restaurant-assistant-kb-f1a6e/ --delete
# 2) Run this script to start the ingestion job for the knowledge base.
#    This will create vector embeddings for the updated files in the s3 bucket and store it in opensearch collection index
#    python prereqs/step_22_start_ingestion_job.py
if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    #Knowledge Base Name and Description
    knowledge_base_name = "restaurant-assistant-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Assistant"

    #Knowledge Base will be created for these Files (Vector Embeddings Will be stored in OpenSearch Serverless Vector Index)
    kb_files_path = "kb_files/restaurant_assistant"
	#kb_files_path = "kb_files/restaurant_policies"

    create_or_retrieve_knowledge_base(region_name, collection_group_name, collection_name, knowledge_base_name, knowledge_base_description,
                                      kb_files_path, run_upload_directory = False)



