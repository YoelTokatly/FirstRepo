import boto3
import pandas as pd
import os
import zipfile



def main():
    print("hello")
    session = boto3.Session(profile_name='default',region_name='us-west-2')
    ec2_client = session.client('ec2')
    s3_client = session.client('s3')
    choose_operation = int(input('what do you whant to do? 1.create bucket. 2. create folder. 3.upload files'))
    if choose_operation == 1:
        bucket_name =  input("give the bucket name or 'X' to continue").lower()
        if bucket_name not in 'x':
            print(f'Trying to create {bucket_name} bucket')
            bucket_exists(s3_client,bucket_name,session)
    elif choose_operation == 2:
        folder_exists(s3_client,bucket_name)
    elif choose_operation == 3:
        bucket_name = 'dst-sales-1235'
        upload_files(s3_client,bucket_name)     


def bucket_exists(s3_client,bucket_name,session):
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
        # print(f"Available buckets:{buckets}")
        # return bucket_name in buckets

        if bucket_name in buckets:
            # bucket exists
            print(f'Bucket {bucket_name} exists.')
        else:
            s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': session.region_name
            }    
            )
            print(f'Bucket {bucket_name} created in {session.region_name} region')


def folder_exists (s3_client,bucket_name):
    #  check if folder exists
    folder_name = 'dcustomer-details/'
    folders_in_bucket = []
    files_in_bucket = []
    objects_in_bucket =  []

    response = s3_client.list_objects_v2( Bucket=bucket_name , Prefix=folder_name)

    if 'Contents' in response:
        print(f"Folder '{folder_name}' already exists ")
    # Create 'folder' (empty object with the folder name as key)
    else:
        s3_client.put_object(
                    Bucket=bucket_name,
                    Key=folder_name,
                    Body=''
                )
        print(f"Created folder '{folder_name}' in bucket '{bucket_name}'")

def upload_files(s3_client,bucket_name):
    local_path = './test_folder/'
    files_to_upload= ['dr1.csv','dr2.csv','dr3.csv']
    for files in files_to_upload:
        for file in files_to_upload:
            files_to_upload.append(local_path+file)
    print (f'Files in local path {files_to_upload}')  



    # # files = [os.path.basename(local_path)]
    # s3_client.upload_file(files_to_upload, bucket_name, files_to_upload)
    # print(f"Uploaded {files_to_upload} to s3://{bucket_name}/{files_to_upload}")


if __name__ == "__main__":
    main()