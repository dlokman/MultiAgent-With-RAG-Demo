# execute in git bash on windows

echo "create collection group and collection ..."
python step_1_create_opensearch_collection.py

echo "create knowledge base ..."
python step_2-create_or_retrieve_knowledge_base.py

echo "create DynamoDB ..."
python prereqs/dynamodb.py --mode create
