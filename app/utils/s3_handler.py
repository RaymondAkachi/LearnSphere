import boto3

s3 = boto3.client('s3')


def download_from_s3(s3_key, local_path):
    bucket_name = "your-s3-bucket-name"  # Replace with your S3 bucket
    s3.download_file(bucket_name, s3_key, local_path)
