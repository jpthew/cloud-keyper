import random
import string
import uuid

def generate_fake_aws_credentials(num_credentials):
    credentials = []
    for _ in range(num_credentials):
        access_key = str(uuid.uuid4()).replace("-", "")
        secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        session_token = str(uuid.uuid4()).replace("-", "")
        credentials.append({"AccessKey": access_key, "SecretKey": secret_key, "SessionToken": session_token})
    return credentials

num_credentials = 5
fake_credentials = generate_fake_aws_credentials(num_credentials)

for credential in fake_credentials:
    print(credential)

