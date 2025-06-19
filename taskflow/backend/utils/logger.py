"""Module that contains the logger."""
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

logger = logging.getLogger("TaskFlowLogger")