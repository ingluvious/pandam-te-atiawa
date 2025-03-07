'''
File that gets a list of users from the database and returns in JSON
'''
from aws_lambda_powertools import Logger #type:ignore
import db_queries as seek #type:ignore
import goFetch as fetch #type:ignore

logger = Logger()

def sendTheNuke(payload):
    logger.info(f"Received request. Doing the thing!")
    return fetch.upsertData(payload, table_name = "contact")