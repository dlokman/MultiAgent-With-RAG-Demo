import argparse
import os

import boto3
import yaml
from boto3.session import Session
from dynamodb import AmazonDynamoDB

if __name__ == "__main__":

    knowledge_base_name = 'restaurant-assistant-kb'
    table_name = 'restaurant-assistant-bookings'
    pk_item = 'booking_id'
    sk_item = 'restaurant_name'

    dynamodb = AmazonDynamoDB(region_name="us-east-1")

    dynamodb.create_dynamodb(
        knowledge_base_name,
        table_name,
        pk_item,
        sk_item,
    )

    print(f"Table Name: {table_name}")

