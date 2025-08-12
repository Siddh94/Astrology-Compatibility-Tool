import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET, REGION

def upload_to_s3(file_path, s3_key):
    """Upload file to AWS S3 bucket."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION
    )
    s3.upload_file(file_path, S3_BUCKET, s3_key)
    print(f"✅ Uploaded {file_path} to s3://{S3_BUCKET}/{s3_key}")
