from typing import NewType

import os  # Add this line
import json
from datetime import datetime
import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repos = "DROP TABLE IF EXISTS repos"
table_drop_issues = "DROP TABLE IF EXISTS issues"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id int,
        login text,
        display_login text,
        gravatar_id int,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""
table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id text,
        type text,
        actor_id int,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id)
    )
"""
table_create_repos = """
    CREATE TABLE IF NOT EXISTS repos (
        id int,
        name text,
        url text,
        PRIMARY KEY(id),
        UNIQUE(url)
    )
"""
table_create_issues = """
    CREATE TABLE IF NOT EXISTS issues (
        id int,
        url text,
        repository_url text,
        user_id int,
        title text,
        state text,
        locked boolean,
        assignee_id int,
        milestone_id int,
        comments int,
        created_at timestamp,
        updated_at timestamp,
        closed_at timestamp,
        author_association text,
        active_lock_reason text,
        body text,
        PRIMARY KEY(id),
        CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repository_url) REFERENCES repos(url)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_events,
    table_create_repos,
    table_create_issues,
]
drop_table_queries = [
    table_drop_events,
    table_drop_actors,
    table_drop_repos,
    table_drop_issues,
]


# def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
#     """
#     Drops each table using the queries in `drop_table_queries` list.
#     """
#     for query in drop_table_queries:
#         cur.execute(query)
#         conn.commit()

### Edit
def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in reversed(drop_table_queries):
        cur.execute(f"{query} CASCADE")
        conn.commit()
###

def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

#insert data

def get_file_path(file_name: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file_name)

def read_json_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def insert_data_from_file(cur: PostgresCursor, conn: PostgresConn, file_path: str) -> None:
    """
    Inserts data from a JSON file into the appropriate tables.
    """
    data = read_json_file('/workspaces/dw-and-bi/data/github_events_01.json')

    try:
        for event in data:
            actor = event.get("actor", {})
            repo = event.get("repo", {})
            payload = event.get("payload", {})
            issue = payload.get("issue", {})

            # Skip if issue id is missing or null
            if issue.get("id") is None:
                continue

            # Convert empty strings to None for integer columns
            actor_id = actor.get("id") or None
            gravatar_id = actor.get("gravatar_id") or None
            user_id = issue.get("user_id") or None
            assignee_id = issue.get("assignee_id") or None
            milestone_id = issue.get("milestone_id") or None
            comments = issue.get("comments") or None

            # Insert actor
            cur.execute("""
                INSERT INTO actors (id, login, display_login, gravatar_id, url, avatar_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                actor_id,
                actor.get("login"),
                actor.get("display_login"),
                gravatar_id,
                actor.get("url"),
                actor.get("avatar_url"),
            ))

            # Insert repo
            cur.execute("""
                INSERT INTO repos (id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                repo.get("id"),
                repo.get("name"),
                repo.get("url"),
            ))

            # Insert event
            cur.execute("""
                INSERT INTO events (id, type, actor_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                event.get("id"),
                event.get("type"),
                actor_id,
            ))

            # Convert empty strings to None for date columns
            created_at_str = event.get("created_at")
            updated_at_str = event.get("updated_at")
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00')) if created_at_str else None
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00')) if updated_at_str else None

            # Insert issue
            cur.execute("""
                INSERT INTO issues (
                    id, url, repository_url, user_id, title, state, locked, assignee_id, milestone_id,
                    comments, created_at, updated_at, closed_at, author_association, active_lock_reason, body
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                issue.get("id"),
                issue.get("url"),
                issue.get("repository_url"),
                user_id,
                issue.get("title"),
                issue.get("state"),
                issue.get("locked"),
                assignee_id,
                milestone_id,
                comments,
                created_at,
                updated_at,
                None,
                event.get("author_association"),
                event.get("active_lock_reason"),
                issue.get("body"),
            ))

        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {str(e)}")
        conn.rollback()


###

def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    json_file_path = get_file_path('/workspaces/dw-and-bi/data/github_events_01.json')
    insert_data_from_file(cur, conn, json_file_path)

    conn.close()


if __name__ == "__main__":
    main()
