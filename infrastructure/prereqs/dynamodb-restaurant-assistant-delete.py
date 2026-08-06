import argparse
import os

import boto3
import yaml
from boto3.session import Session
from dynamodb import AmazonDynamoDB

if __name__ == "__main__":

    knowledge_base_name = 'restaurant-assistant-kb'
    table_name = 'restaurant-assistant-bookings'

    dynamodb = AmazonDynamoDB(region_name="us-east-1")

    dynamodb.delete_dynamodb_table(knowledge_base_name, table_name)
