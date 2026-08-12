import json
import boto3


# Attaches an inline IAM policy (from a JSON file) to the specified IAM role.
def attach_inline_policy(role_arn, policy_file, policy_name: str = "InlinePolicy") -> None:
    """
    Attaches an inline IAM policy (from a JSON file) to the specified IAM role.

    Args:
        role_arn (str): The ARN of the IAM role.
        policy_file (str): Path to the JSON file containing the policy definition.
        policy_name (str): Name for the inline policy. Defaults to "InlinePolicy".
    """
    # Extract role name from ARN
    if ":role/" not in role_arn:
        raise ValueError("Invalid IAM role ARN format.")
    role_name = role_arn.split(":role/")[-1].split("/")[-1]

    # Read policy from JSON file
    with open(policy_file, "r", encoding="utf-8") as f:
        policy_doc = json.load(f)

    # Attach inline policy
    iam = boto3.client("iam")
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_doc),
    )

    print(f"✅ Inline policy '{policy_name}' attached to role '{role_name}'.")


if __name__ == "__main__":
    # Attach the inline policy to AgentCore Runtime execution role which AgentCore Runtime assumes to run an agent
	attach_inline_policy(
    role_arn="arn:aws:iam::742752463290:role/AgentCore-restaurantassis-ApplicationAgentRestauran-Nmpr715x73h6",
    policy_file="agentcore-extra-inline-policy.json",
    policy_name="ExtraInlinePolicy")


# 	# restaurant-assistant-kb-id  L19PD9QCH9
#     # restaurant-policies-kb-id   WGLZD3BW3C
#     print(get_kb_id("restaurant-assistant-kb"))
#     print()  # blank line
#     print(get_kb_id("restaurant-policies-kb"))