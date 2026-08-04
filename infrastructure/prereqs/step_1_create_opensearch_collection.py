from opensearch_collection_helper import create_collection_group_and_collection
import boto3
# Create Seperate Orchestrator file to create a New KnowledgeBase with underlying Vector Index in OpenSearch

if __name__ == "__main__":

    region_name="us-east-2"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    boto3_session = boto3.Session(region_name=region_name)
    aoss_client = boto3_session.client("opensearchserverless", region_name=region_name)

    (
        host,
        collection_group,
        collection_group_id,
        collection_group_arn,
        collection,
        collection_id,
        collection_arn,
    ) = create_collection_group_and_collection(region_name, aoss_client, collection_group_name, collection_name)


