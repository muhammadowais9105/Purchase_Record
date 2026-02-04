import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_sortable import sortable_list  # pip install streamlit-sortable

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Electronic Shop POS", page_icon="🛒")

# --------------------------------------------------
# Shop Info
# --------------------------------------------------
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

st.title(f"🏪 {shop_name}")
st.subheader(f"📍 Location: {shop_city}")

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
# Products with Price
# --------------------------------------------------
products = {
    "Laptop": 85000, "Mobile": 35000, "TV": 50000,
    "Headphones": 2000, "Keyboard": 1200, "Mouse": 700,
    "Fan": 4000, "Iron": 2500, "Speaker": 3000,
    "Charger": 900, "Camera": 60000, "Washing Machine": 55000
}

st.divider()
st.subheader("🛒 Drag & Drop Products in the Order You Want")

# Drag-and-drop sortable list
selected_items = sortable_list(list(products.keys()), direction="vertical")

# Quantity selection
purchases = {}
if selected_items:
    for item in selected_items:
        qty = st.number_input(f"Quantity for {item}:", min_value=1, value=1, key=item)
        purchases[item] = qty

# --------------------------------------------------
# Save Transaction
# --------------------------------------------------
def save_transaction(customer, payment, bill_df):
    file_name = "transactions.csv"
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bill_df = bill_df.copy()
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
# Billing Function with Styled Invoice
# --------------------------------------------------
def show_bill(pur_dict):
    total = 0
    bill_data = []

    st.markdown("""
    <style>
    .bill-box {
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bill-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🧾 OFFICIAL INVOICE</h2>", unsafe_allow_html=True)
    st.write(f"**Shop:** {shop_name} | **City:** {shop_city}")
    st.divider()

    for item, qty in pur_dict.items():
        price = products[item]
        cost = price * qty
        total += cost
        bill_data.append([item, qty, price, cost])
        st.write(f"🔹 {item} (x{qty}) : **Rs {cost:,}**")

    st.divider()

    discount = total * 0.10 if total > 50000 else 0
    final_amount = total - discount

    st.write(f"**Subtotal:** Rs {total:,}")
    st.write(f"**Discount:** Rs {discount:,}")
    st.success(f"💰 Final Amount: Rs {final_amount:,}")
    st.markdown("</div>", unsafe_allow_html=True)

    df = pd.DataFrame(bill_data, columns=["Product", "Quantity", "Unit Price", "Total"])
    return df

# --------------------------------------------------
# Generate Bill Button
# --------------------------------------------------
if shop_open:
    if st.button("🧾 Generate Invoice"):
        if not customer_name:
            st.warning("Please enter customer name")
        elif not purchases:
            st.warning("Please select at least one product")
        else:
            bill_df = show_bill(purchases)
            save_transaction(customer_name, payment_method, bill_df)
            # Download receipt
            csv = bill_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Receipt",
                csv,
                f"{customer_name}_receipt.csv",
                "text/csv"
            )
