"""Module that contains doc_path util."""
import os


def doc_path(relative_path: str) -> str:
    """
    Generate the absolute path to a YAML file used for Swagger documentation.

    Args:
        relative_path (str): Relative path to the YAML file.

    Returns:
        str: Absolute path to the specified YAML file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "docs", relative_path)
