#!/usr/bin/env python
import boto3
import click

@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
def cli(profile):
    ec2 = boto3.Session(profile_name=profile).resource('ec2')
    sgs = ec2.security_groups.all()

    for sg in sgs:
        tag_name = sg.group_name
        if sg.tags is not None:
            for tag in sg.tags:
                if tag['Key'] == 'Name' and tag['Value'] != '':
                    tag_name = tag['Value']

        print 'id: %s, name: %s, vpc_id: %s' % (sg.id, tag_name, sg.vpc_id)

if __name__ == '__main__':
    cli()