import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Electronic Shop POS", page_icon="🛒")

# --------------------------------------------------
# Shop Info
# --------------------------------------------------
shop_name = "Electronic Shop"
shop_city = "Karachi"

st.title(f"🏪 {shop_name}")
st.caption(f"📍 {shop_city}")

# --------------------------------------------------
# Customer Details
# --------------------------------------------------
st.subheader("👤 Customer Details")
customer_name = st.text_input("Enter customer name")

payment_method = st.selectbox(
    "Payment Method",
    ["Cash", "Credit Card", "Debit Card", "JazzCash", "EasyPaisa"]
)

# --------------------------------------------------
# Products (Price + Stock)
# --------------------------------------------------
products = {
    "Laptop": {"price": 85000, "stock": 5},
    "Mobile": {"price": 35000, "stock": 10},
    "TV": {"price": 50000, "stock": 4},
    "Headphones": {"price": 2000, "stock": 20},
    "Keyboard": {"price": 1200, "stock": 15},
    "Mouse": {"price": 700, "stock": 30},
    "Fan": {"price": 4000, "stock": 8},
    "Iron": {"price": 2500, "stock": 6},
}

# --------------------------------------------------
# Product Selection
# --------------------------------------------------
st.divider()
st.subheader("🛍️ Select Products")

selected_items = st.multiselect("Choose products", products.keys())
purchases = {}

if selected_items:
    for item in selected_items:
        qty = st.number_input(
            f"{item} (Stock: {products[item]['stock']})",
            min_value=1,
            max_value=products[item]["stock"],
            value=1,
            key=item
        )
        purchases[item] = qty

# --------------------------------------------------
# Save Transaction (FULL DATA)
# --------------------------------------------------
def save_transaction(customer, payment, bill_df):
    file_name = "transactions.csv"
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bill_df["Date"] = date_time
    bill_df["Customer"] = customer
    bill_df["Payment Method"] = payment

    bill_df = bill_df[
        ["Date", "Customer", "Product", "Quantity", "Unit Price", "Total", "Payment Method"]
    ]

    if os.path.exists(file_name):
        bill_df.to_csv(file_name, mode="a", header=False, index=False)
    else:
        bill_df.to_csv(file_name, index=False)

# --------------------------------------------------
# Billing Function
# --------------------------------------------------
def show_bill(pur_dict):
    total = 0
    bill_data = []

    for item, qty in pur_dict.items():
        price = products[item]["price"]
        cost = price * qty
        total += cost
        bill_data.append([item, qty, price, cost])

    df = pd.DataFrame(
        bill_data,
        columns=["Product", "Quantity", "Unit Price", "Total"]
    )

    st.subheader("🧾 Order Summary")
    st.table(df)

    discount = total * 0.10 if total > 50000 else 0
    final_amount = total - discount

    st.divider()
    st.write(f"**Subtotal:** Rs {total}")
    st.write(f"**Discount:** Rs {discount}")
    st.success(f"💰 Final Amount: Rs {final_amount}")
    st.info(f"💳 Payment Method: {payment_method}")

    # Save transaction
    save_transaction(customer_name, payment_method, df)

    # Receipt download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Receipt",
        csv,
        f"{customer_name}_receipt.csv",
        "text/csv"
    )

# --------------------------------------------------
# Generate Bill Button
# --------------------------------------------------
if st.button("🧾 Generate Bill"):
    if not customer_name:
        st.warning("Please enter customer name")
    elif not purchases:
        st.warning("Please select at least one product")
    else:
        show_bill(purchases)

# ==================================================
# REPORTS & ANALYTICS
# ==================================================
st.divider()
st.header("📊 Sales Reports & Analytics")

if os.path.exists("transactions.csv"):
    sales_df = pd.read_csv("transactions.csv")
    sales_df["Date"] = pd.to_datetime(sales_df["Date"])
    sales_df["Amount"] = sales_df["Total"]

    report_type = st.selectbox(
        "Select Report Type",
        ["Monthly Report", "Yearly Report"]
    )

    if report_type == "Monthly Report":
        sales_df["Month"] = sales_df["Date"].dt.to_period("M")
        monthly = sales_df.groupby("Month")["Amount"].sum().reset_index()

        st.subheader("📅 Monthly Sales Report")
        st.dataframe(monthly)

        st.bar_chart(monthly.set_index("Month"))

        st.success(f"💰 Total Monthly Sales: Rs {monthly['Amount'].sum()}")

        st.download_button(
            "📥 Download Monthly Report",
            monthly.to_csv(index=False).encode("utf-8"),
            "monthly_sales_report.csv",
            "text/csv"
        )

    else:
        sales_df["Year"] = sales_df["Date"].dt.year
        yearly = sales_df.groupby("Year")["Amount"].sum().reset_index()

        st.subheader("📆 Yearly Sales Report")
        st.dataframe(yearly)

        st.line_chart(yearly.set_index("Year"))

        st.success(f"💰 Total Yearly Sales: Rs {yearly['Amount'].sum()}")

        st.download_button(
            "📥 Download Yearly Report",
            yearly.to_csv(index=False).encode("utf-8"),
            "yearly_sales_report.csv",
            "text/csv"
        )

else:
    st.info("No transactions found. Generate a bill first.")
