import logging

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone





def _say_hello():
    logging.debug("This is DEBUG log")
    logging.info("hello")

#Open file Dag
with DAG(
    "hello", #dag ID is the same file name
    start_date=timezone.datetime(2024, 4, 9),
    schedule=None,    
    tags=["DS525"],
):
    start = EmptyOperator(task_id="start")

    echo_hello = BashOperator(
        task_id="echo_hello",
        bash_command = "echo 'hello'",
    )

    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=_say_hello,
    )

    end = EmptyOperator(task_id="end")

    start >> echo_hello >> end
    start >> say_hello >> end