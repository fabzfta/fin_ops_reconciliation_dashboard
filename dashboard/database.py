import os

import pandas as pd
import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """Create a PostgreSQL connection using environment variables."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def execute_query(query: str) -> pd.DataFrame:
    """Execute a read-only query and return the result as a DataFrame."""
    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def load_live_reconciliation() -> pd.DataFrame:
    """Load the production-like reconciliation results."""
    query = """
        SELECT *
        FROM analytics_analytics.reconciliation_summary
        ORDER BY company_name, stripe_invoice_id
    """

    return execute_query(query)


def load_demo_reconciliation() -> pd.DataFrame:
    """Load reconciliation results with controlled demo scenarios."""
    query = """
        SELECT *
        FROM analytics_analytics.reconciliation_scenarios
        ORDER BY company_name, stripe_invoice_id
    """

    return execute_query(query)