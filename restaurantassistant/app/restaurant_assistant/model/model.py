from strands.models.bedrock import BedrockModel

# Claude Sonnet 4.6 - Application inference profile for
model_arn="arn:aws:bedrock:us-east-1:742752463290:application-inference-profile/wtv4phtvp7i1"

# Haiku 4.5 - Application Inference Profile
#model_arn="arn:aws:bedrock:us-east-1:742752463290:application-inference-profile/y9sbkw911b2k"

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
