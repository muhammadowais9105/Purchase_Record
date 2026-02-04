import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop", page_icon="🛒")

# Step 1: (Variables)
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

st.title(f"🏪 Welcome to {shop_name}")
st.subheader(f"📍 Location: {shop_city}")

# Products Data
products = {
    "laptop": 85000,
    "mobile": 35000,
    "tv": 50000,
    "headphones": 2000,
    "keyboard": 1200,
    "mouse": 700,
    "fan": 4000,
    "iron": 2500,
    "speaker": 3000,
    "charger": 900,
    "camera": 60000,
    "washing_machine": 55000
}

# User Selection
st.divider()
st.subheader("🛍️ Create Purchase Record")
selected_items = st.multiselect("Select products to buy:", list(products.keys()))

purchases = {}
if selected_items:
    for item in selected_items:
        qty = st.number_input(f"Quantity for {item.title()}:", min_value=1, value=1, key=item)
        purchases[item] = qty

# Calculation Function with Discount
def show_bill(pur_dict):
    total = 0
    st.markdown("### 🧮 Bill Details")
    for item, qty in pur_dict.items():
        price = products.get(item, 0)
        cost = price * qty
        total += cost
        st.write(f"{item.title()} (x{qty}) = **Rs {cost}**")
    
    st.divider()
    
    # --- Discount Logic ---
    # Agar total 50,000 se upar ho toh 10% discount milega
    if total > 50000:
        discount = total * 0.10
        final_amount = total - discount
        st.info(f"🎉 10% Discount Applied: -Rs {discount}")
    else:
        final_amount = total
        st.write("No discount applied (Buy more than Rs 50,000 for 10% off!)")

    st.subheader(f"📊 Final Payable Amount: Rs {final_amount}")
    st.success("Thank You for Shopping! 😊")

# Run Button
if shop_open:
    if st.button("Generate Bill"):
        if not purchases:
            st.warning("Pehle kuch products select karein!")
        else:
            show_bill(purchases)
