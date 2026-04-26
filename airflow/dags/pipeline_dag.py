from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "data_engineer",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="data_pipeline_e2e",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    run_ingestion = BashOperator(
        task_id="run_ingestion",
        bash_command=(
            "docker run --rm "
            "--network data_pipeline_data_network "
            "--env POSTGRES_HOST=postgres "
            "--env POSTGRES_PORT=5432 "
            "--env POSTGRES_DB=landing_db "
            "--env POSTGRES_USER=$POSTGRES_USER "
            "--env POSTGRES_PASSWORD=$POSTGRES_PASSWORD "
            "data_pipeline-ingestion"
        ),
    )

    airbyte_sync = BashOperator(
    task_id="airbyte_sync",
    bash_command="""
    RESPONSE=$(curl -s -u "$AIRBYTE_EMAIL:$AIRBYTE_PASSWORD" \
      -X POST http://host.docker.internal:8000/api/v1/connections/sync \
      -H "Content-Type: application/json" \
      -d '{"connectionId": "a4808516-348b-434d-bde0-70188a41087e"}')

    echo "$RESPONSE"

    echo "$RESPONSE" | grep -q '"job"' || exit 1
    echo "$RESPONSE" | grep -q '"status":"running"' || exit 1
    """,
)

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="docker exec dbt_clickhouse dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="docker exec dbt_clickhouse dbt test",
    )

    run_ingestion >> airbyte_sync >> dbt_run >> dbt_test