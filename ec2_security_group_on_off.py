#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import urllib2
import boto.ec2
import boto.ec2.securitygroup


# Get ISP assigned ip address
url = 'http://ip4.me'
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
items = soup.find_all('font')


# Add/remove security perm
def get_security_group(region, group_id):
    conn = boto.ec2.connect_to_region(region)
    sg_groups = conn.get_all_security_groups()
    for sg in sg_groups:
        if sg.id == group_id:
            return sg

if items and len(items) == 2:
    ip_address = items[1].string

    argument = sys.argv[1]
    sg = get_security_group('us-east-1', 'sg-68ba4607')
    port = 3389
    cidr = ip_address + '/32'
    result = None
    action = None

    if (argument == 'on') or (argument == 'add'):
        action = 'adding'
        result = sg.authorize(ip_protocol='tcp', from_port=port, to_port=port, cidr_ip=cidr, dry_run=False)
    elif (argument == 'off') or (argument == 'remove'):
        action = 'removing'
        result = sg.revoke(ip_protocol='tcp', from_port=port, to_port=port, cidr_ip=cidr, dry_run=False)

    if result:
        print 'Success %s RDP rule for ip %s from/to security group %s' % (action, ip_address, sg.name)
    else:
        print 'Failed %s RDP rule for ip %s from/to security group %s' % (action, ip_address, sg.name)
else:
    print 'Cannot get ip address from ' + url
