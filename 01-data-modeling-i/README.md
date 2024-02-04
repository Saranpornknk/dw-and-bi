# Data-Modeling-i

### Create table and Insert data with Relational Database in Postgrest

Overview of the relationships between the tables in database:

1. Actors Table (actors):
    - id (Primary Key): Identifier for the actor.
    - login: Actor's login name.
    - display_login: Display name for the actor.
    - gravatar_id: Gravatar ID of the actor.
    - url: URL associated with the actor.
    - avatar_url: URL of the actor's avatar image.

2. Repos Table (repos):
    - id (Primary Key): Identifier for the repository.
    - name: Name of the repository.
    - url: URL of the repository.

3. Events Table (events):
    - id (Primary Key): Identifier for the event.
    - type: Type of the event.
    - actor_id (Foreign Key referencing actors.id): Identifier for the actor associated with the event.

4. Issues Table (issues):
    - id (Primary Key): Identifier for the issue.
    - url: URL of the issue.
    - repository_url (Foreign Key referencing repos.url): URL of the repository associated with the issue.
    - user_id (Foreign Key referencing actors.id): Identifier for the user associated with the issue.
    - title: Title of the issue.
    - state: State of the issue (e.g., open, closed).
    - locked: Boolean indicating whether the issue is locked.
    - assignee_id (Foreign Key referencing actors.id): Identifier for the user assigned to the issue.
    - milestone_id: Identifier for the milestone associated with the issue.
    - comments: Number of comments on the issue.
    - created_at: Timestamp indicating when the issue was created.
    - updated_at: Timestamp indicating when the issue was last updated.
    - closed_at: Timestamp indicating when the issue was closed.
    - author_association: Association of the author with the issue.
    - active_lock_reason: Reason for the active lock on the issue.
    - body: Body or content of the issue.


This schema represents the relationships between the tables using foreign key constraints. 
Specifically, the actor_id in the events table refers to the id in the actors table, the repository_url in the issues table refers to the url in the repos table, and the user_id and assignee_id in the issues table both refer to the id in the actors table.

### Example analyses based on the tables

1. Number of Events by Actor:
    - Query: SELECT actors.login, COUNT(events.id) AS event_count FROM actors JOIN events ON actors.id = events.actor_id GROUP BY actors.login;
    - Insight: This analysis shows the number of events performed by each actor. It helps identify the most active contributors.

2. Top Repositories by Number of Issues:
    - Query: SELECT repos.name, COUNT(issues.id) AS issue_count FROM repos JOIN issues ON repos.url = issues.repository_url GROUP BY repos.name ORDER BY issue_count DESC LIMIT 5;
    - Insight: This analysis provides information about the repositories with the highest number of issues. It can help identify which repositories require more attention or have significant activity.

3. Timeline of Issue Creation Over Time:
    - Query: SELECT DATE_TRUNC('day', created_at) AS issue_date, COUNT(id) AS issue_count FROM issues GROUP BY issue_date ORDER BY issue_date;
    - Insight: This analysis visualizes the timeline of issue creation over time, helping identify patterns or trends.