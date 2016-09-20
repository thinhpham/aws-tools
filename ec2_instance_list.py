#!/usr/bin/env python
import boto3

ec2 = boto3.resource('ec2')

for i in ec2.instances.all():
    tag_name = 'UNKNOWN'
    if i.tags is not None:
        for tag in i.tags:
            if tag['Key'] == 'Name':
                tag_name = tag['Value']

    state_name = 'UNKNOWN'
    if i.state is not None:
        state_name = i.state['Name']

    print 'id: %s, state: %s, name: %s' % (i.id, state_name, tag_name)
