# Implement ETL to BigQuery

This project test to do about implement ETL to BigQuery

* BigQuery: BigQuery is a fully managed, serverless data warehouse provided by Google Cloud Platform (GCP). It is designed to handle large-scale data analytics workloads and offers features such as scalability, real-time analytics, and built-in machine learning capabilities.

* Definition of ETL: ETL stands for Extract, Transform, Load. It's a process used in data warehousing and data integration to move data from various sources, transform it into a usable format, and load it into a target destination, such as a data warehouse.

* Implementing ETL to BigQuery:

    * Extract: Data can be extracted from various sources using different methods, such as Google Cloud Storage (GCS), Cloud Storage Transfer Service, Google Cloud Pub/Sub, Cloud Dataflow, or third-party tools.
    * Transform: Transformation of data can be done using various tools and technologies. Google Cloud Dataflow, Apache Beam, or even SQL queries within BigQuery itself can be used for data transformation tasks.
    * Load: Once the data has been transformed, it can be loaded into BigQuery using its native capabilities for data ingestion. This can be done through batch loads, streaming inserts, or data transfer services.


## How work this Project 

This project aims to extract data from the 'github_event_01.json' file and collect specific fields such as "id," "type," "actor," and "created_at" into Google BigQuery for analysis purposes.

The data extracted from this file will enable analysts to perform various analyses, including:

* Counting the occurrences of different event types.
* Counting the number of events created by each actor.
* Analyzing event types or actors based on the creation timestamp ('created_at').

By leveraging the collected data in BigQuery, analysts can gain insights into the frequency of different event types on GitHub, identify the most active actors in terms of event creation, and explore trends in event types or actor activities over time by analyzing their creation timestamps.

This project facilitates the efficient storage, management, and analysis of GitHub event data, empowering users to derive actionable insights and make informed decisions based on the patterns and trends observed within the dataset.





