#!/usr/bin/env python
import sys
import boto3

s3 = None
if len(sys.argv) <= 1:
    s3 = boto3.resource('s3')
else:
    session = boto3.Session(profile_name=sys.argv[1])
    s3 = session.resource('s3')

for i in s3.buckets.all():
    print('name: %s' % i.name)
