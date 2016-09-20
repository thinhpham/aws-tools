# aws-tools
Collection of Python scripts to manage Amazon AWS

## Installation
    ```bash
        git clone https://github.com/thinhpham/aws-tools.git
        cd aws-tools
        pip install -r requirements.txt
    ```

## Usage
* It's pretty self-explanatory what each script does. Run the script without parameter to get the usage
* Several of the scripts also accept a profile name if provided as a second parameter. They'll use the [default] profile if nothing is supplied. For example:
    ```bash
        python ec2_instance_list.py
        python ec2_instance_list.py dev
        python ec2_instance_list.py prod
    ```

## Notes
* Requires Python
* Make sure you've configured the "config" and "credentials" files before using these scripts. Check for the existence of the ".aws" folder if you're not sure
* The ".aws" folder can be created either manually or by using "aws configure". It can be located in the following locations
    * On Linux/Mac: ~/.aws
    * On Windows: %USERPROFILE%\\.aws (Normally C:\\Users\\USERNAME\\.aws)
* "aws configure" requires the [AWS Command Line Interface](https://aws.amazon.com/cli)
* Below is an example of both the "config" and "credentials" files if you want to create them manually
    * ~/.aws/config
        ```ini
        [default]
        output = json
        region = us-east-1
        
        [profile dev]
        output = xml
        region = us-east-2
        
        [profile prod]
        output = json
        region = us-east-1
        ```
        
    * ~/.aws/credentials
        ```ini
        [default]
        aws_access_key_id = AWS_ACCESS_KEY_ID
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY

        [dev]
        aws_access_key_id = AWS_ACCESS_KEY_ID
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY

        [prod]
        aws_access_key_id = AWS_ACCESS_KEY_ID
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        ```
        