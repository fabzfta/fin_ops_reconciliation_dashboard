"""
Configure the NovaTech SaaS Chart of Accounts in QuickBooks.
"""

from integrations.quickbooks.accounts import QuickBooksAccounts
from integrations.quickbooks.clients import QuickBooksClient


NOVATECH_ACCOUNTS = [
    {
        "name": "Deferred Revenue",
        "type": "Other Current Liability",
        "subtype": "OtherCurrentLiabilities",
    },
    {
        "name": "Accrued Expenses",
        "type": "Other Current Liability",
        "subtype": "OtherCurrentLiabilities",
    },
    {
        "name": "Subscription Revenue",
        "type": "Income",
        "subtype": "ServiceFeeIncome",
    },
    {
        "name": "Professional Services Revenue",
        "type": "Income",
        "subtype": "ServiceFeeIncome",
    },
    {
        "name": "Hosting Costs",
        "type": "Cost of Goods Sold",
        "subtype": "SuppliesMaterialsCogs",
    },
    {
        "name": "Customer Support",
        "type": "Cost of Goods Sold",
        "subtype": "SuppliesMaterialsCogs",
    },
    {
        "name": "Salaries & Wages",
        "type": "Expense",
        "subtype": "PayrollExpenses",
    },
    {
        "name": "Sales & Marketing",
        "type": "Expense",
        "subtype": "AdvertisingPromotional",
    },
    {
        "name": "Software & SaaS",
        "type": "Expense",
        "subtype": "DuesSubscriptions",
    },
    {
        "name": "Stripe Clearing",
        "type": "Other Current Asset",
        "subtype": "OtherCurrentAssets",
    },
    {
        "name": "Stripe Processing Fees",
        "type": "Expense",
        "subtype": "BankCharges",
    },
]


def main() -> None:
    client = QuickBooksClient()
    accounts = QuickBooksAccounts(client)

    print("")
    print("Configuring NovaTech Chart of Accounts")
    print("--------------------------------------")

    for definition in NOVATECH_ACCOUNTS:
        accounts.get_or_create_account(
            name=definition["name"],
            account_type=definition["type"],
            account_subtype=definition["subtype"],
        )

    print("")
    print("Chart of Accounts configuration completed.")


if __name__ == "__main__":
    main()