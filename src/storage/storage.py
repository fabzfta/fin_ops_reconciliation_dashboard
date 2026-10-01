"""
Local object storage abstraction.

The local filesystem is used as the RAW storage layer during
development. In production, this interface can be replaced by
an Amazon S3 implementation.
"""

import json

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class LocalObjectStorage:
    """
    Store raw JSON objects in the local filesystem.
    """

    def __init__(
        self,
        base_path: str = "data/raw",
    ) -> None:
        self.base_path = Path(base_path)

    def put_json(
        self,
        source: str,
        entity: str,
        object_id: str,
        payload: dict[str, Any],
        run_id: str,
        ingestion_time: datetime | None = None,
    ) -> Path:
        """
        Persist a JSON payload in the RAW storage layer.

        Objects are partitioned by ingestion date and ingestion run.
        """

        ingestion_time = ingestion_time or datetime.now(
            timezone.utc
        )

        ingestion_date = ingestion_time.date().isoformat()

        directory = (
            self.base_path
            / source
            / entity
            / f"ingestion_date={ingestion_date}"
            / f"run_id={run_id}"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = directory / f"{object_id}.json"

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                indent=2,
                ensure_ascii=False,
                default=str,
            )

        return file_path