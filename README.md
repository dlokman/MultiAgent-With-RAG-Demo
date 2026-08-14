# Multi-Agent With RAG Demo (AgentCore with Strands Agents)

This is a Restaurant Chatbot Demo of Multi-Agents with RAG.

This project combines both **GenAI** and **Agentic AI**.

## Tech Stack
- **Architecture:** AWS-Native Tech Stack
- **Project Setup:** UV-based project created using the AgentCore CLI
- **Hosting Platform:** Amazon Bedrock AgentCore
- **AI Agent Framework:** Strands Agents SDK
- **Programming Language:** Python
- **Vector Store:** Amazon OpenSearch Serverless
- **Other AWS Services & Technologies:**
  - Amazon Bedrock
  - Amazon Bedrock Knowledge Bases
  - Amazon DynamoDB
  - Amazon S3
  - Streamlit

## 🏗️ Architecture Overview
![architecture](Architecture-Diagram.svg)

## 🌟 Project Overview

### Models

- **Foundation Model:** Claude Sonnet 4.6
- **Embedding Model:** Cohere Embed English v3
  - Model: `cohere.embed-english-v3`
  - Similarity Metric: `cosinesimil` (Cosine Similarity)
- **Reranker Model:** Cohere Rerank 3.5
  - Model: `cohere.rerank-v3-5:0`

### OpenSearch Serverless (Next-Generation)

This project uses **Amazon OpenSearch Serverless (Next-Generation)** as the vector store.

The next generation of Amazon OpenSearch Serverless became generally available on **May 28, 2026** and introduced **Scale to Zero**, which provides **$0 idle compute cost**. This makes OpenSearch Serverless more cost-effective and practical for small projects and workloads with intermittent usage.

