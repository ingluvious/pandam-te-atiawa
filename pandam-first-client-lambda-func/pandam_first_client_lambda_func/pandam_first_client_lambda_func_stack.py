from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apig,
    aws_ec2 as ec2,
    Fn,
    CfnOutput,
    Tags
)

from dotenv import load_dotenv
import os

class PandamFirstClientLambdaFuncStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        METAVERSION = "1.2"
        PROJECT_NAME = os.getenv("PROJECT_NAME")
        ENVIRONMENT = os.getenv("ENVIRONMENT")

        STACK_NAME = f"{PROJECT_NAME}-{ENVIRONMENT}"

        DB_STACK_VPC_ID = Fn.import_value("VPC-ID")
        DB_STACK_SEC_GROUP_ID = Fn.import_value("SECURITY-GROUP-ID")
        PUBLIC_SUBNET_ONE = Fn.import_value("PublicSubnet-1")
        PUBLIC_SUBNET_TWO = Fn.import_value("PublicSubnet-2")
        ROUTE_TABLE_ONE = Fn.import_value("PublicSubnet-1-route-table")
        ROUTE_TABLE_TWO = Fn.import_value("PublicSubnet-2-route-table")

        DB_HOST = Fn.import_value("DB-HOST")
        DB_NAME = Fn.import_value("DB-NAME")
        DB_PORT = "5432"
        DB_USERNAME = Fn.import_value("DB-USERNAME")
        DB_PASSWORD = Fn.import_value("DB-PASSWORD")

        
        iam_name = f"{PROJECT_NAME}-{ENVIRONMENT}-iam-role"

        vpc_lambda_name = f"{PROJECT_NAME}-{ENVIRONMENT}-lambda-vpc"
        sec_group_name = f"{PROJECT_NAME}-{ENVIRONMENT}-sec-group"
        lambda_sec_group_name = f"{PROJECT_NAME}-{ENVIRONMENT}-lambda-sec-group"
        
        lambda_func_folder = f"lambda_function"
        lambda_handler = f"lambda_handler.lambda_handler"
        lambda_layer_folder = f"lambda_layer"

        lambda_func_handler_name = f"{PROJECT_NAME}-{ENVIRONMENT}-func"
        lambda_layer_goFetch_name = f"{PROJECT_NAME}-{ENVIRONMENT}-utility-layer"
        lambda_layer_powertools_name = f"{PROJECT_NAME}-{ENVIRONMENT}-powertools-layer"
        lambda_layer_powertools_arn = "arn:aws:lambda:ap-southeast-2:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-arm64:4"

        api_gateway_name = f"{PROJECT_NAME}-{ENVIRONMENT}-apig"

        vpc = ec2.Vpc.from_vpc_attributes(
            self, 
            vpc_lambda_name, 
            vpc_id = DB_STACK_VPC_ID,
            availability_zones = ["ap-southeast-2a", "ap-southeast-2b"],
            public_subnet_ids = [PUBLIC_SUBNET_ONE, PUBLIC_SUBNET_TWO],
            public_subnet_route_table_ids = [ROUTE_TABLE_ONE, ROUTE_TABLE_TWO]
            )
        
        sec_group = ec2.SecurityGroup.from_security_group_id(
            self, 
            sec_group_name, 
            security_group_id = DB_STACK_SEC_GROUP_ID
            )

        layer_powertools = _lambda.LayerVersion.from_layer_version_arn(
            self, 
            lambda_layer_powertools_name,
            layer_version_arn = lambda_layer_powertools_arn,
        )

        layer_goFetch = _lambda.LayerVersion(
            self,
            lambda_layer_goFetch_name,
            layer_version_name = lambda_layer_goFetch_name,
            code = _lambda.Code.from_asset(lambda_layer_folder),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_12, _lambda.Runtime.PYTHON_3_13],
            description = "DL - Custom Lambda Layer for the Lambda Handler to goFetch commonly used functions between multiple functions"
        )

        lambda_role = iam.Role(
            self,
            iam_name,
            assumed_by = iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies = [iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole")]
        )

        lambda_sec_group = ec2.SecurityGroup(
            self,
            lambda_sec_group_name,
            security_group_name = lambda_sec_group_name,
            vpc = vpc,
            description = "DL - Security Group for the Lambda Function Handler",
            allow_all_outbound = True
        )

        sec_group.add_ingress_rule(
            peer = lambda_sec_group,
            connection = ec2.Port.tcp(5432),
            description = "Allow Lambda to connect to the RDS"
        )

        lambda_func_handler = _lambda.Function(
            self, 
            lambda_func_handler_name,
            function_name = lambda_func_handler_name,
            architecture = _lambda.Architecture.X86_64,
            runtime = _lambda.Runtime.PYTHON_3_12,
            code = _lambda.Code.from_asset(lambda_func_folder),
            handler = lambda_handler,
            layers = [layer_powertools, layer_goFetch],
            role = lambda_role,
            vpc = vpc,
            vpc_subnets = ec2.SubnetSelection(
                subnet_type = ec2.SubnetType.PUBLIC
                ),
            security_groups = [lambda_sec_group],
            allow_public_subnet = True,
            timeout = Duration.seconds(20),
            memory_size = 1024,
            description = "DL - Lambda Handler to manage all traffic routed via the API Gateway",
            environment = {
                "ENVIRONMENT":ENVIRONMENT,
                "DB_HOST":DB_HOST,
                "DB_NAME":DB_NAME,
                "DB_PORT":DB_PORT,
                "DB_USERNAME":DB_USERNAME,
                "DB_PASSWORD":DB_PASSWORD
            }
        )

        # Define the API Gateways here
        te_atiawa_api = apig.RestApi(self, api_gateway_name, rest_api_name = api_gateway_name)
        te_atiawa_api_root = te_atiawa_api.root.add_resource("te_atiawa")

        # Define the GET Users API here
        r_getUser_path = te_atiawa_api_root.add_resource("get_users")
        r_getUser_path.add_method("GET", apig.LambdaIntegration(lambda_func_handler))

        # Define the GET Contacts API here
        r_getContacts_path = te_atiawa_api_root.add_resource("get_contacts")
        r_getContacts_path.add_method("GET", apig.LambdaIntegration(lambda_func_handler))

        # Define the GET Orgs API here
        r_getOrganisations_path = te_atiawa_api_root.add_resource("get_organisations")
        r_getOrganisations_path.add_method("GET", apig.LambdaIntegration(lambda_func_handler))

        # Define the POST createContact here
        r_createContact_path = te_atiawa_api_root.add_resource("create_contact")
        r_createContact_path.add_method("POST", apig.LambdaIntegration(lambda_func_handler))

        # Define the POST createOrganisation here
        r_createOrg_path = te_atiawa_api_root.add_resource("create_organisation")
        r_createOrg_path.add_method("POST", apig.LambdaIntegration(lambda_func_handler))

        # Define the PATCH updateContact here
        r_updateContact_path = te_atiawa_api_root.add_resource("update_contact")
        p_updateContact = r_updateContact_path.add_resource("{contact_uuid}")
        p_updateContact.add_method("PATCH", apig.LambdaIntegration(lambda_func_handler))

        # Define the PATCH updateOrganisation here
        r_updateOrg_path = te_atiawa_api_root.add_resource("update_organisation")
        p_updateOrg = r_updateOrg_path.add_resource("{org_id}")
        p_updateOrg.add_method("PATCH", apig.LambdaIntegration(lambda_func_handler))

        # Define Tags Here
        Tags.of(layer_goFetch).add("applicationId", STACK_NAME)
        Tags.of(layer_powertools).add("applicationId", STACK_NAME)
        Tags.of(lambda_role).add("applicationId", STACK_NAME)
        Tags.of(lambda_func_handler).add("applicationId", STACK_NAME)
        Tags.of(vpc).add("applicationId", STACK_NAME)
        Tags.of(sec_group).add("applicationId", STACK_NAME)
        Tags.of(lambda_sec_group).add("applicationId", STACK_NAME)
        Tags.of(te_atiawa_api).add("applicationId", STACK_NAME)

        # Set the Stack Description Here
        self.template_options.description = f"Stack that manages the lambda function and API Gateway for the Client Te Atiawa - Connects to the Pandam DB"
