import boto3

ec2 = boto3.client('ec2')
regions = ec2.describe_regions()['Regions']

for item in regions:
    print('name: %s, endpoint: %s' % (item['RegionName'], item['Endpoint']))