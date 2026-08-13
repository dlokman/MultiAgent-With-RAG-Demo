"""Restaurant Agent for restaurant queries and booking management."""

import json
import os
from datetime import datetime
import boto3
from constants.constants import RESTAURANT_ASSISTANT_KB_NAME
from model.model import get_rerank_model_arn, load_model, get_model_arn
from strands import Agent, tool
from strands.models import BedrockModel
from utils import utils
import uuid
import logging
from strands_tools import current_time

log = logging.getLogger(__name__)

RESTAURANT_ASSISTANT_KNOWLEDGE_BASE_ID = utils.get_kb_id(kb_name=RESTAURANT_ASSISTANT_KB_NAME)

bedrock_runtime = boto3.client('bedrock-agent-runtime')
dynamodb = boto3.resource("dynamodb")

db_table_name = utils.get_db_table_name(kb_name=RESTAURANT_ASSISTANT_KB_NAME)
db_table = dynamodb.Table(db_table_name)


@tool()
def restaurant_assistant_kb_retrieve(query: str) -> str:
    """Use this tool to retrieve restaurant information from the restaurant assistant Knowledge Base,
	   including restaurant names, addresses, phone numbers, menus, menu items, and prices.

	   Args:
			query: The user's question about restaurants, restaurant details, menus, menu items, or prices.

	   Returns:
			A response containing relevant restaurant information retrieved from the Knowledge Base.
    """

    if not RESTAURANT_ASSISTANT_KNOWLEDGE_BASE_ID:
        log.error("RESTAURANT_ASSISTANT_KNOWLEDGE_BASE_ID is not set up. Please check the configuration.")
        return "RESTAURANT_ASSISTANT_KNOWLEDGE_BASE_ID is not set up. Please check the configuration."
	# https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html
    params = {
				"input": {"text": query},
				"retrieveAndGenerateConfiguration": {
					'type': 'KNOWLEDGE_BASE',
					'knowledgeBaseConfiguration': {
						'knowledgeBaseId': RESTAURANT_ASSISTANT_KNOWLEDGE_BASE_ID,
						'modelArn': get_model_arn(),
						'retrievalConfiguration': {
							'vectorSearchConfiguration': {
								'numberOfResults': 7,
								"overrideSearchType": "HYBRID",
                                "rerankingConfiguration": {
									"type": "BEDROCK_RERANKING_MODEL",
									"bedrockRerankingConfiguration": {
										"modelConfiguration": {
											"modelArn": get_rerank_model_arn()
										},
										"numberOfRerankedResults": 3
									}
								}
							 }
						  }
					}
				}
    		}


    try:
        response = bedrock_runtime.retrieve_and_generate(**params)
        return response.get("output", {}).get("text", "No relevant information found in the restaurant assistant Knowledge Base.")
    except Exception as e:
        log.error(f"Failed to retrieve information from restaurant assistant knowledge base: {type(e).__name__}: {str(e)}", exc_info=True)
        return f"Failed to retrieve information from restaurant assistant knowledge base:"

@tool
def create_booking(date: str, hour: str, restaurant_name: str, guest_name: str, num_guests: str) -> str:
    """Create a new booking at restaurant_name
    Args:
        date: The date of the booking in the format YYYY-MM-DD.
        hour:the hour of the booking in the format HH:MM"
        restaurant_name:The name of the restaurant handling the reservation"
        guest_name: The name of the customer to have in the reservation"
        num_guests: The number of guests for the booking"

    Returns:
        confirmation_message: confirmation message
    """

    print(f"Creating reservation for {num_guests} people at {restaurant_name}, {date} at {hour} in the name of {guest_name}")

    try:
        booking_id = str(uuid.uuid4())[:8]
        db_table.put_item(
            Item={
                "booking_id": booking_id,
                "restaurant_name": restaurant_name,
                "date": date,
                "name": guest_name,
                "hour": hour,
                "num_guests": num_guests
            }
        )
        return f"Reservation created with booking id: {booking_id}"
    except Exception as e:
        log.error(f"Failed to create booking: {type(e).__name__}: {str(e)}", exc_info=True)
        return "Failed to create booking."

