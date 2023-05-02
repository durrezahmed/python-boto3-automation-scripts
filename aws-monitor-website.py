import os
import time
import smtplib
import paramiko
import schedule
import requests
import boto3
from botocore.exceptions import ClientError

# constants
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECEIVER_ADDRESS = os.environ.get('RECEIVER_ADDRESS')

HOSTNAME = os.environ.get('HOSTNAME')
HOST_URL = os.environ.get('HOST_URL')
HOST_USERNAME = os.environ.get('HOST_USERNAME')
HOST_PASSWORD = os.environ.get('HOST_PASSWORD')

ec2_client = boto3.client('ec2', region_name='us-east-1')
INSTANCE_ID = 'i-0a9ce5ad2782e8f22'


def send_email(email_message):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        msg = f'Subject: SITE DOWN\n{email_message}.'
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, RECEIVER_ADDRESS, msg)
    print('Email Sent.')


def restart_container():
    print('Restarting the application...')
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=HOSTNAME, username=HOST_USERNAME, password=HOST_PASSWORD)

    _stdin, _stdout, _stderr = ssh_client.exec_command('docker restart charming_robinson')
    time.sleep(5)

    print(_stdout.readlines())
    ssh_client.close()
    print('Application Restarted.')


def restart_server_and_app():
    # Reboot the ec2 instance
    try:
        response = ec2_client.reboot_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)

    print('Server Restarted.')

    # restart the application
    while True:
        instance_status = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]
        if instance_status['State']['Name'] == 'running':
            time.sleep(10)
            restart_container()
            break


def monitor_application():
    try:
        response = requests.get(HOST_URL)
        if response.status_code == 200:
            print('Website is running Successfully.')
        else:
            print('Website is Down, Fix it!')
            message = f'Application returned {response.status_code}.'
            send_email(message)
            restart_container()

    except Exception as ex:
        print(f'Connection Error happened {ex}.')
        message = 'Application not accessible at all.'
        send_email(message)
        restart_server_and_app()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()
