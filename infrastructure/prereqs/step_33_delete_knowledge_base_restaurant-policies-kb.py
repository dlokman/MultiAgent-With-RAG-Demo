
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock
from delete_knowledge_base_helper import delete_knowledge_base

pp = pprint.PrettyPrinter(indent=2)

# To Delete a specific Knowledge Base

if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    # Delete This Knowledge Base Name
    knowledge_base_name = "restaurant-policies-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Policies"

    delete_knowledge_base(region_name, collection_group_name, collection_name, knowledge_base_name, knowledge_base_description)
