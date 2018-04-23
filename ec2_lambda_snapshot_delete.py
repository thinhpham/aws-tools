import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# IMPORTANT
# Make sure you create an IAM role with an inline policy using the 
# file ec2_lambda_snapshot_role.json before creating this function

def delete_snapshot(snapshot_id, reg):
    print "Deleting snapshot %s " % (snapshot_id)
    try:  
        ec2resource = boto3.resource('ec2', region_name=reg)
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        print "Caught exception: %s" % e

    
def lambda_handler(event, context):
    # TODO: AWS Account ID    
    account_id = 'XXXXXXXXXXXX'
    
    # TODO: Define retention period in days
    retention_days = 30
    
    # TODO: Get list of regions
    regions = ['us-east-1', 'us-east-2']

    # Get current timestamp in UTC
    now = datetime.utcnow()

    # Create EC2 client
    ec2 = boto3.client('ec2')
    
    # Iterate over regions
    for region in regions:
        print "Checking for snapshots in region %s " % region
        
        # Connect to region
        ec2 = boto3.client('ec2', region_name=region)
        
        # Filtering by snapshot timestamp comparison is not supported
        # So we grab all snapshot id's
        result = ec2.describe_snapshots(OwnerIds=[account_id])
    
        for snapshot in result['Snapshots']:
            print "Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'], snapshot['StartTime'])
       
            # Remove timezone info from snapshot in order for comparison to work below
            snapshot_time = snapshot['StartTime'].replace(tzinfo=None)

            # Find automated snapshots
            snapshot_tags = snapshot['Tags']
            automated_snapshot = False
            for tag in snapshot_tags:
                if tag['Key'] == 'Category' and tag['Value'] == 'LambdaAutomatedSnapshot':
                    automated_snapshot = True
        
            # Only delete if snapshot was an automated snapshot
            if automated_snapshot:
                # Subtract snapshot time from now returns a timedelta 
                # Check if the timedelta is greater than retention days
                if (now - snapshot_time) > timedelta(retention_days):
                    print "Snapshot is older than configured retention of %d days" % (retention_days)
                    delete_snapshot(snapshot['SnapshotId'], region)
                else:
                    print "Snapshot is newer than configured retention of %d days so we keep it" % (retention_days)          
            else:
                print "Snapshot is not an automated snapshot so we keep it"
