#!/usr/bin/env python
import boto3

s3 = boto3.resource('s3')

for i in s3.buckets.all():
    print('name: %s' % i.name)
