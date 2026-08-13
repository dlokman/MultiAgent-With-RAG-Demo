# MultiAgent-With-RAG-Demo

MultiAgent-With-RAG-Demo Application

OpenSearch Collection
├── products-index   ← Products KnowledgeBase  (All Product Related Docs ingested here)
├── orders-index     ← Orders KnowledgeBase    (All Orders Related Docs ingested here)
├── warranty-index   ← Warranty KnowledgeBase
└── policies-index   ← Policies KnowledgeBase

1:1 Relationship => Each Knowledgebase has its own Vector Index.

Collection Group
│
├── Collection A
│   ├── Vector Index 1 ← KnowledgeBase 1  (All KnowledgeBase 1 Related Docs ingested here)
│   └── Vector Index 2 ← KnowledgeBase 2  (All KnowledgeBase 2 Related Docs ingested here)


restaurant-collection-group
│
├── restaurant-collection
│   ├── restaurant-assistant-kb-index   ←   restaurant-assistant-kb  (All Restaurant Assistant Docs ingested here)
│   └── restaurant-policies-kb-index    ←   restaurant-policies-kb  (All Restaurant Policies Docs ingested here)

============================================Instructions=============================================
cd infrastructure
python prerequisites/step_1_create_opensearch_collection.py  (Create Encryption Policy, Collection Group and Collection)
python prerequisites/step_2-create_knowledge_base_restaurant-assistant-kb.py


============================================Scripts=============================================

restaurant-assistant-kb
restaurant-policies-kb

cd infrastructure
python prerequisites/step_1_create_opensearch_collection.py
python prerequisites/step_2-create_knowledge_base_restaurant-assistant-kb.py
python prerequisites/step_2-create_knowledge_base_restaurant-policies-kb.py

if needed after adding/updating/deleting docs in kb_files
python prerequisites/step_22_start_ingestion_job.py

python prerequisites/step_33_delete_knowledge_base_restaurant-assistant-kb.py
python prerequisites/step_44_delete_knowledge_base_restaurant-policies-kb.py
python prerequisites/step_55_delete_opensearch_collection.py


Test Queries against KnowledgeBases (cross check with raw docs in kb_files)
	restaurant-assistant-kb
	What restaurants are in San Francisco?
	Does Rice & Spice restaurant have Korean Fried Chicken with gochujang? If so, how much does it cost?
	Is Tip 6 automatically added for large groups?  (No Info in KB)

	restaurant-policies-kb
	Is Tip 6 automatically added for large groups?

cd infrastructure
Create dynamoDB Table
python prerequisites/dynamodb-restaurant-assistant-create.py

Delete dynamoDB Table
python prerequisites/dynamodb-restaurant-assistant-delete.py
============================================Assets Created===========================================

============================================Assets Created===========================================

Assets created when you execute below for the first time:
step_1_create_opensearch_collection.py
step_2-create_knowledge_base_restaurant-assistant-kb.py


encryption_policy_name = {collection_name}-sp   <=== created
network_policy_name = {collection_name}-np
collection group  = "restaurant-collection-group"
collection = "restaurant-collection" (collection can have multiple indexes)

S3 bucket: restaurant-assistant-kb-{self.suffix}
SSM Parameter Store: restaurant-assistant-kb-id


knowledge_base_name = "restaurant-assistant-kb"
vector index name = f"restaurant-assistant-kb-index"

opensearchclient (created via opensearch client so it applies to opensearch. we dont attach this to any Role)
  access_policy_name = f"restaurant-assistant-kb-ap-{self.suffix}"  ==> kb & identity executing can perform opensearch collection operations

These 3 policies are attached to Knowledge Base Execution Role
kb_execution_role_name = f"BedrockExecutionRoleForKB_restaurant-assistant-kb_{self.suffix}"
   rerank_policy_name = f"BedrockRerankPolicyForKB_restaurant-assistant-kb_{self.suffix}"
   fm_policy_name = f"BedrockFoundationModelPolicyForKB_restaurant-assistant-kb_{self.suffix}"
   s3_policy_name = f"BedrockS3PolicyForKB__restaurant-assistant-kb_{self.suffix}"
   oss_policy_name = f"BedrockOSSPolicyForKB_restaurant-assistant-kb_{self.suffix}"  ==> kb can access the collection's OpenSearch APIs
    AOSS Data Access Policy
    aoss:ReadDocument
    aoss:WriteDocument
    aoss:DescribeIndex


