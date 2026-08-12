import json

import boto3


def get_kb_id(kb_name):
    smm_client = boto3.client("ssm")
    kb_id = smm_client.get_parameter(Name=f"{kb_name}-id", WithDecryption=False)
    print("Knowledge Base Id:", kb_id["Parameter"]["Value"])
    return kb_id["Parameter"]["Value"]


def get_db_table_name(kb_name):
    smm_client = boto3.client("ssm")
    table_name = smm_client.get_parameter(
        Name=f"{kb_name}-table-name", WithDecryption=False
    )
    print("DynamoDB table:", table_name["Parameter"]["Value"])
    return table_name["Parameter"]["Value"]