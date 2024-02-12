import glob
import json
import os
from typing import List

from cassandra.cluster import Cluster


table_drop = "DROP TABLE IF EXISTS events"

table_create = """
    CREATE TABLE IF NOT EXISTS events
    (
        id text,
        type text,
        public boolean,
        PRIMARY KEY (
            id,
            type
        )
    )
"""

create_table_queries = [
    table_create,
]
drop_table_queries = [
    table_drop,
]

def drop_tables(session):
    for query in drop_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print(e)


def create_tables(session):
    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print(e)


def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def insert_data_from_file(session, filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
        for event in data:
            try:
                event_id = event["id"]
                event_type = event["type"]
                is_public = event["public"]

                query = """
                INSERT INTO events (id, type, public) VALUES (%s, %s, %s)
                """
                session.execute(query, (event_id, event_type, is_public))

                print(f"Inserted event: {event_id}, {event_type}, {is_public}")
            except Exception as e:
                print(f"Error inserting event: {str(e)}")


def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    # Create keyspace
    try:
        session.execute(
            """
            CREATE KEYSPACE IF NOT EXISTS github_events
            WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
            """
        )
    except Exception as e:
        print(e)

    # Set keyspace
    try:
        session.set_keyspace("github_events")
    except Exception as e:
        print(e)

    drop_tables(session)
    create_tables(session)

    # Insert data from file
    insert_data_from_file(session, filepath="/workspaces/dw-and-bi/data/github_events_01.json")

    # Select data in Cassandra and print them to stdout
    query = """
    SELECT * from events
    """
    try:
        rows = session.execute(query)
    except Exception as e:
        print(e)

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
