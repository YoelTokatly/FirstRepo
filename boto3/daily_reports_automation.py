
def main():
        import boto3 as boto3
        import os as os
        import zipfile as zipfile
        import botocore as botocore
        

        print ("Hello, lets start!")
        #start a session
        session = boto3.Session(profile_name='default',region_name='us-west-2')
        s3_client = session.client('s3')
        bucket_name = 'daily-reports-035-06-2025'
        local_path = './test_folder/'
        zip_file = './dayly_zip/archive.zip'

        # return bucket_name 
        bucket_exists(s3_client,bucket_name,session)
        folder_exists (s3_client,bucket_name)
        create_zip_file(s3_client,bucket_name,zip_file,local_path) # upload the zip file to s3


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
    folder_name = 'daily-reports-05-06-2025/'
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

def create_zip_file(s3_client,bucket_name,zip_file,local_path):
    # getting the list of files to zip
    import os
    import zipfile
    files_to_zip = []
    for _, _, files in os.walk(local_path):
        for file in files:
            files_to_zip.append(local_path+file)
    # Create a zip file and add files to it
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))
            else:
                print(f"Warning: {file} not found or not a file")
    print (f'Files in local path {local_path}: {files_to_zip}')  
    #upload the zip file to s3
    s3_client.upload_file(zip_file, bucket_name, local_path + os.path.basename(zip_file))
    print(f"Uploaded {zip_file} to s3://{bucket_name}/{local_path}{os.path.basename(zip_file)}")


main()

