#!/usr/bin/env python
import boto

print 'Security group information:\n'

ec2 = boto.connect_ec2()
sgs = ec2.get_all_security_groups()

for sg in sgs:
    instances = sg.instances()
    print 'id: %s, name: %s, count: %s' % (sg.id, sg.name, len(instances))

    for inst in instances:
        tag_name = 'UNKNOWN'
        if inst.tags is not None and 'Name' in inst.tags:
            tag_name = inst.tags['Name']
        print '\tid: %s, name: %s' % (inst.id, tag_name)
