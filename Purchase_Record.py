import streamlit as st
from fpdf import FPDF

# --- Page Config ---
st.set_page_config(page_title="Pro Electronic Store", page_icon="⚡", layout="wide")

# Initialize Stock in Session State (Taki refresh pe data na ure)
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "laptop": {"price": 85000, "stock": 10},
        "mobile": {"price": 35000, "stock": 20},
        "tv": {"price": 50000, "stock": 5},
        "headphones": {"price": 2000, "stock": 50},
        "camera": {"price": 60000, "stock": 8},
        "washing_machine": {"price": 55000, "stock": 4}
    }

# --- Styling ---
st.markdown("""
    <style>
    .stock-card {
        border-radius: 10px; padding: 10px; background-color: #f0f2f6;
        border-left: 5px solid #2E7D32; margin-bottom: 10px;
    }
    .bill-box {
        border: 2px solid #2E7D32; border-radius: 15px;
        padding: 25px; background-color: white; box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Inventory Status ---
with st.sidebar:
    st.header("📊 Current Stock Status")
    for item, details in st.session_state.inventory.items():
        color = "red" if details['stock'] < 3 else "black"
        st.markdown(f"""<div class='stock-card'>{item.title()}: 
                    <b style='color:{color}'>{details['stock']}</b> left</div>""", unsafe_allow_html=True)

# --- Main Shop UI ---
st.title("⚡ Pro Electronic Store Management")
st.write("Manage sales, stocks, and generate professional invoices.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛒 Customer Selection")
    selected_items = st.multiselect("Items choose karein:", list(st.session_state.inventory.keys()))
    
    purchases = {}
    if selected_items:
        for item in selected_items:
            max_qty = st.session_state.inventory[item]['stock']
            if max_qty > 0:
                qty = st.number_input(f"Qty for {item.title()} (Max: {max_qty})", 
                                      min_value=1, max_value=max_qty, key=f"buy_{item}")
                purchases[item] = qty
            else:
                st.error(f"⚠️ {item.title()} is Out of Stock!")

# --- Bill Generation Logic ---
with col2:
    st.subheader("🧾 Invoice Section")
    if st.button("Generate & Update Stock"):
        if not purchases:
            st.warning("Please select items first!")
        else:
            total_raw = sum(st.session_state.inventory[item]['price'] * qty for item, qty in purchases.items())
            discount = total_raw * 0.10 if total_raw > 50000 else 0
            final_amount = total_raw - discount

            # Update Stock in Session State
            for item, qty in purchases.items():
                st.session_state.inventory[item]['stock'] -= qty

            # Display Bill Box
            st.markdown('<div class="bill-box">', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>INVOICE</h3>", unsafe_allow_html=True)
            for item, qty in purchases.items():
                cost = st.session_state.inventory[item]['price'] * qty
                st.write(f"{item.title()} x{qty}: Rs {cost:,}")
            
            st.divider()
            if discount > 0: st.write(f"Discount: -Rs {discount:,}")
            st.subheader(f"Total: Rs {final_amount:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.balloons()
            st.success("Stock Updated Successfully!")

# --- PDF Feature (Optional) ---
# (Yahan aap pichla PDF function dobara add kar sakte hain)
