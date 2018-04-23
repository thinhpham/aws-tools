import boto3
from datetime import datetime

# IMPORTANT
# Make sure you create an IAM role with an inline policy using the 
# file ec2_lambda_snapshot_role.json before creating this function

def lambda_handler(event, context):
    # Get EC2 client
    ec2 = boto3.client('ec2')

    # Get current timestamp in UTC
    now = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    
    # Get list of regions
    regions = ec2.describe_regions().get('Regions', [])

    # Iterate over regions
    for region in regions:
        print "Checking region %s " % region['RegionName']
        reg=region['RegionName']

        # Connect to region
        ec2 = boto3.client('ec2', region_name=reg)
    
        # Get snapshot resource 
        ec2resource = boto3.resource('ec2', region_name=reg)

        # Get all in-use volumes in all regions  
        result = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['in-use']}])
        
        for volume in result['Volumes']:
            volume_id = volume['VolumeId']
            print "Backing up %s in %s" % (volume_id, volume['AvailabilityZone'])
        
            # Create snapshot
            result = ec2.create_snapshot(VolumeId=volume['VolumeId'], Description='Created by automated Lambda function')
            snapshot = ec2resource.Snapshot(result['SnapshotId'])
        
            # Find name tag for volume if it exists
            volumename = volume_id + '-' + now
            if 'Tags' in volume:
                for tags in volume['Tags']:
                    if tags["Key"] == 'Name':
                        volumename = tags["Value"] + '-' + now
        
            # Add volume name to snapshot for easier identification
            snapshot.create_tags(Tags=[{'Key': 'Name', 'Value': volumename}])
            snapshot.create_tags(Tags=[{'Key': 'Category','Value': 'LambdaAutomatedSnapshot'}])
