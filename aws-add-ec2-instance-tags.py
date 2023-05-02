import boto3

# first region details
region_1 = 'us-west-1'
key_1 = 'environment'
value_1 = 'prod'

# second region details
region_2 = 'us-west-2'
key_2 = 'environment'
value_2 = 'dev'

ec2_client_1 = boto3.client('ec2', region_name=region_1)
ec2_client_2 = boto3.client('ec2', region_name=region_2)

instance_ids_1 = []
instance_ids_2 = []

# first region
first_reservations = ec2_client_1.describe_instances()['Reservations']
for reservation in first_reservations:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids_1.append(instance['InstanceId'])

response_1 = ec2_client_1.create_tags(
    Resources=instance_ids_1,
    Tags=[
        {
            'Key': key_1,
            'Value': value_1
        },
    ]
)

print(f'{region_1} Region Instance Tags Updated.')

# second region
second_reservations = ec2_client_2.describe_instances()['Reservations']
for reservation in second_reservations:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids_2.append(instance['InstanceId'])

response_2 = ec2_client_2.create_tags(
    Resources=instance_ids_2,
    Tags=[
        {
            'Key': key_2,
            'Value': value_2
        },
    ]
)

print(f'{region_2} Region Instance Tags Updated.')
