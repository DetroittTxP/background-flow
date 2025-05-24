from prefect import flow


def _deployment_workflow(entrypoint, name, work_pool, tags):
    SOURCE_DIR = "/app/jobs"
    DEPLOYMENT_VERSION = "1.0"

    flow.from_source(
        source=SOURCE_DIR,
        entrypoint=entrypoint,
    ).deploy(
        name=name,
        work_pool_name=work_pool,
        tags=tags,
        version=DEPLOYMENT_VERSION,
    )


def deploy_flow():

    work_flow = [
        {
            "entrypoint": "process_order/flow.py:process_order_flow",
            "name": "run-process-order",
            "tags": ["order-processing", "deploy"],

        },
    ]

    for flow_config in work_flow:
        _deployment_workflow(
            entrypoint=flow_config["entrypoint"],
            name=flow_config["name"],
            work_pool="worker-site-default",
            tags=flow_config["tags"],
        )


def deploy():
    deploy_flow()


if __name__ == "__main__":
    deploy()
    print("Deployment flow executed.")
