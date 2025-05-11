import boto3
import json
import time
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Configuration
BUCKET1_NAME = 'my-first-bucket-' + str(int(time.time()))
BUCKET2_NAME = 'my-second-bucket-' + str(int(time.time()))
EMAIL_ADDRESS = 'your-email@example.com'  # Replace with your email
REGION = 'us-east-1'  # Replace with your preferred region

def create_buckets():
    """Create two S3 buckets"""
    buckets = [BUCKET1_NAME, BUCKET2_NAME]
    created_buckets = []
    
    for bucket_name in buckets:
        try:
            if REGION == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': REGION}
                )
            print(f"Successfully created bucket: {bucket_name}")
            created_buckets.append(bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"Bucket {bucket_name} already exists")
            else:
                print(f"Error creating bucket {bucket_name}: {e}")
    
    return created_buckets

def create_sns_topic():
    """Create SNS topic and subscribe email"""
    topic_name = 'FileMovementNotification'
    
    try:
        # Create SNS topic
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"Created SNS topic: {topic_arn}")
        
        # Subscribe email to topic
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=EMAIL_ADDRESS
        )
        print(f"Subscribed {EMAIL_ADDRESS} to SNS topic (check your email to confirm)")
        
        return topic_arn
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")
        return None

def create_sample_files():
    """Create sample files with prefixes sr1_, sr2_, sr3_"""
    files = [
        'sr1_customer_data.txt',
        'sr1_report.csv',
        'sr1_analysis.json',
        'sr2_customer_info.txt',
        'sr2_transactions.csv',
        'sr3_customer_feedback.txt',
        'sr3_sales_data.csv'
    ]
    
    for file_name in files:
        with open(file_name, 'w') as f:
            f.write(f"Sample content for {file_name}")
        print(f"Created sample file: {file_name}")
    
    return files

def upload_files_to_bucket(bucket_name, files, folder_name='customer-details'):
    """Upload files to specified bucket and folder"""
    uploaded_files = []
    
    for file_name in files:
        try:
            s3_key = f"{folder_name}/{file_name}"
            s3_client.upload_file(file_name, bucket_name, s3_key)
            print(f"Uploaded {file_name} to {bucket_name}/{s3_key}")
            uploaded_files.append(s3_key)
        except ClientError as e:
            print(f"Error uploading {file_name}: {e}")
    
    return uploaded_files

def list_and_move_sr1_files(bucket_name, source_folder='customer-details', dest_folder='sr1'):
    """List files with sr1_ prefix and move them to sr1/ folder"""
    moved_files = []
    
    try:
        # List objects with sr1_ prefix
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=f"{source_folder}/sr1_"
        )
        
        if 'Contents' not in response:
            print("No files with sr1_ prefix found")
            return moved_files
        
        print(f"\nFound {len(response['Contents'])} files with sr1_ prefix:")
        
        for obj in response['Contents']:
            source_key = obj['Key']
            file_name = source_key.split('/')[-1]
            dest_key = f"{dest_folder}/{file_name}"
            
            print(f"\nMoving {source_key} to {dest_key}")
            
            try:
                # Copy object to new location
                s3_client.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': source_key},
                    Key=dest_key
                )
                
                # Delete original object
                s3_client.delete_object(Bucket=bucket_name, Key=source_key)
                
                print(f"Successfully moved {file_name} from {source_folder}/ to {dest_folder}/")
                print(f"Deleted original file from {source_folder}/ folder")
                
                moved_files.append(file_name)
                
            except ClientError as e:
                print(f"Error moving {source_key}: {e}")
        
        if moved_files:
            print(f"\n{len(moved_files)} files have been moved to {dest_folder}/ folder and deleted from {source_folder}/ folder")
        
    except ClientError as e:
        print(f"Error listing objects: {e}")
    
    return moved_files

def send_sns_notification(topic_arn, moved_files, bucket_name):
    """Send SNS notification about moved files"""
    if not moved_files:
        return
    
    message = {
        'bucket': bucket_name,
        'moved_files': moved_files,
        'count': len(moved_files),
        'source_folder': 'customer-details',
        'destination_folder': 'sr1',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message, indent=2),
            Subject=f'File Movement Notification - {len(moved_files)} files moved'
        )
        print(f"\nSNS notification sent for {len(moved_files)} moved files")
    except ClientError as e:
        print(f"Error sending SNS notification: {e}")

def main():
    """Main function to execute all tasks"""
    print("=== Task 1: Creating buckets and SNS topic ===")
    created_buckets = create_buckets()
    topic_arn = create_sns_topic()
    
    print("\n=== Task 2: Creating and uploading files ===")
    files = create_sample_files()
    uploaded_files = upload_files_to_bucket(BUCKET1_NAME, files)
    
    print("\n=== Task 3: Moving sr1_ files ===")
    moved_files = list_and_move_sr1_files(BUCKET1_NAME)
    
    if moved_files and topic_arn:
        send_sns_notification(topic_arn, moved_files, BUCKET1_NAME)
    
    # Verify the move operation by listing both folders
    print("\n=== Verification: Listing files in both folders ===")
    
    print("\nFiles in customer-details/ folder:")
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET1_NAME,
            Prefix="customer-details/"
        )
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"  - {obj['Key']}")
        else:
            print("  No files found")
    except ClientError as e:
        print(f"  Error listing files: {e}")
    
    print("\nFiles in sr1/ folder:")
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET1_NAME,
            Prefix="sr1/"
        )
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"  - {obj['Key']}")
        else:
            print("  No files found")
    except ClientError as e:
        print(f"  Error listing files: {e}")

if __name__ == "__main__":
    # Make sure to replace EMAIL_ADDRESS with your actual email
    if EMAIL_ADDRESS == 'your-email@example.com':
        print("Please update EMAIL_ADDRESS with your actual email address")
    else:
        main()