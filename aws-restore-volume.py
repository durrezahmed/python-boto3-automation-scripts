import boto3
from operator import itemgetter

# we have to assume that the instance has only one volume attached to it

ec2_client = boto3.client('ec2', region_name='us-east-1')
instance_id = 'i-0ac3319fc0jkl65464nj9'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        },
    ]
)

instance_volume = volumes['Volumes'][0]
print(instance_volume)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        },
    ],
)

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone='us-east-1a',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                },
            ]
        },
    ],
)

while True:
    new_volume_status = ec2_client.describe_volumes(
        VolumeIds=[new_volume['VolumeId']],
        DryRun=False,
    )

    new_volume_state = new_volume_status['Volumes'][0]['State']

    if new_volume_state == 'available':
        volume_attachment = ec2_client.attach_volume(
            Device='/dev/xvdb',
            InstanceId=instance_id,
            VolumeId=new_volume['VolumeId'],
            DryRun=False
        )
        break
