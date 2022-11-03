import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class EC2Stack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #vpc
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
        vpcID = vpc.vpc_id
        
        #amazon machine image, for ec2 instances
        linux_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
        
        #ec2 instance creation, one associated with public subnet, two associated with privates subnets  
        miA = ec2.Instance(self, "miA",
            vpc=vpc,
            instance_name="miiA_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=linux_ami
            )
        miB1 = ec2.Instance(self, "miB1",
            vpc=vpc,
            instance_name="miiB1_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=linux_ami
            )
        miB2 = ec2.Instance(self, "miB2",
            vpc=vpc,
            instance_name="miiB2_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=linux_ami
            )

        #routes public ec2's associated public subnet to the two isolated subnets
        A_B1 = ec2.CfnRoute(self, "A_B1",
            route_table_id=vpc.public_subnets[0].route_table.route_table_id,
            destination_cidr_block=vpc.isolated_subnets[0].ipv4_cidr_block,
            instance_id=miB1.instance_id
            )
        A_B2 = ec2.CfnRoute(self, "A_B2",
            route_table_id=vpc.public_subnets[0].route_table.route_table_id,
            destination_cidr_block=vpc.isolated_subnets[1].ipv4_cidr_block,
            instance_id=miB2.instance_id
            )
            
