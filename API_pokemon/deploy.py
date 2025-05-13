import boto3

#tell boto3 to use the default profile
session = boto3.Session(profile_name='default',region_name='us-west-2')
#tell boto3 to use the default region
ec2 = session.resource('ec2')

import boto3
import time

def create_ec2_with_game_dependencies():
    # Initialize boto3 EC2 client
    ec2 = boto3.resource('ec2', region_name='us-east-1')  # Change region as needed
    
    # Bash script to install dependencies and setup your Python game
    user_data_script = """#!/bin/bash
    # Update package lists
    apt-get update -y
    
    # Install Python and pip
    apt-get install -y python3 python3-pip
    
    # Install system dependencies that might be needed for your game
    apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    
    # Create a directory for your game
    mkdir -p /opt/API_POKEMON
    
    # Install Python game dependencies
    pip3 install pygame numpy pandas sqlite3 requests random json
    
    # You could also clone your game from a repository
    # git clone https://github.com/yourusername/your-game-repo.git /opt/python-game
    
    # Or you could download your game files from S3
    # aws s3 cp s3://your-bucket/your-game.zip /opt/python-game/
    # cd /opt/python-game && unzip your-game.zip
    
    # Set up any environment variables
    echo 'export GAME_HOME=/opt/python-game' >> /etc/environment
    
    # Optional: Set the game to run on startup
    echo "@reboot python3 /opt/python-game/main.py" | crontab -
    
    # Log the completion of the setup
    echo "Game setup completed at $(date)" > /opt/python-game/setup_complete.log
    """
    
    # Create the EC2 instance
    instances = ec2.create_instances(
        ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2 AMI (change to your preferred AMI)
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',  
        KeyName='vockey',  
        SecurityGroupIds=['sg-05ec148a2b76e68b9'],  
        UserData=user_data_script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'PythonGameServer'
                    },
                ]
            },
        ],
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 8,  # Size in GB
                    'VolumeType': 'gp2',
                    'DeleteOnTermination': True
                }
            },
        ]
    )
    
    instance = instances[0]
    print(f"Waiting for instance {instance.id} to be running...")
    instance.wait_until_running()
    
    # Reload the instance to get the updated public IP
    instance.reload()
    
    print(f"Instance {instance.id} is now running")
    print(f"Public IP: {instance.public_ip_address}")
    print(f"Public DNS: {instance.public_dns_name}")
    
    return instance

if __name__ == "__main__":
    instance = create_ec2_with_game_dependencies()
    print("EC2 instance for Python game created successfully!")
    print("Note: The user-data script is still running in background.")
    print("You can SSH into the instance once it completes setup.")
