from strands.models.bedrock import BedrockModel

# application inference profile for Claude Sonnet 4.6
model_arn="arn:aws:bedrock:us-east-1:742752463290:application-inference-profile/wtv4phtvp7i1"

# cohere.rerank-v3-5:0
rerank_model_arn="arn:aws:bedrock:us-east-1::foundation-model/cohere.rerank-v3-5:0"

def load_model() -> BedrockModel:
    """Get Bedrock model client using IAM credentials."""
    return BedrockModel(model_id=model_arn)

def get_model_arn() -> str:
	"""Get the ARN of the Bedrock model."""
	return model_arn

def get_rerank_model_arn() -> str:
	"""Get the ARN of the Rerank Bedrock model."""
	return rerank_model_arn
