'''
@Author: David Liu

@Description: 
Pandam Database Stack. Set up the initial Pandam Database

@Notes: 
Make the DB public and remove the Private NAT Gateways to save on costs
Export DB values to the env so that the other stacks can reference
'''

from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_apigateway as api,
    SecretValue,
    Duration,
    CfnOutput,
    RemovalPolicy,
    Tags
)
from constructs import Construct
from dotenv import load_dotenv

import os

load_dotenv(override = True)

class PandamDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the project names here
        db_identifier = f"{os.getenv("DB_IDENTIFIER")}"
        db_name = f"{os.getenv("DB_NAME")}"
        db_port = f"{os.getenv("DB_PORT")}"
        db_port_int = 5432
        db_username = f"{os.getenv("DB_USERNAME")}"
        db_password = f"{os.getenv("DB_PASSWORD")}"

        project_name = "pandamDB-dev"

        rds_name = f"{project_name}-rds"
        vpc_name = f"{project_name}-vpc"
        security_group_name = f"{project_name}-security-group"

        dl_public_ip = f"{os.getenv("DL_PUBLIC_IP")}/32"
        dl_public_ip_two = f"{os.getenv("DL_PUBLIC_IP_TWO")}/32"
        ja_public_ip = f"{os.getenv("JA_PUBLIC_IP")}/32"
        ja_public_ip_two = f"{os.getenv("JA_PUBLIC_IP_TWO")}/32"
        ja_public_ip_three = f"{os.getenv("JA_PUBLIC_IP_THREE")}/32"

        # Create and specify public VPC
        vpc = ec2.Vpc(
            self, 
            vpc_name, 
            vpc_name = vpc_name,
            cidr = "10.0.0.0/16",
            max_azs =  2,
            # availability_zones = ["ap-southeast-2a", "ap-southeast-2b"], # Define the Availability Zones here
            nat_gateways = 0, # Specify the NAT Gateways here to be 0
            subnet_configuration = [ec2.SubnetConfiguration(
                name = "PublicSubnet",
                subnet_type = ec2.SubnetType.PUBLIC,
                cidr_mask = 24,
            )] 
        )

        # Create the outputs of the Public Subnets here
        for number, subnet in enumerate(vpc.public_subnets):
            CfnOutput(self, f"PublicSubnet-{number + 1}-Output", value = subnet.subnet_id, export_name = f"PublicSubnet-{number + 1}")
            CfnOutput(self, f"PublicSubnet-{number + 1}-Output-routeTable", value = subnet.route_table.route_table_id, export_name = f"PublicSubnet-{number + 1}-route-table")


        # Create the Security Group here
        rds_security_group = ec2.SecurityGroup(
            self,
            rds_name,
            security_group_name = security_group_name,
            vpc = vpc,
            description = "Access to Pandam Database",
            allow_all_outbound = True
        )
        rds_security_group.add_ingress_rule(
            peer = ec2.Peer.ipv4(dl_public_ip_two),
            connection = ec2.Port.tcp(db_port_int),
            description = "All PostgreSQL traffic from DL public IP - Hotspot"
        )
        rds_security_group.add_ingress_rule(
            peer = ec2.Peer.ipv4(dl_public_ip),
            connection = ec2.Port.tcp(db_port_int),
            description = "All PostgreSQL traffic from DL public IP - Home"
        )
        rds_security_group.add_ingress_rule(
            peer = ec2.Peer.ipv4(ja_public_ip),
            connection = ec2.Port.tcp(db_port_int),
            description = "All PostgreSQL traffic from JA public IP - Home"
        )
        rds_security_group.add_ingress_rule(
            peer = ec2.Peer.ipv4(ja_public_ip_two),
            connection = ec2.Port.tcp(db_port_int),
            description = "All PostgreSQL traffic from JA public IP - Alternative Place"
        )
        rds_security_group.add_ingress_rule(
            peer = ec2.Peer.ipv4(ja_public_ip_three),
            connection = ec2.Port.tcp(db_port_int),
            description = "All PostgreSQL traffic from JA public IP - Alternative Place II"
        )
        
        # Create the DB Instance here
        db_instance = rds.DatabaseInstance(
            self, 
            db_identifier,
            instance_identifier = db_identifier,
            engine = rds.DatabaseInstanceEngine.postgres(
                version = rds.PostgresEngineVersion.VER_17_2
            ),
            instance_type = ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.MICRO
            ),
            security_groups = [rds_security_group],
            vpc = vpc,
            vpc_subnets = ec2.SubnetSelection(
                subnet_type = ec2.SubnetType.PUBLIC
            ),
            allocated_storage = 20,
            max_allocated_storage = 1000,
            storage_encrypted = True,
            multi_az = False,
            auto_minor_version_upgrade = False,
            publicly_accessible = True,
            database_name = db_name,
            credentials = rds.Credentials.from_password(
                username = db_username,
                password = SecretValue.unsafe_plain_text(db_password)
            )
        )

        # Make the outputs here
        CfnOutput(self, "VPC-ARN", value = vpc.vpc_arn, export_name = "VPC-ARN")
        CfnOutput(self, "VPC-ID", value = vpc.vpc_id, export_name = "VPC-ID")

        CfnOutput(self, "SECURITY-GROUP-ID", value = rds_security_group.security_group_id, export_name = "SECURITY-GROUP-ID")
        CfnOutput(self, "DB-ARN", value = db_instance.instance_arn, export_name = "DB-ARN")
        CfnOutput(self, "DB-HOST", value = db_instance.db_instance_endpoint_address, export_name = "DB-HOST")

        CfnOutput(self, "DB-IDENTIFIER", value = db_identifier, export_name = "DB-IDENTIFIER")
        CfnOutput(self, "DB-NAME", value = db_name, export_name = "DB-NAME")
        CfnOutput(self, "DB-PORT", value = db_port, export_name = "DB-PORT")
        CfnOutput(self, "DB-USERNAME", value = db_username, export_name = "DB-USERNAME")
        CfnOutput(self, "DB-PASSWORD", value = db_password, export_name = "DB-PASSWORD")