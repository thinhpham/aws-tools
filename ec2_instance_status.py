#!/usr/bin/env python
import sys
from aws_util import Ec2Util

if len(sys.argv) == 1:
    print('Usage: %s (instance_id)' % sys.argv[0])
    sys.exit(1)

id_or_tag = sys.argv[1]
ec2 = Ec2Util()
instance = ec2.get_instance(id_or_tag)

tag_name = 'UNKNOWN'
if instance.tags is not None:
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            tag_name = tag['Value']

print('id:                  %s' % instance.id)
print('name:                %s' % tag_name)
print('image_id:            %s' % instance.image_id)
print('instance_id:         %s' % instance.instance_id)
print('instance_type:       %s' % instance.instance_type)
print('platform:            %s' % instance.platform)
print('private_dns_name:    %s' % instance.private_dns_name)
print('private_ip_address:  %s' % instance.private_ip_address)
print('public_dns_name:     %s' % instance.public_dns_name)
print('public_ip_address:   %s' % instance.public_ip_address)
print('security_groups:     %s' % instance.security_groups)
print('state:               %s' % instance.state)
print('state_reason:        %s' % instance.state_reason)
print('vpc:                 %s' % instance.vpc)
print('subnet:              %s' % instance.subnet)
