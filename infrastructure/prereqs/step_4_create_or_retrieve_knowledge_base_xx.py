# Create a new KnowledgeBase with underlying Vector Index in OpenSearch Serverless NextGen. Follow step_0_orchestrator.py

if __name__ == "__main__":

    region_name="us-east-2"

    collection_group_name = "restaurant-collection-group"  #Needed for OpenSearch Serverless NextGen
    collection_name = "restaurant-collection"

    #Knowledge Base Name and Description
    knowledge_base_name = ""
    knowledge_base_description = ""

    #Knowledge Base will be created for these Files (Vector Embeddings Will be stored in OpenSearch Serverless Vector Index)
    kb_files_path = ""

