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
            instance.reboot()
            instance.wait_until_running()
            print('Instance reboot successfully')
        else:
            print('Cannot find instance. Did you select a correct profile?')
    else:
        sys.exit(1)

if __name__ == '__main__':
    cli()