#!/usr/bin/env python
import boto3

print 'Security group information:\n'

ec2 = boto3.resource('ec2')
sgs = ec2.security_groups.all()

for sg in sgs:
    tag_name = sg.group_name
    if sg.tags is not None:
        for tag in sg.tags:
            if tag['Key'] == 'Name' and tag['Value'] != '':
                tag_name = tag['Value']

    print 'id: %s, name: %s, vpc_id: %s' % (sg.id, tag_name, sg.vpc_id)