**References:**
- [Amazon OpenSearch Serverless Next-Generation – General Availability](https://aws.amazon.com/about-aws/whats-new/2026/05/amazon-opensearch-serverless-next-generation-generally-available/)
- [Introducing the Next Generation of Amazon OpenSearch Serverless](https://aws.amazon.com/blogs/aws/introducing-the-next-generation-of-amazon-opensearch-serverless-for-building-your-agentic-ai-applications/)

---

## 🗺️ Implementation Overview

### 1. Create Two Knowledge Bases

Create two **Amazon Bedrock Knowledge Bases**:

- **Restaurant Assistant Knowledge Base** — used by the Restaurant Assistant Agent
- **Policies Knowledge Base** — used by the Policies Agent

### 2. Create Two Vector Indexes

Create two vector indexes in **Amazon OpenSearch Serverless**:

- One index for the **Restaurant Assistant Knowledge Base**
- One index for the **Policies Knowledge Base**

### 3. Create Two Data Sources

Create a separate data source for each Knowledge Base. Each data source uses its own **Amazon S3 bucket**:

- **Restaurant Assistant S3 Bucket**
- **Policies S3 Bucket**

### 4. Create a DynamoDB Table

Create one **Amazon DynamoDB** table for storing and managing restaurant bookings.

### 5. RAG Setup — Ingestion Process

1. **Upload documents to each S3 bucket**
   - **Restaurant Assistant S3 Bucket:** Upload all `.docx` files containing restaurant menu information and the restaurant directory.
   - **Policies S3 Bucket:** Upload all `.docx` files containing restaurant policy information.

2. **Start the ingestion process for each Knowledge Base**
   - This process generates **vector embeddings** for the documents stored in S3.
   - The vector embeddings are stored in the corresponding **Amazon OpenSearch Serverless vector indexes**.

### 6. Create the Multi-Agent System

Create:

- **1 Orchestrator Agent**
- **2 Specialized Agents**
  - Restaurant Assistant Agent
  - Policies Agent

The **Orchestrator Agent's conversation history is preserved** across requests as long as the same session ID is used.

The **Specialized Agents' conversation history is reset** for each new request, keeping them stateless between Orchestrator requests.

---

## 🤖 Agent Routing and Data Access

The **Orchestrator Agent** routes each user request to the appropriate Specialized Agent based on its system prompt and the task being requested.

### Restaurant Assistant Agent

The Restaurant Assistant Agent handles restaurant information and booking operations.

For booking operations, it uses **Amazon DynamoDB**:

- Get Booking
- Create Booking
- Delete Booking
- List Bookings

For questions that can be answered from the ingested restaurant documents, the agent uses the **Restaurant Assistant Knowledge Base** to perform semantic retrieval against the content stored in the OpenSearch Serverless vector index.

### Policies Agent

The Policies Agent handles restaurant policy questions.

It uses the **Policies Knowledge Base** to perform semantic retrieval against the policy documents stored in the OpenSearch Serverless vector index.


## 🌟 Project Setup

This project contains two main folders:

1. **`infrastructure/`** — Contains the prerequisite and infrastructure scripts used to provision the required AWS resources.
2. **`restaurantassistant/`** — Contains the AgentCore application built using the Strands Agents SDK.

The source documents for the Knowledge Base S3 buckets are located in:

```text
infrastructure/prerequisites/kb_files/
```

---

### 1. Prerequisites

#### A. Provision Resources and Start Ingestion Jobs

The following steps provision the required resources and start the Knowledge Base ingestion jobs. Documents uploaded to S3 will be processed, vector embeddings will be generated, and the embeddings will be stored in the corresponding Amazon OpenSearch Serverless vector indexes.

Navigate to the `infrastructure` folder:

```bash
cd infrastructure
```

Add the Restaurant Assistant `.docx` files to:

```text
infrastructure/prerequisites/kb_files/restaurant_assistant/
```

Add the Restaurant Policies `.docx` files to:

```text
infrastructure/prerequisites/kb_files/restaurant_policies/
```

Run the prerequisite scripts:

```bash
uv run prerequisites/step_1_create_opensearch_collection.py

uv run prerequisites/step_2-create_knowledge_base_restaurant-assistant-kb.py

uv run prerequisites/step_2-create_knowledge_base_restaurant-policies-kb.py
```

> **Note:** The Knowledge Base creation scripts also start the ingestion jobs for their respective Knowledge Bases.

#### B. Deploy Agents to AgentCore Runtime

Navigate to the `restaurantassistant` folder and deploy the application:

```bash
agentcore deploy
```

---

### 2. Post-Deployment Setup

Attach the required policy to the **AgentCore Runtime execution role** by running `utils.py`.

Before running the script, update it with the correct AgentCore Runtime `RoleName`.

From the `infrastructure/post_deployment` folder, run:

```bash
uv run utils.py
```

---

### 3. Run the Streamlit UI

The Streamlit UI runs locally and invokes the agents deployed to **AgentCore Runtime**.

From the following folder:

```text
restaurantassistant/app/restaurant_assistant/
```

#### Non-Streaming UI

```bash
streamlit run ui/non_streaming/demo_app.py
```

#### Streaming UI

```bash
streamlit run ui/streaming/demo_app.py
```

---

## 🔄 Re-Run Knowledge Base Ingestion

After adding, updating, or deleting documents in `kb_files`, re-run the Knowledge Base ingestion job.

Update `step_22_start_ingestion_job.py` as needed, then run:

```bash
uv run prerequisites/step_22_start_ingestion_job.py
```

---

## 🧹 Delete Resources

### Delete the Restaurant Policies Knowledge Base

```bash
uv run prerequisites/step_33_delete_knowledge_base_restaurant-policies-kb.py
```

### Delete the Restaurant Assistant Knowledge Base

```bash
uv run prerequisites/step_44_delete_knowledge_base_restaurant-assistant-kb.py
```

### Delete the OpenSearch Collection

```bash
uv run prerequisites/step_55_delete_opensearch_collection.py
```


## 🌟 Assets Created

The following AWS resources are created when these scripts are executed for the first time:

```bash
step_1_create_opensearch_collection.py
step_2-create_knowledge_base_restaurant-assistant-kb.py
```

> **Note:** Running `step_2-create_knowledge_base_restaurant-policies-kb.py` creates a Knowledge Base named `restaurant-policies-kb` along with equivalent supporting resources.

---

### Amazon Bedrock Knowledge Base

```text
Knowledge Base Name: restaurant-assistant-kb
```

---

### Amazon OpenSearch Serverless

#### Collection Group

```text
Collection Group Name: restaurant-collection-group
```

#### Collection

```text
Collection Name: restaurant-collection
```

> A single OpenSearch Serverless collection can contain multiple indexes.

#### Security and Access Policies

```text
Encryption Policy: restaurant-collection-sp
Network Policy:    restaurant-collection-np
Data Access Policy: restaurant-assistant-kb-ap-{suffix}
```

The **Data Access Policy** allows the Knowledge Base and the configured IAM principal to perform operations against the OpenSearch Serverless collection.

This is an **OpenSearch Serverless data access policy**, so it applies directly to OpenSearch Serverless resources and is not attached to an IAM role like a standard IAM policy.

#### Vector Index

```text
Vector Index Name: restaurant-assistant-kb-index
```

---

### Amazon S3

The S3 bucket stores the source documents used by the Knowledge Base.

```text
Bucket Name: restaurant-assistant-kb-{suffix}
```

---

### AWS Systems Manager Parameter Store

The Knowledge Base ID is stored in SSM Parameter Store:

```text
Parameter Name: restaurant-assistant-kb-id
```

---

### Knowledge Base Execution Role

The following IAM execution role is created for the Knowledge Base:

```text
BedrockExecutionRoleForKB_restaurant-assistant-kb_{suffix}
```

The following four IAM policies are attached to the Knowledge Base execution role:

#### 1. Reranking Model Policy

```text
BedrockRerankPolicyForKB_restaurant-assistant-kb_{suffix}
```

Provides the permissions required to invoke the configured reranking model.

#### 2. Foundation Model Policy

```text
BedrockFoundationModelPolicyForKB_restaurant-assistant-kb_{suffix}
```

Provides the permissions required to invoke the configured Bedrock model.

#### 3. S3 Access Policy

```text
BedrockS3PolicyForKB_restaurant-assistant-kb_{suffix}
```

Provides the Knowledge Base with access to the S3 bucket containing the source documents.

#### 4. OpenSearch Serverless Policy

```text
BedrockOSSPolicyForKB_restaurant-assistant-kb_{suffix}
```

Provides the Knowledge Base execution role with the required IAM permissions for Amazon OpenSearch Serverless.

In addition, this Policy grants the Knowledge Base execution role permissions to access the collection's OpenSearch APIs, such as:

```text
aoss:ReadDocument
aoss:WriteDocument
aoss:DescribeIndex
aoss:CreateCollectionItems
```


## 📝 Notes

### Foundation Model

This project currently uses **Claude Sonnet 4.6**.

Alternative models that can be used include:

- **Claude Sonnet 5**
- **Claude Opus 5**

---

### System Prompt Optimization

The system prompts have been updated to address errors and issues identified during testing. Additional prompt optimization may be required if new issues are discovered.

#### Troubleshooting Hints

- Use `agentcore dev` to test the agent locally.
- While using `agentcore dev`, if no **tooluse** is shown, then **Orchestrator system prompt** may be the issue since request did not get routed.
- Ask the agent to explain its reasoning why it produced a particular response, if the response is not what you expected.
- Many agent behavior issues can be resolved through **system prompt optimization**.

---

### OpenSearch Serverless — Scale to Zero

This project uses the **Scale to Zero** capability of Amazon OpenSearch Serverless Next-Generation for cost optimization.

- The first request after scaling to zero may experience a **cold start of approximately 10 seconds** while the OCU scales up from zero.
- After approximately **10 minutes of inactivity**, the OCUs can scale back down to zero.
- Setting `minSearchCapacityInOCU` to `0` enables **$0 idle compute cost**.
- Set `minSearchCapacityInOCU` to `1` if you want to avoid the search cold start.

```python
capacityLimits={
    "minIndexingCapacityInOCU": 0,
    "maxIndexingCapacityInOCU": 8,
    "minSearchCapacityInOCU": 0,  # $0 idle compute cost; set to 1 to avoid cold start
    "maxSearchCapacityInOCU": 8
}
```

**Reference:**

[Introducing the Next Generation of Amazon OpenSearch Serverless](https://aws.amazon.com/blogs/aws/introducing-the-next-generation-of-amazon-opensearch-serverless-for-building-your-agentic-ai-applications/)

---

### OpenSearch Serverless Vector Index

OpenSearch Serverless NextGen - vector search collections do not require the `engine` and `mode` parameters in the index mappings.

**Reference:**

[Amazon OpenSearch Serverless Vector Search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vector-search.html)

---

### Embedding Model

The project currently uses:

```text
Embedding Model: cohere.embed-english-v3
Similarity Metric (space_type): cosinesimil
```

#### Alternative

An alternative configuration is:

```text
Embedding Model: amazon.titan-embed-text-v2:0
Similarity Metric (space_type): l2
```


## 🚀 Future Improvements

### Add Guardrails

Add **Amazon Bedrock Guardrails** to the `RetrieveAndGenerate` configuration using:

```text
guardrailId
guardrailVersion
```

---

### Configure a Custom Parser

The project currently uses the **default parser** for Knowledge Base document ingestion.

A custom parser has not yet been configured.

---

### Automate Knowledge Base Re-Ingestion

There are two potential approaches for automatically starting Knowledge Base re-ingestion:

1. **CI/CD Ingestion Process (per environment)** — **Preferred**
2. **S3 Event → Lambda → Ingestion Job** — Trigger a Lambda function when documents are added, updated, or deleted in the S3 bucket used as the Knowledge Base data source.

---

### Local Incremental Ingestion Process

For local development, synchronize the local Knowledge Base documents with S3:

```bash
aws s3 sync kb_files/ s3://my-bucket/ --delete
```

Then start the Knowledge Base ingestion job:

```text
Start Ingestion Job
```

This allows document additions, updates, and deletions to be synchronized with the Knowledge Base.

---

### CI/CD Ingestion Process — Preferred

For each environment, automate document deployment and Knowledge Base ingestion through the CI/CD pipeline.

#### Workflow

```text
GitHub Repository
      │
      │ PR => Add / Update / Delete documents in kb_files/
      ▼
GitHub Actions
      │
      │ aws s3 sync --delete (updates S3 bucket with the file changes in kb_files)
      ▼
Amazon S3
      │
      │ start_ingestion_job()
      ▼
Amazon Bedrock Knowledge Base
      │
      ▼
Amazon OpenSearch Serverless
```

The process consists of:

1. Add, update, or delete documents in `kb_files/` through a GitHub pull request.
2. GitHub Actions synchronizes S3 bucket with kb_files/ using aws s3 sync --delete
3. The pipeline runs a Python script that calls `start_ingestion_job()` to synchronize the Knowledge Base with the updated S3 data source.

#### Example GitHub Actions Workflow

```yaml
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

      # 4. Set up Python
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      # 5. Install dependencies
      - name: Install dependencies
        run: pip install boto3

      # 6. Start Bedrock Knowledge Base ingestion
      - name: Start KB ingestion
        run: python scripts/start_ingestion.py
        env:
          KNOWLEDGE_BASE_ID: ${{ vars.KNOWLEDGE_BASE_ID }}
          DATA_SOURCE_ID: ${{ vars.DATA_SOURCE_ID }}
```

---

### Event-Driven Ingestion with S3 and Lambda

As an alternative to the CI/CD approach, configure S3 events to trigger a Lambda function whenever Knowledge Base documents are added, updated, or deleted.

```text
Add / Update / Delete Document
             │
             ▼
          Amazon S3
             │
          S3 Event
             │
             ▼
         AWS Lambda
             │
      start_ingestion_job()
             │
             ▼
Amazon Bedrock Knowledge Base
             │
             ▼
Amazon OpenSearch Serverless
```

The Lambda function acts as the trigger for the Knowledge Base ingestion job. The actual document parsing, chunking, embedding generation, and vector-store synchronization continue to be handled by the **Amazon Bedrock Knowledge Base ingestion process**.