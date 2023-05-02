import boto3

ec2_client = boto3.client('ec2', region_name='us-east-1')

new_vpc = ec2_client.create_vpc(
    CidrBlock='10.0.0.0/16',
    TagSpecifications=[
        {
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'dev-vpc'
                },
            ]
        },
    ],
)

new_subnet_1 = ec2_client.create_subnet(
    CidrBlock='10.0.1.0/24',
    VpcId=new_vpc['VpcId']
)

new_subnet_2 = ec2_client.create_subnet(
    CidrBlock='10.0.2.0/24',
    VpcId=new_vpc['VpcId']
)

all_available_vpcs = ec2_client.describe_vpcs()
vpcs = all_available_vpcs['Vpcs']

for vpc in vpcs:
    print(vpc['VpcId'])
    cidr_block_asso_sets = vpc['CidrBlockAssociationSet']
    for asso_set in cidr_block_asso_sets:
        print(asso_set['CidrBlockState'])
