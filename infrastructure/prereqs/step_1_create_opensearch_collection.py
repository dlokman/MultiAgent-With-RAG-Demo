from opensearch_collection_helper import create_collection_group_and_collection
import boto3
import json

# Create Seperate Orchestrator file to create a New KnowledgeBase with underlying Vector Index in OpenSearch

if __name__ == "__main__":

    region_name="us-east-1"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"
    encryption_policy_name = f"{collection_name}-sp"

    boto3_session = boto3.Session(region_name=region_name)
    aoss_client = boto3_session.client("opensearchserverless", region_name=region_name)

    # Create Encryption Policy for OpenSearch Serverless Collection
    try:
        encryption_policy = aoss_client.create_security_policy(
            name=encryption_policy_name,
            policy=json.dumps(
                {
                    "Rules": [
                        {
                            "Resource": ["collection/" + collection_name],
                            "ResourceType": "collection",
                        }
                    ],
                    "AWSOwnedKey": True,
                }
            ),
            type="encryption",
        )
    except aoss_client.exceptions.ConflictException:
        print(f"{encryption_policy_name} already exists, retrieving it!")

	# Create Collection Group and Collection in OpenSearch Serverless NextGen
    (
        host,
        collection_group,
        collection_group_id,
        collection_group_arn,
        collection,
        collection_id,
        collection_arn,
    ) = create_collection_group_and_collection(region_name, aoss_client, collection_group_name, collection_name)


