CDK cloudformation template

VPC with 2 subnets, public and private

2 instances, one in the public(A), one in the private(B)

SSH connection to instance A, and connect from there to other private instance(s)

public instance acts as managerial overseeer

-----------------------------------------------------

git clone https://github.com/Asilomare/CDKNetwork ./ 

cdk deploy

aws ec2 describe-instances
#find "PublicIp"
#make key pair in ec2 key manager

ssh -i "keypair.pem" "PublicIp"
