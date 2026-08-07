from strands.models.bedrock import BedrockModel


def load_model() -> BedrockModel:
    """Get Bedrock model client using IAM credentials."""
    return BedrockModel(model_id="arn:aws:bedrock:us-east-1:742752463290:application-inference-profile/wtv4phtvp7i1")
