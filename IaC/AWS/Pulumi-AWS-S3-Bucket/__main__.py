"""An AWS Python Pulumi program to create an S3 bucket"""

import pulumi
from pulumi_aws import s3
import pulumi_aws as aws


bucket_name = 'journeytothewest'
# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket(bucket_name,
                   )

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
