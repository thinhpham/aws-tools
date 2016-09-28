#!/usr/bin/env python
import sys
import boto3
import click

@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
def cli(profile):
    ec2 = boto3.Session(profile_name=profile).resource('ec2')

    for item in ec2.instances.all():
        tag_name = 'UNKNOWN'
        if item.tags is not None:
            for tag in item.tags:
                if tag['Key'] == 'Name':
                    tag_name = tag['Value']

        state_name = 'UNKNOWN'
        if item.state is not None:
            state_name = item.state['Name']

        print 'id: %s, state: %s, name: %s' % (item.id, state_name, tag_name)

if __name__ == '__main__':
    cli()
