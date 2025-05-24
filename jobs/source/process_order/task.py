from prefect import flow, task
from prefect.logging import get_run_logger
import random
import time


@task(name="Validate Order")
def validate_order(order_id: str) -> bool:

    logger = get_run_logger()
    logger.info(f"Validating order: {order_id}")
    time.sleep(1)
    is_valid = random.random() > 0.1  # 90% chance of success

    if is_valid:
        logger.info(f"Order {order_id} is valid")
    else:
        logger.warning(f"Order {order_id} failed validation")

    return is_valid


@task(name="Process Payment")
def process_payment(order_id: str) -> bool:

    logger = get_run_logger()
    logger.info(f"Processing payment for order: {order_id}")
    time.sleep(2)
    payment_success = random.random() > 0.05  # 95% chance of success

    if payment_success:
        logger.info(f"Payment for order {order_id} processed successfully")
    else:
        logger.error(f"Payment for order {order_id} failed")

    return payment_success


@task(name="Update Inventory")
def update_inventory(order_id: str) -> bool:

    logger = get_run_logger()
    logger.info(f"Updating inventory for order: {order_id}")
    # Simulate inventory update
    time.sleep(1.5)
    update_success = random.random() > 0.02  # 98% chance of success

    if update_success:
        logger.info(f"Inventory updated for order {order_id}")
    else:
        logger.error(f"Failed to update inventory for order {order_id}")

    return update_success


@task(name="Send Confirmation")
def send_confirmation(order_id: str) -> None:

    logger = get_run_logger()
    logger.info(f"Sending confirmation for order: {order_id}")
    # Simulate sending confirmation
    time.sleep(1)
    success = random.random() > 0.01  # 99% chance of success

    if success:
        logger.info(f"Confirmation sent for order {order_id}")
    else:
        logger.warning(f"Failed to send confirmation for order {order_id}")


@flow(name="Process Order Flow")
def process_order_flow(order_id: str):
    """
    Flow to process an order.

    Args:
        order_id (str): The ID of the order to be processed.
    """
    logger = get_run_logger()
    logger.info(f"Starting processing for order: {order_id}")

    # Step 1: Validate the order
    is_valid = validate_order(order_id)
    if not is_valid:
        logger.error(
            f"Order {order_id} processing stopped due to validation failure")
        return False

    # Step 2: Process payment
    payment_successful = process_payment(order_id)
    if not payment_successful:
        logger.error(
            f"Order {order_id} processing stopped due to payment failure")
        return False

    # Step 3: Update inventory
    inventory_updated = update_inventory(order_id)
    if not inventory_updated:
        logger.error(
            f"Order {order_id} processing encountered inventory update failure")
        # In this case, we might still want to proceed with the order

    # Step 4: Send confirmation
    send_confirmation(order_id)

    logger.info(f"Completed processing for order: {order_id}")
    return True
