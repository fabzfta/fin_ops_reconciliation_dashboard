CREATE TABLE IF NOT EXISTS raw.api_records (
    ingestion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    source_system VARCHAR(50) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    source_record_id VARCHAR(255) NOT NULL,

    ingestion_date DATE NOT NULL,
    run_id VARCHAR(100) NOT NULL,

    raw_object_path TEXT NOT NULL,
    payload JSONB NOT NULL,

    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_raw_api_record
        UNIQUE (
            source_system,
            entity_type,
            source_record_id,
            run_id
        )
);

CREATE INDEX IF NOT EXISTS idx_raw_api_records_source
    ON raw.api_records (
        source_system,
        entity_type
    );

CREATE INDEX IF NOT EXISTS idx_raw_api_records_run
    ON raw.api_records (
        run_id
    );

CREATE INDEX IF NOT EXISTS idx_raw_api_records_payload
    ON raw.api_records
    USING GIN (
        payload
    );