'''
@Author David Liu

@Description: 
Lambda Handler function that manages and routes all connected API Gateway traffic
'''
from aws_lambda_powertools.event_handler import APIGatewayRestResolver #type:ignore
from aws_lambda_powertools.utilities.typing import LambdaContext #type:ignore
from aws_lambda_powertools import Logger #type:ignore

import os
import goFetch as fetch #type:ignore
import psycopg2 as psy

import api_get_users as gusrs
import api_get_organisations as orgs
import api_get_contacts as cnts
import api_post_contact as pcnts
import api_post_organisation as porg

app = APIGatewayRestResolver()
logger = Logger()

# Function for the getUsers Query
@app.get('/te_atiawa/get_users')
def getUsers():
    logger.info(f"{app.current_event}")
    return gusrs.sendTheNuke()

@app.get('/te_atiawa/get_organisations')
def getOrganisations():
    logger.info(f"{app.current_event}")
    return orgs.sendTheNuke()

@app.get('/te_atiawa/get_contacts')
def getContacts():
    logger.info(f"{app.current_event}")
    return cnts.sendTheNuke()

@app.post('/te_atiawa/create_contact')
def createContact():
    logger.info(f"{app.current_event}")
    logger.info(f"{type(app.current_event.json_body)}")
    return pcnts.sendTheNuke(app.current_event.json_body)

@app.post('/te_atiawa/create_organisation')
def createOrganisation():
    logger.info(f"{app.current_event}")
    logger.info(f"{type(app.current_event.json_body)}")
    return porg.sendTheNuke(app.current_event.json_body)

# Lambda Handler for all received traffic from the apig
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f"Received Event -> {event}")
    return app.resolve(event, context)