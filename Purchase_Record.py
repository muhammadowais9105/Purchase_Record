import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Electronic Shop",
    page_icon="🛒",
    layout="centered"
)

# --- Shop Variables ---
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

# --- Header ---
st.title(f"🏪 Welcome to {shop_name}")
st.subheader(f"📍 Location: {shop_city}")

# --- Products Data ---
products = {
    "Laptop": 85000,
    "Mobile": 35000,
    "TV": 50000,
    "Headphones": 2000,
    "Keyboard": 1200,
    "Mouse": 700,
    "Fan": 4000,
    "Iron": 2500,
    "Speaker": 3000,
    "Charger": 900,
    "Camera": 60000,
    "Washing Machine": 55000
}

st.divider()
st.subheader("🛍️ Create Purchase Record")

# --- Product Selection ---
selected_items = st.multiselect(
    "Select products to buy:",
    list(products.keys())
)

purchases = {}

if selected_items:
    for item in selected_items:
        qty = st.number_input(
            f"Quantity for {item}:",
            min_value=1,
            value=1,
            key=item
        )
        purchases[item] = qty


# --- Billing Function ---
def show_bill(pur_dict):
    total = 0
    st.markdown("### 🧮 Bill Details")

    for item, qty in pur_dict.items():
        price = products[item]
        cost = price * qty
        total += cost
        st.write(f"**{item}** × {qty} = Rs {cost}")

    st.divider()

    # --- Discount Logic ---
    if total > 50000:
        discount = total * 0.10
        final_amount = total - discount
        st.info(f"🎉 10% Discount Applied: -Rs {discount:.0f}")
    else:
        final_amount = total
        st.warning("No discount applied (Buy above Rs 50,000 to get 10% off)")

    st.subheader(f"💰 Final Payable Amount: Rs {final_amount:.0f}")
    st.success("Thank you for shopping with us! 😊")


# --- Generate Bill Button ---
if shop_open:
    if st.button("🧾 Generate Bill"):
        if not purchases:
            st.error("Please select at least one product!")
        else:
            show_bill(purchases)
