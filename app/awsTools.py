import boto3

#인스턴스 정보 조회
def getInstance():

    ec2 = boto3.client('ec2')

    # 인스턴스 목록 조회
    response = ec2.describe_instances()

    # 인스턴스 정보 추출
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_info = {
                'InstanceID': instance.get('InstanceId'),
                'InstanceType': instance.get('InstanceType'),
                'State': instance['State'].get('Name'),
                'InstanceName': next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'empty'),
                'PrivateIP': instance.get('PrivateIpAddress'),
                'PublicIP': instance.get('PublicIpAddress', 'No Public'),
                'InstanceVPC': instance.get('VpcId')
            }
            instances.append(instance_info)

    return instances

#VPC ID와 VPC NAME 맵핑을 위한 데이터 추출
def getVpc():
    vpcs = {}
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()

    for vpc in response['Vpcs']:
        vpcs[vpc.get('VpcId')] = next((tag['Value'] for tag in vpc.get('Tags', []) if tag['Key'] == 'Name'), 'no_name_vpc')

    return vpcs