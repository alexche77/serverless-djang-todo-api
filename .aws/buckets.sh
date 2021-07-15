#!/bin/bash
set -x
awslocal  --endpoint-url=http://localstack:4566 s3 mb s3://bucket 
set +x