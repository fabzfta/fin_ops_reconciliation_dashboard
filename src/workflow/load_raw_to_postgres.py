"""
Load filesystem RAW objects into PostgreSQL.

Expected RAW path structure:

data/raw/
    <source_system>/
        <entity_type>/
            ingestion_date=YYYY-MM-DD/
                run_id=<run_id>/
                    <source_record_id>.json
"""

from datetime import date
from pathlib import Path

from loaders.postgres_raw_loader import PostgresRawLoader


RAW_BASE_PATH = Path("data/raw")


def parse_raw_path(
    file_path: Path,
) -> dict:
    """
    Extract ingestion metadata from a RAW object path.

    Args:
        file_path:
            Path to a RAW JSON object.

    Returns:
        dict:
            Metadata extracted from the path.
    """

    relative_path = file_path.relative_to(
        RAW_BASE_PATH
    )

    parts = relative_path.parts

    if len(parts) != 5:
        raise ValueError(
            f"Unexpected RAW path structure: {file_path}"
        )

    source_system = parts[0]
    entity_type = parts[1]

    ingestion_date_part = parts[2]
    run_id_part = parts[3]

    if not ingestion_date_part.startswith(
        "ingestion_date="
    ):
        raise ValueError(
            f"Invalid ingestion date partition: {file_path}"
        )

    if not run_id_part.startswith(
        "run_id="
    ):
        raise ValueError(
            f"Invalid run ID partition: {file_path}"
        )

    ingestion_date_value = (
        ingestion_date_part.split(
            "=",
            1,
        )[1]
    )

    run_id = run_id_part.split(
        "=",
        1,
    )[1]

    source_record_id = file_path.stem

    return {
        "source_system": source_system,
        "entity_type": entity_type,
        "source_record_id": source_record_id,
        "ingestion_date": date.fromisoformat(
            ingestion_date_value
        ),
        "run_id": run_id,
    }


def main() -> None:
    """
    Discover RAW JSON objects and load them into PostgreSQL.
    """

    if not RAW_BASE_PATH.exists():
        raise ValueError(
            f"RAW directory does not exist: {RAW_BASE_PATH}"
        )

    loader = PostgresRawLoader()

    files = sorted(
        RAW_BASE_PATH.rglob("*.json")
    )

    print("")
    print("RAW → PostgreSQL Loader")
    print("=======================")
    print(f"Files discovered: {len(files)}")

    inserted = 0
    skipped = 0
    failed = 0

    for file_path in files:

        try:
            metadata = parse_raw_path(
                file_path
            )

            payload = loader.read_json(
                file_path
            )

            was_inserted = loader.load_record(
                source_system=metadata[
                    "source_system"
                ],
                entity_type=metadata[
                    "entity_type"
                ],
                source_record_id=metadata[
                    "source_record_id"
                ],
                ingestion_date=metadata[
                    "ingestion_date"
                ],
                run_id=metadata[
                    "run_id"
                ],
                raw_object_path=str(
                    file_path
                ),
                payload=payload,
            )

            if was_inserted:
                inserted += 1

                print(
                    "[INSERTED] "
                    f"{metadata['source_system']}/"
                    f"{metadata['entity_type']}/"
                    f"{metadata['source_record_id']}"
                )

            else:
                skipped += 1

                print(
                    "[SKIPPED]  "
                    f"{metadata['source_system']}/"
                    f"{metadata['entity_type']}/"
                    f"{metadata['source_record_id']}"
                )

        except Exception as error:
            failed += 1

            print(
                f"[FAILED]   {file_path}"
            )

            print(
                f"           {error}"
            )

    print("")
    print("Load completed")
    print("==============")
    print(f"Inserted: {inserted}")
    print(f"Skipped:  {skipped}")
    print(f"Failed:   {failed}")


if __name__ == "__main__":
    main()