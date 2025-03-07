#!/usr/bin/env python3

import aws_cdk as cdk

from pandam_first_client_lambda_func.pandam_first_client_lambda_func_stack import PandamFirstClientLambdaFuncStack
from dotenv import load_dotenv
import os

load_dotenv()

account = os.getenv("AWS_ACCOUNT_ID")
region = os.getenv("AWS_REGION")

stackName = f"{os.getenv("STACK_NAME")}-{os.getenv("ENVIRONMENT")}"

app = cdk.App()
PandamFirstClientLambdaFuncStack(app, stackName,
                                 env = cdk.Environment(account = account, region = region))

app.synth()