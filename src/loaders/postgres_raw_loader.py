"""
PostgreSQL RAW loader.

This module loads JSON objects from the filesystem RAW layer into
PostgreSQL while preserving the original payload.

The loader is idempotent. The same source record from the same
ingestion run cannot be inserted more than once.
"""

import json
import os

from datetime import date
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb


load_dotenv()


class PostgresRawLoader:
    """
    Load RAW JSON records into PostgreSQL.
    """

    def __init__(self) -> None:
        self.host = os.getenv(
            "POSTGRES_HOST",
            "localhost",
        )

        self.port = os.getenv(
            "POSTGRES_PORT",
            "5432",
        )

        self.database = os.getenv(
            "POSTGRES_DB",
            "finops",
        )

        self.user = os.getenv(
            "POSTGRES_USER",
            "finops",
        )

        self.password = os.getenv(
            "POSTGRES_PASSWORD",
        )

        if not self.password:
            raise ValueError(
                "POSTGRES_PASSWORD is not set."
            )

    def connect(self):
        """
        Create a PostgreSQL connection.
        """

        return psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password,
        )

    def load_record(
        self,
        source_system: str,
        entity_type: str,
        source_record_id: str,
        ingestion_date: date,
        run_id: str,
        raw_object_path: str,
        payload: dict,
    ) -> bool:
        """
        Load one RAW record into PostgreSQL.

        Returns:
            bool:
                True when a new record was inserted.
                False when the record already existed.
        """

        sql = """
            INSERT INTO raw.api_records (
                source_system,
                entity_type,
                source_record_id,
                ingestion_date,
                run_id,
                raw_object_path,
                payload
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (
                source_system,
                entity_type,
                source_record_id,
                run_id
            )
            DO NOTHING
            RETURNING ingestion_id;
        """

        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        source_system,
                        entity_type,
                        source_record_id,
                        ingestion_date,
                        run_id,
                        raw_object_path,
                        Jsonb(payload),
                    ),
                )

                result = cursor.fetchone()

        return result is not None

    @staticmethod
    def read_json(
        file_path: Path,
    ) -> dict:
        """
        Read a JSON file from the RAW filesystem.
        """

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)