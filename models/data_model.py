from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['localhost'])  # Replace 'localhost' with your Cassandra cluster's contact points
session = cluster.connect()

# Create a keyspace
session.execute("CREATE KEYSPACE IF NOT EXISTS task_manager WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")

# Use the keyspace
session.set_keyspace('task_manager')

# Create a table for tasks
session.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id UUID PRIMARY KEY,
        title TEXT,
        description TEXT,
        status TEXT,
        due_date TIMESTAMP,
        assigned_user TEXT
    )
""")
                
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        username TEXT,
        password TEXT,
        email TEXT,
        additional_info TEXT
    )
""")
                
# Close the session and cluster when done
session.shutdown()
cluster.shutdown()
