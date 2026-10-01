import pandas as pd
import streamlit as st

from database import (
    load_demo_reconciliation,
    load_live_reconciliation,
)


st.set_page_config(
    page_title="FinOps AI",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------

@st.cache_data(ttl=30)
def get_live_data() -> pd.DataFrame:
    """Load live reconciliation data."""
    return load_live_reconciliation()


@st.cache_data(ttl=30)
def get_demo_data() -> pd.DataFrame:
    """Load demo reconciliation data."""
    return load_demo_reconciliation()


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def format_usd(value) -> str:
    if pd.isna(value):
        return "-"

    return f"${float(value):,.2f}"


def format_brl(value) -> str:
    if pd.isna(value):
        return "-"

    return f"R$ {float(value):,.2f}"


def render_control(
    title: str,
    source_name: str,
    source_value,
    target_name: str,
    target_value,
    difference,
    reconciled: bool,
) -> None:
    """Render a financial reconciliation control."""

    with st.container(border=True):
        st.markdown(f"### {title}")

        col1, col2 = st.columns(2)

        col1.caption(source_name)
        col1.markdown(f"### {format_usd(source_value)}")

        col2.caption(target_name)
        col2.markdown(f"### {format_usd(target_value)}")

        st.caption("Difference")

        if float(difference or 0) == 0:
            st.markdown(f"### {format_usd(difference)}")
        else:
            st.markdown(f"### :red[{format_usd(difference)}]")

        if reconciled:
            st.success("RECONCILED")
        else:
            st.error("EXCEPTION")


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

st.title("FinOps AI")

st.caption(
    "Financial Data Integration & Autonomous Close"
)

st.divider()


# ---------------------------------------------------------------------
# Mode
# ---------------------------------------------------------------------

mode = st.segmented_control(
    "Reconciliation Mode",
    options=[
        "Live Reconciliation",
        "Demo Scenario",
    ],
    default="Live Reconciliation",
)


if mode == "Demo Scenario":
    df = get_demo_data()
    demo_mode = True

    st.warning(
        "Demo mode is active. Controlled test scenarios are being "
        "applied without modifying source financial data."
    )

else:
    df = get_live_data()
    demo_mode = False


if df.empty:
    st.warning("No reconciliation data available.")
    st.stop()


# ---------------------------------------------------------------------
# Client filter
# ---------------------------------------------------------------------

companies = sorted(
    df["company_name"]
    .dropna()
    .unique()
)

selected_company = st.selectbox(
    "Client",
    companies,
)

filtered_df = df[
    df["company_name"] == selected_company
].copy()


# ---------------------------------------------------------------------
# Determine status
# ---------------------------------------------------------------------

if demo_mode:

    status_column = "simulated_reconciliation_status"
    reason_column = "simulated_exception_reason"

else:

    status_column = "reconciliation_status"
    reason_column = "exception_reason"


exception_count = int(
    (
        filtered_df[status_column]
        == "EXCEPTION"
    ).sum()
)

reconciled_count = int(
    (
        filtered_df[status_column]
        == "RECONCILED"
    ).sum()
)

total_records = len(filtered_df)

reconciliation_rate = (
    reconciled_count / total_records * 100
    if total_records
    else 0
)


# ---------------------------------------------------------------------
# Close status
# ---------------------------------------------------------------------

st.subheader("Close Status")

if exception_count == 0:

    st.success(
        "FINANCIAL CLOSE HEALTHY — "
        "All reconciliation controls passed."
    )

else:

    st.error(
        f"FINANCIAL CLOSE REQUIRES REVIEW — "
        f"{exception_count} exception(s) detected."
    )


# ---------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------

invoice_total = float(
    filtered_df["invoice_amount"].fillna(0).sum()
)

collected_total = float(
    filtered_df["amount_received"].fillna(0).sum()
)

settlement_net = float(
    filtered_df["settlement_net"].fillna(0).sum()
)

fees = float(
    filtered_df["settlement_fee"].fillna(0).sum()
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Invoiced",
    format_usd(invoice_total),
)

col2.metric(
    "Collected",
    format_usd(collected_total),
)

col3.metric(
    "Net Settled",
    format_brl(settlement_net),
)

col4.metric(
    "Reconciliation Rate",
    f"{reconciliation_rate:.1f}%",
)

col5.metric(
    "Exceptions",
    exception_count,
)


st.divider()


# ---------------------------------------------------------------------
# Reconciliation controls
# ---------------------------------------------------------------------

st.subheader("Reconciliation Controls")

selected_invoice = st.selectbox(
    "Invoice",
    filtered_df["stripe_invoice_id"].tolist(),
)

row = filtered_df[
    filtered_df["stripe_invoice_id"]
    == selected_invoice
].iloc[0]


if demo_mode:

    qbo_invoice_amount = (
        row["simulated_quickbooks_total_amount"]
    )

    invoice_difference = (
        row["simulated_invoice_difference"]
    )

    invoice_reconciled = (
        float(invoice_difference) == 0
    )

else:

    qbo_invoice_amount = (
        row["quickbooks_total_amount"]
    )

    invoice_difference = (
        row["invoice_difference"]
    )

    invoice_reconciled = bool(
        row["invoice_reconciled"]
    )


control1, control2, control3 = st.columns(3)


with control1:

    render_control(
        title="Invoice",
        source_name="Stripe",
        source_value=row["invoice_amount"],
        target_name="QuickBooks",
        target_value=qbo_invoice_amount,
        difference=invoice_difference,
        reconciled=invoice_reconciled,
    )


with control2:

    render_control(
        title="Payment",
        source_name="Stripe",
        source_value=row["amount_received"],
        target_name="QuickBooks",
        target_value=row["quickbooks_payment_amount"],
        difference=row["payment_difference"],
        reconciled=bool(
            row["payment_reconciled"]
        ),
    )


with control3:

    with st.container(border=True):

        st.markdown("### Settlement")

        c1, c2 = st.columns(2)

        c1.caption("Gross")
        c1.markdown(
            f"### {format_brl(row['settlement_gross'])}"
        )

        c2.caption("Net")
        c2.markdown(
            f"### {format_brl(row['settlement_net'])}"
        )

        st.caption("Processing Fee")

        st.markdown(
            f"### {format_brl(row['settlement_fee'])}"
        )

        if bool(row["settlement_reconciled"]):
            st.success("RECONCILED")
        else:
            st.error("EXCEPTION")


# ---------------------------------------------------------------------
# Exception details
# ---------------------------------------------------------------------

st.divider()
st.subheader("Exception Management")


exceptions = filtered_df[
    filtered_df[status_column]
    == "EXCEPTION"
].copy()


if exceptions.empty:

    st.success(
        "No reconciliation exceptions detected."
    )

else:

    st.error(
        f"{len(exceptions)} financial exception(s) "
        "require investigation."
    )

    for _, exception in exceptions.iterrows():

        reason = exception[reason_column]

        with st.container(border=True):

            st.markdown(
                f"### {reason}"
            )

            st.write(
                f"Client: **{exception['company_name']}**"
            )

            st.write(
                "Stripe Invoice: "
                f"`{exception['stripe_invoice_id']}`"
            )

            if reason == "INVOICE_MISMATCH":

                if demo_mode:

                    difference = exception[
                        "simulated_invoice_difference"
                    ]

                    qbo_value = exception[
                        "simulated_quickbooks_total_amount"
                    ]

                else:

                    difference = exception[
                        "invoice_difference"
                    ]

                    qbo_value = exception[
                        "quickbooks_total_amount"
                    ]

                st.write(
                    "Stripe amount: "
                    f"**{format_usd(exception['invoice_amount'])}**"
                )

                st.write(
                    "QuickBooks amount: "
                    f"**{format_usd(qbo_value)}**"
                )

                st.write(
                    "Difference: "
                    f"**{format_usd(difference)}**"
                )


# ---------------------------------------------------------------------
# Settlement
# ---------------------------------------------------------------------

st.divider()
st.subheader("Settlement Breakdown")


gross = float(
    filtered_df["settlement_gross"]
    .fillna(0)
    .sum()
)

net = float(
    filtered_df["settlement_net"]
    .fillna(0)
    .sum()
)

average_fx = (
    filtered_df["exchange_rate"]
    .dropna()
    .astype(float)
    .mean()
)

fee_rate = (
    fees / gross * 100
    if gross
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Gross",
    format_brl(gross),
)

col2.metric(
    "Processing Fees",
    format_brl(fees),
)

col3.metric(
    "Net",
    format_brl(net),
)

col4.metric(
    "Fee Rate",
    f"{fee_rate:.2f}%",
)

col5.metric(
    "FX Rate",
    f"{average_fx:.5f}",
)


# ---------------------------------------------------------------------
# Transaction lineage
# ---------------------------------------------------------------------

st.divider()
st.subheader("Transaction Lineage")

st.caption(
    "End-to-end traceability across CRM, billing, "
    "accounting and payment processing."
)


lineage = {
    "HubSpot Deal": row["hubspot_deal_id"],
    "Stripe Invoice": row["stripe_invoice_id"],
    "QuickBooks Invoice": row["quickbooks_invoice_id"],
    "Stripe Payment Intent": row["stripe_payment_intent_id"],
    "QuickBooks Payment": row["quickbooks_payment_id"],
    "Stripe Charge": row["stripe_charge_id"],
    "Stripe Balance Transaction": (
        row["stripe_balance_transaction_id"]
    ),
}


for system, identifier in lineage.items():

    col1, col2 = st.columns(
        [1, 3]
    )

    col1.write(f"**{system}**")
    col2.code(str(identifier))


# ---------------------------------------------------------------------
# Raw reconciliation table
# ---------------------------------------------------------------------

st.divider()

with st.expander("Reconciliation Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )