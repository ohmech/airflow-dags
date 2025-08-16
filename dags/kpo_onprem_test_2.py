from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="kpo_onprem_test_2",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["onprem", "smoke"],
):
    KubernetesPodOperator(
        task_id="echo-onprem",
        name="echo-onprem",
        namespace="airflow-onprem",
        image="asia-northeast3-docker.pkg.dev/cbx-ai-vision/airflow/airflow-kpo:kpo-4",
        cmds=["/bin/sh", "-c"],
        arguments=["echo RUN_ONPREM_OK && env | sort && sleep 3"],
        get_logs=True,
        is_delete_operator_pod=True,

        # ✅ 여기 고침
        in_cluster=False,
        config_file="/opt/onprem/kubeconfig",  # Secret으로 마운트한 kubeconfig
    )
