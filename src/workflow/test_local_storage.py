"""
Test the local RAW object storage.
"""

from datetime import datetime, timezone

from storage.storage import LocalObjectStorage


def main() -> None:
    storage = LocalObjectStorage()

    run_id = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    payload = {
        "id": "test_001",
        "source": "test",
        "message": "RAW storage is working",
    }

    file_path = storage.put_json(
        source="test",
        entity="objects",
        object_id="test_001",
        payload=payload,
        run_id=run_id,
    )

    print("")
    print("RAW object stored successfully")
    print("--------------------------------")
    print(f"Run ID: {run_id}")
    print(f"Path: {file_path}")


if __name__ == "__main__":
    main()