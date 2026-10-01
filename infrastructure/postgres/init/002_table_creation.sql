CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- ============================================================
-- CLIENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.dim_client (
    client_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    industry VARCHAR(255),
    country VARCHAR(100),
    currency VARCHAR(3),

    hubspot_company_id VARCHAR(100),
    stripe_customer_id VARCHAR(100),
    quickbooks_customer_id VARCHAR(100),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_client_hubspot
        UNIQUE (hubspot_company_id),

    CONSTRAINT uq_client_stripe
        UNIQUE (stripe_customer_id),

    CONSTRAINT uq_client_quickbooks
        UNIQUE (quickbooks_customer_id)
);


-- ============================================================
-- CONTACTS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.dim_contact (
    contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_id UUID NOT NULL
        REFERENCES core.dim_client(client_id),

    contact_name VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),

    email VARCHAR(255),
    job_title VARCHAR(255),
    phone VARCHAR(100),

    hubspot_contact_id VARCHAR(100),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_contact_hubspot
        UNIQUE (hubspot_contact_id)
);


-- ============================================================
-- CHART OF ACCOUNTS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.dim_account (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    quickbooks_account_id VARCHAR(100) NOT NULL,

    account_number VARCHAR(100),
    account_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(100),
    account_subtype VARCHAR(100),
    classification VARCHAR(100),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_account_quickbooks
        UNIQUE (quickbooks_account_id)
);


-- ============================================================
-- INVOICES
-- ============================================================

CREATE TABLE IF NOT EXISTS core.fact_invoice (
    invoice_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_id UUID NOT NULL
        REFERENCES core.dim_client(client_id),

    stripe_invoice_id VARCHAR(100),
    quickbooks_invoice_id VARCHAR(100),

    invoice_number VARCHAR(100),

    invoice_date DATE,
    due_date DATE,

    subtotal NUMERIC(18, 2),
    tax_amount NUMERIC(18, 2) NOT NULL DEFAULT 0,
    total_amount NUMERIC(18, 2) NOT NULL,

    amount_paid NUMERIC(18, 2) NOT NULL DEFAULT 0,
    amount_remaining NUMERIC(18, 2) NOT NULL DEFAULT 0,

    currency VARCHAR(3) NOT NULL,

    status VARCHAR(50),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_invoice_stripe
        UNIQUE (stripe_invoice_id),

    CONSTRAINT uq_invoice_quickbooks
        UNIQUE (quickbooks_invoice_id),

    CONSTRAINT ck_invoice_amounts
        CHECK (
            total_amount >= 0
            AND amount_paid >= 0
            AND amount_remaining >= 0
        )
);


-- ============================================================
-- PAYMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.fact_payment (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_id UUID NOT NULL
        REFERENCES core.dim_client(client_id),

    invoice_id UUID
        REFERENCES core.fact_invoice(invoice_id),

    stripe_payment_intent_id VARCHAR(100),
    stripe_charge_id VARCHAR(100),
    quickbooks_payment_id VARCHAR(100),

    payment_date TIMESTAMPTZ,

    amount NUMERIC(18, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,

    status VARCHAR(50),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_payment_stripe_intent
        UNIQUE (stripe_payment_intent_id),

    CONSTRAINT uq_payment_stripe_charge
        UNIQUE (stripe_charge_id),

    CONSTRAINT uq_payment_quickbooks
        UNIQUE (quickbooks_payment_id),

    CONSTRAINT ck_payment_amount
        CHECK (amount >= 0)
);


-- ============================================================
-- STRIPE BALANCE TRANSACTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.fact_stripe_transaction (
    stripe_transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_id UUID NOT NULL
        REFERENCES core.dim_client(client_id),

    payment_id UUID
        REFERENCES core.fact_payment(payment_id),

    stripe_balance_transaction_id VARCHAR(100) NOT NULL,

    source_amount NUMERIC(18, 2),
    source_currency VARCHAR(3),

    settlement_gross NUMERIC(18, 2) NOT NULL,
    settlement_fee NUMERIC(18, 2) NOT NULL DEFAULT 0,
    settlement_net NUMERIC(18, 2) NOT NULL,

    settlement_currency VARCHAR(3) NOT NULL,

    available_on TIMESTAMPTZ,

    reconciliation_status VARCHAR(50)
        NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_stripe_balance_transaction
        UNIQUE (stripe_balance_transaction_id),

    CONSTRAINT ck_stripe_settlement
        CHECK (
            settlement_gross - settlement_fee
            = settlement_net
        )
);


-- ============================================================
-- PAYOUTS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.fact_payout (
    payout_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    stripe_payout_id VARCHAR(100) NOT NULL,

    amount NUMERIC(18, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,

    status VARCHAR(50),

    payout_created_at TIMESTAMPTZ,
    arrival_date TIMESTAMPTZ,

    bank_transaction_id VARCHAR(255),

    reconciliation_status VARCHAR(50)
        NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_stripe_payout
        UNIQUE (stripe_payout_id)
);


-- ============================================================
-- PAYOUT ↔ STRIPE TRANSACTION BRIDGE
-- ============================================================

CREATE TABLE IF NOT EXISTS core.bridge_payout_transaction (
    payout_id UUID NOT NULL
        REFERENCES core.fact_payout(payout_id),

    stripe_transaction_id UUID NOT NULL
        REFERENCES core.fact_stripe_transaction(
            stripe_transaction_id
        ),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (
        payout_id,
        stripe_transaction_id
    )
);


-- ============================================================
-- GENERAL LEDGER
-- ============================================================

CREATE TABLE IF NOT EXISTS core.fact_gl_entry (
    gl_entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    client_id UUID NOT NULL
        REFERENCES core.dim_client(client_id),

    account_id UUID NOT NULL
        REFERENCES core.dim_account(account_id),

    invoice_id UUID
        REFERENCES core.fact_invoice(invoice_id),

    payment_id UUID
        REFERENCES core.fact_payment(payment_id),

    transaction_date DATE NOT NULL,

    source_system VARCHAR(50) NOT NULL,
    source_transaction_id VARCHAR(255),

    debit_amount NUMERIC(18, 2) NOT NULL DEFAULT 0,
    credit_amount NUMERIC(18, 2) NOT NULL DEFAULT 0,

    currency VARCHAR(3) NOT NULL,

    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ck_gl_debit_credit
        CHECK (
            (
                debit_amount > 0
                AND credit_amount = 0
            )
            OR
            (
                credit_amount > 0
                AND debit_amount = 0
            )
        )
);


-- ============================================================
-- CROSS-SYSTEM IDENTITY MAP
-- ============================================================

CREATE TABLE IF NOT EXISTS core.identity_map (
    entity_type VARCHAR(50) NOT NULL,

    internal_id UUID NOT NULL,

    source_system VARCHAR(50) NOT NULL,

    external_id VARCHAR(255) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (
        entity_type,
        source_system,
        external_id
    ),

    CONSTRAINT uq_identity_internal_source
        UNIQUE (
            entity_type,
            internal_id,
            source_system
        )
);