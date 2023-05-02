import boto3
import schedule

eks_client = boto3.client('eks', region_name='us-east-1')


def check_eks_cluster_status():
    eks_clusters = eks_client.list_clusters()['clusters']
    for cluster in eks_clusters:
        response = eks_client.describe_cluster(name=cluster)

        cluster_info = response['cluster']
        cluster_status = cluster_info['status']
        cluster_endpoint = cluster_info['endpoint']
        cluster_version = cluster_info['version']

        print(f"Cluster {cluster} status is {cluster_status}")
        print(f"Cluster endpoint: {cluster_endpoint}")
        print(f"Cluster version: {cluster_version}")
        print('---------------------------------------------------------------------------')


schedule.every(5).hours.do(check_eks_cluster_status)

while True:
    schedule.run_pending()
