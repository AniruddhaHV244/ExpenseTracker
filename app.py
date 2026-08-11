import streamlit as st
from datetime import date

from database import (
    create_table,
    add_expense,
    get_expenses,
    get_monthly_total
)


# -----------------------------------
# Database
# -----------------------------------

create_table()


# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# -----------------------------------
# Title
# -----------------------------------

st.title("💰 My Expense Tracker")

st.write(
    "Track your daily expenses and manage your monthly budget."
)

st.divider()


# -----------------------------------
# Add Expense
# -----------------------------------

st.header("➕ Add Expense")

col1, col2 = st.columns(2)


with col1:

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other"
        ]
    )


with col2:

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    description = st.text_input(
        "Description",
        placeholder="Example: Lunch"
    )


if st.button("➕ Add Expense", type="primary"):

    if amount <= 0:

        st.error("Please enter an amount greater than ₹0.")

    else:

        add_expense(
            amount,
            category,
            description,
            expense_date.isoformat()
        )

        st.success(
            f"₹{amount:,.2f} expense added successfully!"
        )

        st.rerun()


# -----------------------------------
# Current month
# -----------------------------------

today = date.today()

current_month = today.strftime("%Y-%m")


# -----------------------------------
# Monthly calculations
# -----------------------------------

monthly_limit = 30000

total_spent = get_monthly_total(current_month)

remaining = monthly_limit - total_spent


# -----------------------------------
# Dashboard
# -----------------------------------

st.divider()

st.header("📊 Monthly Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Monthly Limit",
        f"₹{monthly_limit:,.2f}"
    )


with col2:

    st.metric(
        "Total Spent",
        f"₹{total_spent:,.2f}"
    )


with col3:

    st.metric(
        "Remaining",
        f"₹{remaining:,.2f}"
    )


# -----------------------------------
# Warning
# -----------------------------------

percentage_used = (
    total_spent / monthly_limit * 100
    if monthly_limit > 0
    else 0
)


if percentage_used >= 100:

    st.error(
        f"🚨 You have exceeded your monthly limit by "
        f"₹{abs(remaining):,.2f}!"
    )

elif percentage_used >= 90:

    st.error(
        f"🚨 You have used {percentage_used:.1f}% "
        "of your monthly limit!"
    )

elif percentage_used >= 70:

    st.warning(
        f"⚠️ You have used {percentage_used:.1f}% "
        "of your monthly limit."
    )


# -----------------------------------
# Progress bar
# -----------------------------------

progress = min(
    total_spent / monthly_limit,
    1.0
) if monthly_limit > 0 else 0

st.progress(progress)

st.write(
    f"**{percentage_used:.1f}%** of your monthly budget used"
)


# -----------------------------------
# Expense history
# -----------------------------------

st.divider()

st.header("📋 Expense History")


expenses = get_expenses()


if not expenses:

    st.info("No expenses added yet.")

else:

    for expense in expenses:

        expense_id = expense[0]
        expense_amount = expense[1]
        expense_category = expense[2]
        expense_description = expense[3]
        expense_date = expense[4]

        st.write(
            f"**{expense_category}** — "
            f"₹{expense_amount:,.2f}"
        )

        st.caption(
            f"{expense_date} | {expense_description}"
        )

        st.divider()
