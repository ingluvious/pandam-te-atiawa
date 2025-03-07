#!/usr/bin/env python3
import os
import aws_cdk as cdk
from dotenv import load_dotenv
from pandam_db_stack.pandam_db_stack import PandamDBStack

load_dotenv()

account = os.getenv("AWS_ACCOUNT_ID")
region = os.getenv("REGION")

app = cdk.App()
PandamDBStack(app, "PandamDBStack",
    env=cdk.Environment(account='779846811053', region='ap-southeast-2'),
    )

app.synth()