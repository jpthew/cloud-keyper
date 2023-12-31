import sqlite3

def create_aws_credentials_table():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect('keys.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aws_credentials (
            key_id INTEGER PRIMARY KEY,
            key_name TEXT,
            aws_access_key_id TEXT,
            aws_secret_access_key TEXT,
            aws_session_token TEXT,
            aws_region TEXT,
            account_id TEXT,
            account_user TEXT,
            datetime TEXT,
            expiration TEXT,
            remote_server TEXT,
            hops TEXT,
            stale TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def connect_to_db():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect('keys.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    return conn, cursor

def check_duplicate_key_name(key_name):
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Get the data from the table
    cursor.execute('SELECT key_name FROM aws_credentials WHERE key_name = ?', (key_name,))

    # Fetch the data
    if cursor.fetchone() is None:
        duplicate_key_name = False
    else:
        duplicate_key_name = True

    # Close the connection
    conn.close()

    return duplicate_key_name

def insert_aws_credentials(key_id, key_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region, account_id, account_user, datetime, expiration, remote_server, hops, stale):
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Insert the data into the table
    cursor.execute('''
        INSERT INTO aws_credentials (
            key_id,
            key_name,
            aws_access_key_id,
            aws_secret_access_key,
            aws_session_token,
            aws_region,
            account_id,
            account_user,
            datetime,
            expiration,
            remote_server,
            hops,
            stale
        ) VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?
        )
    ''', (key_id, key_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region, account_id, account_user, datetime, expiration, remote_server, hops, stale))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def update_aws_credentials(key_id, key_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region, account_id, account_user, datetime, expiration, remote_server, hops, stale):
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Update the data in the table
    cursor.execute('''
        UPDATE aws_credentials SET
            key_id = ?,
            key_name = ?,
            aws_access_key_id = ?,
            aws_secret_access_key = ?,
            aws_session_token = ?,
            aws_region = ?,
            account_id = ?,
            account_user = ?,
            datetime = ?,
            expiration = ?,
            remote_server = ?,
            hops = ?,
            stale = ?
        WHERE key_id = ?
    ''', (key_id, key_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region, account_id, account_user, datetime, expiration, remote_server, hops, stale))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_aws_next_key_id():
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Get the data from the table
    cursor.execute('SELECT MAX(key_id) FROM aws_credentials')

    # Fetch the data
    key_id = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    if key_id is None:
        return 1
    else:
        return key_id + 1

def get_aws_credentials(key_id):
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Get the data from the table
    cursor.execute('SELECT aws_access_key_id, aws_secret_access_key, aws_session_token FROM aws_credentials WHERE key_name = ?', (key_id,))

    # Fetch the data
    aws_credentials = cursor.fetchone()

    # Close the connection
    conn.close()

    return aws_credentials
    
def get_aws_all_key_names():
    # Connect to the database or create it if it doesn't exist
    conn, cursor = connect_to_db()

    # Get the data from the table
    cursor.execute('SELECT key_name FROM aws_credentials ORDER BY key_id ASC')

    # Fetch the data
    if cursor.fetchone() is None:
        key_names = 'No keys found'
    else:
        key_names = cursor.fetchall()

    # Close the connection
    conn.close()

    return key_names

create_aws_credentials_table()