from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="kpo_onprem_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["onprem", "smoke"],
):
    KubernetesPodOperator(
        task_id="echo-onprem",
        name="echo-onprem",
        namespace="airflow",  # ✅ airflow namespace 사용
        image="asia-northeast3-docker.pkg.dev/cbx-ai-vision/airflow/airflow-kpo:kpo-4",
        cmds=["/bin/sh", "-c"],
        arguments=["echo RUN_ONPREM_OK && env | sort && sleep 3"],
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,  # ✅ 클러스터 내부 인증 사용
        pod_template_file="/opt/airflow/pod_templates/pod_template_file.yaml",  # ✅ Secret mount 적용
    )
