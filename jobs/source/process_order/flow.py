from prefect import flow
from prefect.logging import get_run_logger

from process_order.task import process_payment, send_confirmation, update_inventory, validate_order


@flow(name="Process Order Flow")
def process_order_flow(order_id: str):

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

    # Step 4: Send confirmationß
    send_confirmation(order_id)

    logger.info(f"Completed processing for order: {order_id}")
    return True
