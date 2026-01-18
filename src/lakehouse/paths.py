import os
from pathlib import Path
from lakehouse.config_loader import load_yaml

class PathResolver:
    """
    Resolve logical paths to real local or S3 paths.
    No infrastructure details are stored in Git.
    """

    def __init__(self):
        # Mandatory environment
        self.app_env = os.environ.get("APP_ENV")
        if not self.app_env:
            raise RuntimeError("APP_ENV environment variable is required")

        #logical paths
        self.paths_cfg = load_yaml("paths.yaml")

        # local data root (DEV only)
        self.data_root = Path(
            os.getenv("DATA_BASE_PATH", "/opt/lakehouse/data")
        )

        # S3 bucket must come from environment (repo public safe)
        self.s3_bucket = os.environ.get("S3_BUCKET")
        if not self.s3_bucket:
            raise RuntimeError("S3_BUCKET environment variable is required")

    def local_input(self, filename: str) -> str:
        """
        Resolve a local input file path.
        """
        return str(self.data_root / filename)

    def s3_layer_path(self, layer: str, dataset: str) -> str:
        """
        Resolve an S3 path for a given layer and dataset.
        """
        try:
            prefix = self.paths_cfg["paths"][layer]
        except KeyError:
            raise ValueError(f"Unknown data layer: {layer}")

        return f"s3a://{self.s3_bucket}/{prefix}/{dataset}"
