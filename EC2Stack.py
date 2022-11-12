import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Stack, aws_logs
from constructs import Construct

class EC2Stack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #change these values accordingly
        pub_key = "miAKey"
        priv_key = "miBKey"
        
        vpc = ec2.Vpc(self, "MyVpc",
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name = 'PublicSN',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24
                    ),
                ec2.SubnetConfiguration(
                    name = 'PrivateSN',
                    subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask = 24
                    )
                ]
            )
            
        #log groups (for troubleshouting)
        #log_group = aws_logs.LogGroup(self, "log_group")
        #flowlog = ec2.FlowLog(self, "FlowLogs",
        #    resource_type=ec2.FlowLogResourceType.from_vpc(vpc),
        #    destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group)
        #    )
    
        #ec2 instance creation, one associated with public subnet, one associated with private subnet 
        miA = ec2.Instance(self, "miA",
            vpc=vpc,
            instance_name="miA_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            key_name=pub_key
        )
        #allows ipv4 connections, to port 22(SSH)
        miA.connections.allow_from_any_ipv4(ec2.Port.tcp(22))
        
        #private instance
        miB1 = ec2.Instance(self, "miB1",
            vpc=vpc,
            instance_name="miB1_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            key_name=priv_key
            )
        #allows traffic from public instance
        miB1.connections.allow_from(miA, ec2.Port.all_traffic())

        #routes 
        A_B = ec2.CfnRoute(self, "A_B",
            route_table_id=vpc.public_subnets[0].route_table.route_table_id,
            destination_cidr_block=vpc.isolated_subnets[0].ipv4_cidr_block,
            instance_id=miB1.instance_id
            )
