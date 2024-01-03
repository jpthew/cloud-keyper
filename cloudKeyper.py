import db.aws as awsdb
import boto3
import json
import os
import sys
import time
from prompt_toolkit import PromptSession
import prompt_toolkit
from prettytable import PrettyTable

print('''
     _             _ _  __                       
  __| |___ _  _ __| | |/ /___ _  _ _ __  ___ _ _ 
 / _| / _ \ || / _` | ' </ -_) || | '_ \/ -_) '_|
 \__|_\___/\_,_\__,_|_|\_\___|\_, | .__/\___|_|  
                              |__/|_|            
    by @jpthew
''')

# Create a PromptSession object
session = PromptSession()

# Define a function to handle user input
def handle_input(text):
    # Check if the user wants to exit
    if text.lower() == "exit":
        sys.exit()  # Exit the program
    if text.lower() == "help":
        help_page()
    if text.lower() == "list":
        get_aws_keys_table()
    if text.lower() == "import-aws":
        import_aws_key()

def get_aws_keys_table():
    # run awsdb.get_aws_all_key_names() to get all key names and format in a ui table
    keys = awsdb.get_aws_all_key_names()
    columns = ['KEY_NAME']
    table = PrettyTable(columns)
    table.field_names = columns
    for key in keys:
        table.add_row(key)
    print(table)
    

def help_page():
    print('''
    help - Display this help page
    list - List all AWS key names
    import-aws - Manually import AWS key
    exit - Exit the program
    ''')
    
def import_aws_key():    
    try:
        print('''
        Enter memorably AWS key name (e.g. [AKIA] jpthew, [ASIA] ec2-dev1-sts, etc...): 
        ''')
        key_name = input('KEY NAME> ')
        print('''
        Enter AWS access key ID: 
        ''')
        if awsdb.check_duplicate_key_name(key_name) == True:
            print('''
            Key name already exists! Please choose a different key name and try again.
            If you want to update the key, please use the update command.
            If you want to refresh the key, please use the refresh command.
            ''')
            return
        aws_access_key_id = input('AccessKeyId > ')
        print('''
        Enter AWS secret access key: 
        ''')
        aws_secret_access_key = input('SecretAccessKey > ')
        print('''
        Enter AWS session token (optional): 
        ''')
        aws_session_token = input('SessionToken > ')

        if validate_aws_key(aws_access_key_id, aws_secret_access_key, aws_session_token) == True:
            print('''
        Key validated successfully!
        ''')
        else:
            print('''
            Key validation failed! Please check your key and try again.
                ''')
            return
        
        print('''
        Enter AWS region: 
        ''')
        aws_region = input('> ')

        if aws_session_token == '':
            remote_server = 'NULL'
            hops = 'NULL'
        else:
            print('''
            Enter IP for remote server to renew key via IMDS:
                ''')
            remote_server = input('> ')
            print('''
            How many ssh hops to remote server? (1 for direct ssh, 2 or more for chained ssh connections): 
            ''')
            hops = input('> ')
        expiration = get_aws_key_expiration(aws_access_key_id, aws_secret_access_key, aws_session_token)
        account_id = get_aws_account_id(aws_access_key_id, aws_secret_access_key, aws_session_token)
        account_user = get_aws_account_user(aws_access_key_id, aws_secret_access_key, aws_session_token)
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        stale = 'FALSE'
        key_id = awsdb.get_aws_next_key_id()
        print('key_id: ' + str(key_id) + '\nkey_name: ' + key_name + '\naws_access_key_id: ' + aws_access_key_id + '\naws_secret_access_key: ' + aws_secret_access_key + '\naws_session_token: ' + aws_session_token + '\naws_region: ' + aws_region + '\naccount_id: ' + account_id + '\naccount_user: ' + account_user + '\ndatetime: ' + datetime + '\nexpiration: ' + str(expiration) + '\nremote_server: ' + remote_server + '\nhops: ' + hops + '\nstale: ' + stale)
        awsdb.insert_aws_credentials(key_id, key_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region, account_id, account_user, datetime, expiration, remote_server, hops, stale)
    except KeyboardInterrupt:
        print()
        return

def validate_aws_key(aws_access_key_id, aws_secret_access_key, aws_session_token):
    if aws_session_token == '':
        try:
            sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            sts_client.get_caller_identity()
            return True
        except:
            return False
    else:
        try:
            sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
            sts_client.get_caller_identity()
            return True
        except:
            return False

def get_aws_key_expiration(aws_access_key_id, aws_secret_access_key, aws_session_token):
    try:
        sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        expiration = sts_client.get_caller_identity()['Credentials']['Expiration']
        return expiration
    except:
        return 'NULL'
    
def get_aws_account_id(aws_access_key_id, aws_secret_access_key, aws_session_token):
    try:
        sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        account_id = sts_client.get_caller_identity()['Account']
        return account_id
    except:
        return 'NULL'

def get_aws_account_user(aws_access_key_id, aws_secret_access_key, aws_session_token):
    try:
        sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        account_user = sts_client.get_caller_identity()['Arn']
        return account_user
    except:
        return 'NULL'

#########################################
# Main loop for the shell interface
while True:
    try:
        # Read user input
        text = session.prompt("MENU > ")

        # Handle user input
        handle_input(text)

    except KeyboardInterrupt:
        # Handle Ctrl+C
        print("Exiting...")
        break