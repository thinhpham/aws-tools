#!/usr/bin/env python
import sys
import click
from aws_util import Ec2Util

@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
@click.argument('id_or_tag', required=True)
@click.argument('new_instance_type', required=True)
def cli(profile, id_or_tag, new_instance_type):
    ec2 = Ec2Util(profile)
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

if __name__ == '__main__':
    cli()