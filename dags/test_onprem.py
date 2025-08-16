from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="test_onprem",
    schedule_interval=None,
    catchup=False,
) as dag:
    test_task = KubernetesPodOperator(
        task_id="echo-task",
        name="echo-task",
        namespace="default",  # 온프렘 네임스페이스
        image="alpine:3.20",
        cmds=["sh", "-c"],
        arguments=["echo hello-from-onprem && sleep 5"],
        config_file="/opt/onprem/kubeconfig",  # 게이트웨이 kubeconfig
        get_logs=True,
        is_delete_operator_pod=True,
    )