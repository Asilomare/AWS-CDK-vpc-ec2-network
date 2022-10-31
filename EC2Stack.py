import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class EC2Stack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
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
        
        linux_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
            
        miA = ec2.Instance(self, "miA",
            vpc=vpc,
            instance_name="miiA_name",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType(instance_type_identifier="t2.nano"),
            machine_image=linux_ami
            )
        #priv instances
        #selection for putting instances in specfic subnets
        privSelection = vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
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
        #endpoint for priv_iso subnets 1 and 2
        endpoint1 = ec2.InterfaceVpcEndpoint(self, "Endpoint1",
            vpc=vpc,
            subnets=privSelection[0]
            )
        endpoint2 = ec2.InterfaceVpcEndpoint(self, "Endpoint2",
            vpc=vpc,
            subnets=privSelection[1]
            )
        EP1ID = endpoint1.vpc_endpoint_id
        EP2ID = endpoint2.vpc_endpoint_id
        
        #https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#RouteTables
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ec2/CfnLocalGatewayRoute.html?highlight=local%20route%20table#aws_cdk.aws_ec2.CfnLocalGatewayRoute.local_gateway_route_table_id
        CRT = ec2.CfnRouteTable(self, "CRT",
            vpc_id=vpcID
            )
        RTID = CRT.attr_route_table_id
        #association = CRT.CfnRouteTableAssociation(self,
         #   )
    
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ec2/CfnRoute.html
        #A_B1 = ec2.CfnRoute(self, "A_B1",
            #route_table_id=RTID,
            #destination = vpc.private_subnets[0]
            #target=local
            #)
            
        #find gatewayid for private subnets, target = that, destiniation = ip of subnet
        #look into ENI's for connection tables