#!/usr/bin/env python
import sys
import boto3
import click

@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
def cli(profile):
    s3 = boto3.Session(profile_name=profile).resource('s3')

    for item in s3.buckets.all():
        print('name: %s' % item.name)

if __name__ == '__main__':
    cli()
