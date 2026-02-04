import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop", page_icon="🛒")

# Step 1: (Variables)
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

st.title(f"🏪 Welcome to {shop_name}")
st.subheader(f"📍 Location: {shop_city}")

# Step 2: (Tuple)
owner = ("Muhammad Owais", "Manager", "madanielectronic9105@gmail.com")
st.sidebar.markdown(f"**Owner:** {owner[0]}")
st.sidebar.markdown(f"**Contact:** {owner[2]}")

# Step 4: (Set)
brands = {"Sure", "Sony", "Kenwood", "Paktech", "China Board"}
st.write("**Brands Available:** " + ", ".join(brands))

# Step 5: (Dictionary)
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

with st.expander("🛒 View Product Price List"):
    for name, price in products.items():
        st.write(f"- {name.title()}: **Rs {price}**")

# Step 6: Streamlit Input (Form use karenge taake interface acha lage)
st.divider()
st.subheader("🛍️ Create Purchase Record")

purchases = {}
selected_items = st.multiselect("Select products to buy:", list(products.keys()))

if selected_items:
    for item in selected_items:
        qty = st.number_input(f"Quantity for {item.title()}:", min_value=1, value=1, key=item)
        purchases[item] = qty

# Step 7 & 8: Calculation & Summary
def show_bill(pur_dict):
    total = 0
    st.markdown("### 🧮 Bill Details")
    for item, qty in pur_dict.items():
        price = products.get(item, 0)
        cost = price * qty
        total += cost
        st.write(f"{item.title()} (x{qty}) = **Rs {cost}**")
    
    st.divider()
    st.subheader(f"📊 Final Payable Amount: Rs {total}")
    st.success("Thank You for Shopping! 😊")

# Step 9 & 10: Run Program
if shop_open:
    if st.button("Generate Bill"):
        if not purchases:
            st.warning("Pehle kuch products select karein!")
        else:
            show_bill(purchases)
else:
    st.error("Shop Status: ❌ CLOSED")
