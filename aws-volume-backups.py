import boto3
import schedule
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2', region_name='us-east-1')


def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            },
        ],
    )

    for volume in volumes['Volumes']:
        try:
            new_snapshot = ec2_client.create_snapshot(VolumeId=volume['VolumeId'])
            print('Success', new_snapshot)
        except ClientError as e:
            print('Error', e)


schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()
