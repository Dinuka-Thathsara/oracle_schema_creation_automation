import cx_Oracle

# Oracle connection details
oracle_dsn = cx_Oracle.makedsn("", 1521, service_name="") #set the host ip
oracle_user = ""
oracle_password = ""

# Function to create a user in Oracle
def create_oracle_user(cursor, username):
    password = f"{username}78903"
    try:
        # Check if the user already exists
        cursor.execute(f"SELECT COUNT(*) FROM dba_users WHERE username = UPPER('{username}')")
        user_exists = cursor.fetchone()[0]
        
        if user_exists:
            print(f"User {username} already exists.")
        else:
            # Create the user and grant privileges
            cursor.execute(f"CREATE USER {username} IDENTIFIED BY {password}")
            cursor.execute(f"GRANT CONNECT, RESOURCE TO {username}")
            print(f"User {username} created successfully.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Error creating user {username}: {error.message}")

# Read PostgreSQL databases from a file
def read_postgresql_databases(file_path):
    with open(file_path, 'r') as file:
        databases = [line.strip() for line in file if line.strip()]
        print(f"Databases to create users for: {databases}")
    return databases

# Main function
def main():
    # Path to the file containing PostgreSQL databases
    file_path = "db_data.txt"
    
    # Read PostgreSQL databases
    databases = read_postgresql_databases(file_path)
    
    # Connect to Oracle
    connection = cx_Oracle.connect(oracle_user, oracle_password, dsn=oracle_dsn)
    cursor = connection.cursor()
    
    # Create users in Oracle
    for db in databases:
        create_oracle_user(cursor, db)
    
    # Commit the transaction
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
