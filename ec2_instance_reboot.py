#!/usr/bin/env python
import sys
from aws_util import Ec2Util

if len(sys.argv) == 1:
    print('Usage: %s (instance_id)' % sys.argv[0])
    sys.exit(1)

id_or_tag = sys.argv[1]
ec2 = Ec2Util()
instance = ec2.get_instance(id_or_tag)
instance.reboot()
instance.wait_until_running()
print('Instance rebooted sucessfully')
