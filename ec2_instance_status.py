#!/usr/bin/env python
import sys
import click
from aws_util import Ec2Util

@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
@click.argument('id_or_tag', required=True)
def cli(profile, id_or_tag):
    if id_or_tag is not None:
        ec2 = Ec2Util(profile)
        instance = ec2.get_instance(id_or_tag)

        if instance:
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
        else:
            print('Cannot find instance. Did you select a correct profile?')
    else:
        sys.exit(1)

if __name__ == '__main__':
    cli()