from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="kpo_onprem_smoke",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["onprem", "smoke"],
):
    KubernetesPodOperator(
        task_id="echo-onprem",
        name="echo-onprem",
        namespace="airflow-onprem",
        image="busybox",
        cmds=["/bin/sh", "-c"],
        arguments=["echo RUN_ONPREM_OK && env | sort && sleep 3"],
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=False,
        kubernetes_conn_id="kubernetes_onprem",
        kube_client_request_args={    # ← 핵심
            "headers": {"User-Agent": "airflow-kpo"}
        },
    )
