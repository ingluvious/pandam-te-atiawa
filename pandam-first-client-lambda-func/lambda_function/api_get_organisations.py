'''
File that gets a list of users from the database and returns in JSON
'''
from aws_lambda_powertools import Logger #type:ignore
import db_queries as seek #type:ignore
import goFetch as fetch #type:ignore

logger = Logger()

def sendTheNuke():
    logger.info(f"Received request. Doing the thing!")
    QUERY = seek.getOrganisationsQuery()
    
    dictionary_rows, rows = fetch.getData(QUERY)
    row_count = len(rows)
    
    logger.info(f"We got some data -> {dictionary_rows} -> And the rows -> {rows}")
    
    response_data = {
            "statusCode":200,
            "row_count":row_count,
            "data":[
                    {
                    "orgId":row["org_id"],
                    "fields":{key:value for key, value in row.items()}
                    }
                for row in dictionary_rows
                ]
            }
    return fetch.jsonDump(response_data), 200