import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop", page_icon="🛒")

# --- Shop Info ---
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

st.title(f"🏪 {shop_name}")
st.caption(f"📍 {shop_city}")

# --- Customer Details ---
st.subheader("👤 Customer Details")
customer_name = st.text_input("Enter customer name:")

payment_method = st.selectbox(
    "Select payment method:",
    ["Cash", "Credit Card", "Debit Card", "JazzCash", "EasyPaisa"]
)

# --- Products with Price & Stock ---
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

st.divider()
st.subheader("🛍️ Select Products")

selected_items = st.multiselect("Choose products:", products.keys())
purchases = {}

if selected_items:
    for item in selected_items:
        max_qty = products[item]["stock"]
        qty = st.number_input(
            f"{item} (Stock: {max_qty})",
            min_value=1,
            max_value=max_qty,
            value=1,
            key=item
        )
        purchases[item] = qty


# --- Billing Function ---
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

    # --- Discount ---
    if total > 50000:
        discount = total * 0.10
    else:
        discount = 0

    final_amount = total - discount

    st.divider()
    st.write(f"**Subtotal:** Rs {total}")
    st.write(f"**Discount:** Rs {discount}")
    st.success(f"💰 Final Amount: Rs {final_amount}")
    st.info(f"💳 Payment Method: {payment_method}")

    # --- Receipt Download ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Receipt",
        csv,
        f"{customer_name}_receipt.csv",
        "text/csv"
    )


# --- Generate Bill ---
if shop_open:
    if st.button("🧾 Generate Bill"):
        if not customer_name:
            st.warning("Please enter customer name")
        elif not purchases:
            st.warning("Please select at least one product")
        else:
            show_bill(purchases)
