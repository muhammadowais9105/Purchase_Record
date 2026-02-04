import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop", page_icon="🛒")

# Custom CSS for the "Beautiful Box"
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

# Variables
shop_name = "Electronic Shop"
shop_city = "Karachi"
shop_open = True

st.title(f"🏪 Welcome to {shop_name}")
st.subheader(f"📍 Location: {shop_city}")

# Products Data
products = {
    "laptop": 85000, "mobile": 35000, "tv": 50000,
    "headphones": 2000, "keyboard": 1200, "mouse": 700,
    "fan": 4000, "iron": 2500, "speaker": 3000,
    "charger": 900, "camera": 60000, "washing_machine": 55000
}

st.divider()
st.subheader("🛍️ Create Purchase Record")
selected_items = st.multiselect("Select products to buy:", list(products.keys()))

purchases = {}
if selected_items:
    cols = st.columns(2) # Items ko display karne ke liye columns
    for i, item in enumerate(selected_items):
        with cols[i % 2]:
            qty = st.number_input(f"Quantity for {item.title()}:", min_value=1, value=1, key=item)
            purchases[item] = qty

# Calculation Function with Box Styling
def show_bill(pur_dict):
    total = 0
    # Container start
    with st.container():
        st.markdown('<div class="bill-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🧾 OFFICIAL INVOICE</h2>", unsafe_allow_html=True)
        st.write(f"**Shop:** {shop_name} | **City:** {shop_city}")
        st.divider()
        
        for item, qty in pur_dict.items():
            price = products.get(item, 0)
            cost = price * qty
            total += cost
            st.write(f"🔹 {item.title()} (x{qty}) : **Rs {cost:,}**")
        
        st.divider()
        
        if total > 50000:
            discount = total * 0.1