@tool
def get_booking_details(booking_id: str, restaurant_name: str) -> dict:
    """Get details for a restaurant Booking given a booking_id and restaurant_name
    Args:
        booking_id: the id of the reservation
        restaurant_name: name of the restaurant handling the reservation

    Returns:
        booking_details: the details of the booking in JSON format
    """

    try:
        response = db_table.get_item(Key={"booking_id": booking_id, "restaurant_name": restaurant_name})

        if "Item" in response:
            return response["Item"]
        else:
            return f"No booking found with ID {booking_id}"
    except Exception as e:
        log.error(f"Failed to get booking details: {type(e).__name__}: {str(e)}", exc_info=True)
        return "Failed to get booking details"

@tool
def delete_booking(booking_id: str, restaurant_name: str) -> str:
    """Delete an existing booking_id at restaurant_name
    Args:
        booking_id: the id of the reservation
        restaurant_name: name of the restaurant handling the reservation

    Returns:
        confirmation_message: confirmation message
    """
    try:
        response = db_table.delete_item(Key={"booking_id": booking_id, "restaurant_name": restaurant_name})

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return f"Booking with ID {booking_id} deleted successfully"
        else:
            return f"Failed to delete booking with ID {booking_id}"
    except Exception as e:
        log.error(f"Failed to delete booking with ID {booking_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        return f"Failed to delete booking with ID {booking_id}"

@tool
def list_all_bookings() -> dict:
    """List all bookings across all restaurants in the system.

    Returns:
        A dictionary containing all restaurant bookings or an error message.
    """
    try:
        response = db_table.scan()
        bookings = response.get("Items", [])

        # Continue scanning if DynamoDB returns paginated results
        while "LastEvaluatedKey" in response:
            response = db_table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            bookings.extend(response.get("Items", []))

        return {
            "bookings": bookings
        }

    except Exception as e:
        log.error(f"Failed to list all bookings: {type(e).__name__}: {str(e)}", exc_info=True)
        return {"Failed to list all bookings"}


restaurant_assistant_agent = Agent(
    name="restaurant_assistant_agent",
	description="An agent that specializes in restaurant information, menus, pricing, and restaurant booking management.",
    model=load_model(),
    system_prompt="""
		You are the Restaurant Agent, a specialized agent responsible for restaurant information, menus, and booking management.
        You have tools to create, retrieve, delete and list bookings and get restaurant information

		## Instructions
		- Answer questions about restaurant names, addresses, phone numbers, menus, menu items, and prices using the restaurant assistant knowledge base retrieval tool
		- Handle booking operations using the appropriate available booking tools.
        - If date is not provided by user, ask for it before creating a booking. If the user request a booking with terms like create a booking for today, yesterday, tomorrow, next week etc then ask for a specific date when the booking is needed.
          Do not assume or calculate what the date is. Once the user provides a specific date, format that date per tool description to create the booking.
		- ALWAYS verify that the restaurant exists in the restaurant directory using the restaurant assistant knowledge base before creating a booking.
		- NEVER assume missing parameter values when calling a tool. If required information is missing, clearly indicate what information is needed.
		- Only answer using information obtained using available tools. Do not use your own knowledge or invent restaurant, menu, pricing, or booking information.
		- Never claim that a booking was created, retrieved, updated, or deleted unless the corresponding tool confirms the result.
		- If a knowledge base or booking tool does not provide enough information, clearly indicate what information could not be found or what additional information is needed.
		- Only handle restaurant information, menu, pricing, and booking-related tasks.
		- If a request is outside your scope, indicate that it is outside your scope so the orchestrator can route it appropriately.

		## Output Instructions
		- Return relevant restaurant, menu, pricing, or booking information needed by the orchestrator.
		- Clearly indicate when a tool fails or the requested information cannot be found.
		- Do not add introductions, greetings, or unnecessary conversational language.
		""",
    tools=[restaurant_assistant_kb_retrieve, create_booking, get_booking_details, delete_booking, list_all_bookings, current_time]
)