===============================================Testcases=============================================================
agentcore dev  (for troubleshooting purposes. Run from (.venv)  MultiAgent-With-RAG-Demo\restaurantassistant> agentcore dev

streamlit run ui/non_streaming/demo_app.py
streamlit run ui/streaming/demo_app.py

Orchestrator Agent
	Policies Agent
	Restaurant Agent

Hi

Uses Policies Agent > Policies KnowledgeBase
	What is the policy regarding TIPS for large groups?

Uses Policies Agent > Policies KnowledgeBase (Semantic Retrieval Test)
	If I bring seven friends with me for dinner, will the restaurant automatically add a service charge to our check?

what did i just asked you?  (Chatbot remembers since we are using same sessionid)


Uses Restaurant Agent > Restaurant Assistant Knowledgebase Test
    What restaurants are in San Francisco?

Restaurant Agent  > Other Methods Test
	List all the bookings
	I want to book a table for 4 people for tomorrow at 6 PM for John Doe?
	Delete my booking for NutriDine


Reload Broswer
what did i just asked you? (agent doesn't remember. sessionid got reset)

Updated system prompts to fix errors/issues found during testing. May need to update more if other issues are found.
Hints:
agentcore dev (if it doesn't show any tooluse, then orchestrator prompt is possibly the issue since request did not get routed)
Ask agent to explain his reasoning as to why he said something
Most issues are prompt optimization
============================================================================================================
***Notes***

StreamLit UI (Local)  ==> calling AgentCore Runtime (Agents deployed here)

Streaming Vs Non-Streaming Versions

Using Claude Sonnet 4.6. Can also upgrade to Claude Sonnet 5 OR use Clade Opus 4.8

Using Scale-to-zero capability for cost optimization (OpenSearch NExtGen)
1st request will have a cold start of 10 seconds (to allow for the OCU to scale from zero)
After 10 minutes of inactivity, OCUs scale down to zero.

capacityLimits={
	"minIndexingCapacityInOCU": 0,
	"maxIndexingCapacityInOCU": 8,
	"minSearchCapacityInOCU": 0,    <=== $0 Idle Cost. Set to 1 to avoid cold start
	"maxSearchCapacityInOCU": 8
}

https://aws.amazon.com/blogs/aws/introducing-the-next-generation-of-amazon-opensearch-serverless-for-building-your-agentic-ai-applications/


NextGen vector search collections do not require the engine and mode parameters in index mappings.
https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vector-search.html?utm_source=chatgpt.com

Embedding Model Used: cohere.embed-english-v3
space_type: "cosinesimil"

	Alternative
	Embedding Model: amazon.titan-embed-text-v2:0
	space_type: "l2"


***Future Improvements***

Add Guardrails to RetrieveAndGenerate (guardrailId, guardrailVersion)


Right now Using Default Parser (Haven't configure it)

2 different ways to Start Re-Ingestion
1) CICD Ingestion Process (For each Environment) - Preferred
2) Trigger Lambda to start Ingestion Job for any Addition, Update or Deletion of Documents in S3 Bucket

Trigger Lambda to start Ingestion Job for any Addition, Update or Deletion of Documents in S3 Bucket that is the Data Source for Knowledgebase


Local Incremental Ingestion PRocess
aws s3 sync kb_files/ s3://my-bucket/ --delete
Start Ingestion Job


CICD Ingestion Process (For each Environment)

	1. GitHub Actions PR updates kb_files/ (add, update, delete)
	2. aws s3 sync → updates S3
	3. Python script → start_ingestion_job()

	name: Deploy Knowledge Base Documents

	on:
	workflow_dispatch:

	jobs:
	deploy-kb:
		runs-on: ubuntu-latest

		steps:
		# 1. Get repository, including kb_files/
		- name: Checkout repository
			uses: actions/checkout@v4

		# 2. Configure AWS credentials
		- name: Configure AWS credentials
			uses: aws-actions/configure-aws-credentials@v5
			with:
			role-to-assume: ${{ vars.AWS_ROLE_ARN }}
			aws-region: us-east-1

		# 3. Synchronize Git kb_files → S3
		- name: Sync KB files to S3
			run: |
			aws s3 sync kb_files/ s3://${{ vars.KB_BUCKET_NAME }}/ --delete

		# 4. Setup Python
		- name: Setup Python
			uses: actions/setup-python@v5
			with:
			python-version: "3.13"

		# 5. Install boto3
		- name: Install dependencies
			run: pip install boto3

		# 6. Start Bedrock ingestion
		- name: Start KB ingestion
			run: python scripts/start_ingestion.py
			env:
			KNOWLEDGE_BASE_ID: ${{ vars.KNOWLEDGE_BASE_ID }}
			DATA_SOURCE_ID: ${{ vars.DATA_SOURCE_ID }}