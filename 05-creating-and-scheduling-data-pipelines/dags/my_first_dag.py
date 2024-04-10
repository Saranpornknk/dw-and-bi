from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone


#Open file Dag
with DAG(
    "my_first_dag", #dag ID is the same file name
    start_date=timezone.datetime(2024, 4, 9),
    schedule=None,    
    tags=["DS525"],
):
    my_first_task = EmptyOperator(task_id="my_first_task")
    my_second_task = EmptyOperator(task_id="my_second_task")

    my_first_task >> my_second_task