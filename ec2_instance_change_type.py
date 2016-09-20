#!/usr/bin/env python
import sys
from aws_util import Ec2Util

if len(sys.argv) < 3:
    print('Usage: %s (instance_tag_or_id) (instance_type)' % sys.argv[0])
    sys.exit(1)

id_or_tag = sys.argv[1]
new_instance_type = sys.argv[2]

ec2 = Ec2Util()
instance = ec2.get_instance(id_or_tag)

if instance:
    old_instance_state = instance.state['Name']
    old_instance_type = instance.instance_type

    print('Current instance type is %s' % old_instance_type)
    if new_instance_type != instance.instance_type:
        ec2.change_instance_type(id_or_tag, new_instance_type)
        instance.reload()
    print('Instance type changed to %s successfully' % instance.instance_type)
else:
    print('Error. Cannot find instance')
