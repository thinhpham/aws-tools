#!/usr/bin/env python
import sys
from aws_util import Ec2Util

if len(sys.argv) == 1:
    print('Usage: %s (instance_id)' % sys.argv[0])
    sys.exit(1)

id_or_tag = sys.argv[1]
ec2 = Ec2Util()
instance = ec2.get_instance(id_or_tag)

if instance.state['Name'] == 'running':
    instance.stop()
    instance.wait_until_stopped()
    print('Instance stopped succesfully')
elif instance.state['Name'] == 'stopped':
    print('Instance is already stopped')
else:
    print('Instance is in an unknown state: %s' % instance.state['Name'])
