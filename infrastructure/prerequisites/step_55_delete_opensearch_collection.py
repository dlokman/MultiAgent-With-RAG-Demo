from opensearch_collection_helper import create_collection_group_and_collection
import boto3
import json
from utils import interactive_sleep

# Create Seperate Orchestrator file to create a New KnowledgeBase with underlying Vector Index in OpenSearch

if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"
    encryption_policy_name = f"{collection_name}-sp"
    network_policy_name = f"{collection_name}-np"

    boto3_session = boto3.Session(region_name=region_name)
    aoss_client = boto3_session.client("opensearchserverless", region_name=region_name)

    # 1) Get Collection Id
    response = aoss_client.batch_get_collection(names=[collection_name])

    if not response["collectionDetails"]:
        raise ValueError(
            f"OpenSearch collection '{collection_name}' does not exist."
        )

    collection = response["collectionDetails"][0]

    collection_id = collection["id"]
    collection_arn = collection["arn"]


    # 2) Delete Network Policy for the Collection
    try:
        aoss_client.delete_security_policy(type="network", name=network_policy_name)
        print("OpenSearch Serverless network policy deleted successfully!")
    except aoss_client.exceptions.ResourceNotFoundException:
        print(f"Network policy '{network_policy_name}' does not exist.")
    except Exception as e:
        print(e)


    # 3) Delete OpenSearch Collection
    try:
        aoss_client.delete_collection(id=collection_id)
        print("OpenSource Collection deleted successfully!")
    except Exception as e:
        print(e)


    # 4) Wait for Collection to get Deleted
    while True:
        response = aoss_client.batch_get_collection(names=[collection_name])

        if not response["collectionDetails"]:
            break

        print(
            f"Deleting collection... "
            f"Status: {response['collectionDetails'][0]['status']}"
        )

        interactive_sleep(30)

    print("\nCollection successfully deleted!")


    # 5) Delete Encryption Policy (sp=security policy)
    encryption_policy_name = f"{collection_name}-sp"

    try:
        aoss_client.get_security_policy(type="encryption", name=encryption_policy_name)
        aoss_client.delete_security_policy(type="encryption",name=encryption_policy_name)

        print("OpenSearch Serverless encryption policy deleted successfully!")

    except aoss_client.exceptions.ResourceNotFoundException:
        print(f"Encryption policy '{encryption_policy_name}' does not exist.")



    #6) Delete Collection Group
    collection_group = aoss_client.batch_get_collection_group(names=[collection_group_name])["collectionGroupDetails"][0]

    collection_group_id = collection_group["id"]
    collection_group_arn = collection_group["arn"]

    try:
        aoss_client.delete_collection_group(id=collection_group_id)
        print("OpenSource Collection Group deleted successfully!")
    except Exception as e:
        print(e)

