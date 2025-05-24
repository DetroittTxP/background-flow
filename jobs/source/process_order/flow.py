from prefect import flow
from prefect.logging import get_run_logger
import time


@flow(name="Process Order Flow")
def process_order_flow(order_id: str):
    """
    Flow to process an order.

    Args:
        order_id (str): The ID of the order to be processed.
    """
    print(f"Processing order with ID: {order_id}")
    logger = get_run_logger()
    logger.info(f"Starting to process order {order_id}")
    time.sleep(2)
    logger.info(f"Finished processing order {order_id}")

    # Here you would typically call tasks to handle the order processing logic
    # For example, validating the order, charging payment, updating inventory, etc.
