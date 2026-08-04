
import pprint
from utils import interactive_sleep

pp = pprint.PrettyPrinter(indent=2)

# Create Collection Group and Collection in OpenSearch Serverless
def create_collection_group_and_collection(region_name, aoss_client, collection_group_name, collection_name):

	# 1) Create OpenSearch CollectionGroup
	try:
		collection_group = aoss_client.create_collection_group(
			name=collection_group_name,
			generation="NEXTGEN",
			standbyReplicas="ENABLED",
			capacityLimits={
				"minIndexingCapacityInOCU": 0,
				"maxIndexingCapacityInOCU": 8,
				"minSearchCapacityInOCU": 0,
				"maxSearchCapacityInOCU": 8
			},
		)

		collection_group_detail = collection_group["createCollectionGroupDetail"]

		collection_group_id = collection_group_detail["id"]
		collection_group_arn = collection_group_detail["arn"]

	except aoss_client.exceptions.ConflictException:
		collection_group = aoss_client.batch_get_collection_group(names=[collection_group_name])["collectionGroupDetails"][0]

		pp.pprint(collection_group)

		collection_group_id = collection_group["id"]
		collection_group_arn = collection_group["arn"]

	print("\nCollection Group successfully created:")
	pp.pprint(collection_group)



	# 2) Create OpenSearch Collection

	try:
		collection = aoss_client.create_collection(
			name=collection_name, type="VECTORSEARCH", collectionGroupName=collection_group_name   # Need CollectionGroupName for OPenSearch NextGen
		)
		collection_id = collection["createCollectionDetail"]["id"]
		collection_arn = collection["createCollectionDetail"]["arn"]
	except aoss_client.exceptions.ConflictException:
		collection = aoss_client.batch_get_collection(
			names=[collection_name]
		)["collectionDetails"][0]
		pp.pprint(collection)
		collection_id = collection["id"]
		collection_arn = collection["arn"]

	pp.pprint(collection)

	# Get the OpenSearch serverless collection URL
	host = collection_id + "." + region_name + ".aoss.amazonaws.com"

	print(host)
	# wait for collection creation
	# This can take couple of minutes to finish
	response = aoss_client.batch_get_collection(names=[collection_name])

	# Periodically check collection status
	while (response["collectionDetails"][0]["status"]) == "CREATING":
		print("Creating collection...")
		interactive_sleep(30)
		response = aoss_client.batch_get_collection(names=[collection_name])

	print("\nCollection successfully created:")
	pp.pprint(response["collectionDetails"])

	return host, collection_group, collection_group_id, collection_group_arn, collection, collection_id, collection_arn
