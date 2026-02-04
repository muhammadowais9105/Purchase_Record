import streamlit as st
import pandas as pd

st.set_page_config(page_title="ShopMaster 2026", layout="wide")

# Database setup
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = pd.DataFrame(columns=["Item", "Price", "Stock"])
if 'sales' not in st.session_state:
    st.session_state['sales'] = []

st.title("🛒 ShopMaster: Digital Billing & Inventory")

tab1, tab2, tab3 = st.tabs(["➕ Add Stock", "🧾 Create Bill", "📊 Reports"])

with tab1:
    st.header("Stock Management")
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("Product Name")
    with col2: price = st.number_input("Selling Price", min_value=0)
    with col3: stock = st.number_input("Opening Stock", min_value=0)
    
    if st.button("Add to Inventory"):
        new_item = pd.DataFrame([[name, price, stock]], columns=["Item", "Price", "Stock"])
        st.session_state.inventory = pd.concat([st.session_state.inventory, new_item], ignore_index=True)
        st.success("Stock Updated!")

with tab2:
    st.header("Customer Billing")
    if not st.session_state.inventory.empty:
        c_name = st.text_input("Customer Name")
        item_to_sell = st.selectbox("Select Product", st.session_state.inventory["Item"])
        qty_to_sell = st.number_input("Quantity", min_value=1)
        
        if st.button("Generate Bill"):
            idx = st.session_state.inventory.index[st.session_state.inventory["Item"] == item_to_sell][0]
            if st.session_state.inventory.at[idx, "Stock"] >= qty_to_sell:
                # Update Stock
                st.session_state.inventory.at[idx, "Stock"] -= qty_to_sell
                total = st.session_state.inventory.at[idx, "Price"] * qty_to_sell
                # Record Sale
                st.session_state.sales.append({"Customer": c_name, "Item": item_to_sell, "Total": total})
                st.balloons()
                st.write(f"### Bill for {c_name}: Rs {total}")
            else:
                st.error("Out of Stock!")
    else:
        st.info("Pehle 'Add Stock' tab mein ja kar saaman add karein.")

with tab3:
    st.header("Sales Report")
    if st.session_state.sales:
        st.table(pd.DataFrame(st.session_state.sales))
        st.metric("Total Today's Sale", f"Rs {sum(s['Total'] for s in st.session_state.sales)}")
    else:
        st.write("No sales yet.")
