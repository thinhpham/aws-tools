#!/usr/bin/env python
import sys
import boto3

s3 = boto3.resource('s3')
if len(sys.argv) > 1:
    s3 = boto3.Session(profile_name=sys.argv[1]).resource('s3')

for item in s3.buckets.all():
    print('name: %s' % item.name)
