import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='us-east-1')


def check_instance_status():
    statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)
    for status in statuses['InstanceStatuses']:
        ins_status_1 = status['InstanceState']['Name']
        ins_status_2 = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        print(
            f"Instance ({status['InstanceId']}) is {ins_status_1} status is {ins_status_2} and system status is {sys_status}.")
    print(
        '-------------------------------------------------------------------------------------------------------------')


schedule.every(10).seconds.do(check_instance_status)

while True:
    schedule.run_pending()
