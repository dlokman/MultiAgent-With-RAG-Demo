
import boto3
import pprint
import os
from utils import interactive_sleep
from knowledge_base_for_bedrock import KnowledgeBasesForAmazonBedrock

pp = pprint.PrettyPrinter(indent=2)


def verify_collection_name_exists(region_name, collection_name):
    boto3_session = boto3.Session(region_name=region_name)

    aoss_client = boto3_session.client("opensearchserverless", region_name=boto3_session.region_name)
    response = aoss_client.batch_get_collection(names=[collection_name])

    if not response["collectionDetails"]:
        raise ValueError(
            f"OpenSearch collection '{collection_name}' does not exist."
        )


if __name__ == "__main__":

    region_name="us-east-2"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    #Knowledge Base Name and Description
    knowledge_base_name = "restaurant-assistant-kb"
    knowledge_base_description = "Knowledge Base for Restaurant Assistant Application"

    #Knowledge Base will be created for these Files (Vector Embeddings Will be stored in OpenSearch Serverless Vector Index)
    kb_files_path = "kb_files"

    verify_collection_name_exists(region_name, collection_name)

    kb = KnowledgeBasesForAmazonBedrock(region_name=region_name, collection_name=collection_name)

    smm_client = boto3.client("ssm") # Systems Manager
    current_dir = os.path.dirname(os.path.abspath(__file__))

    kb_id, ds_id = kb.create_or_retrieve_knowledge_base(knowledge_base_name, knowledge_base_description)

    print(f"Knowledge Base ID: {kb_id}")
    print(f"Data Source ID: {ds_id}")

    #copy all docx files from kb_files to S3 bucket from
    kb.upload_directory(f"{current_dir}/{kb_files_path}", kb.get_data_bucket_name())

    # start_ingestion_job (create vector embeddings)
    kb.synchronize_data(kb_id, ds_id)

    # store the knowledge base id in SSM Parameter Store
    smm_client.put_parameter(
        Name=f"{knowledge_base_name}-id",
        Description=f"{knowledge_base_description} kb id",
        Value=kb_id,
        Type="String",
        Overwrite=True,
    )

