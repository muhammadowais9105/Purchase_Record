import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="ShopMaster: Electronic Store", page_icon="⚡", layout="wide")

# --- Initialize Session State (Data Storage) ---
if 'inventory' not in st.session_state:
    # Default products from your first code
    default_data = {
        "Item": ["Laptop", "Mobile", "TV", "Headphones", "Keyboard"],
        "Price": [85000, 35000, 50000, 2000, 1200],
        "Stock": [10, 20, 15, 50, 40]
    }
    st.session_state['inventory'] = pd.DataFrame(default_data)

if 'sales_history' not in st.session_state:
    st.session_state['sales_history'] = []

# --- Header Section ---
st.title("🏪 Electronic Shop: Management System")
st.markdown("Manage your stock and generate professional bills with automatic discounts.")

# --- Tabs for Organization ---
tab1, tab2, tab3 = st.tabs(["🛒 Point of Sale", "📦 Inventory Manager", "📊 Sales Report"])

# --- Tab 1: Billing System (Point of Sale) ---
with tab1:
    st.subheader("Create New Bill")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter name here...")
        available_items = st.session_state.inventory[st.session_state.inventory["Stock"] > 0]["Item"].tolist()
        selected_items = st.multiselect("Select Products to Buy:", available_items)

    purchases = []
    total_bill = 0

    if selected_items:
        st.write("---")
        for item in selected_items:
            # Get item details
            item_row = st.session_state.inventory[st.session_state.inventory["Item"] == item].iloc[0]
            max_stock = int(item_row["Stock"])
            unit_price = int(item_row["Price"])
            
            # Quantity Input
            qty = st.number_input(f"Quantity for {item} (Available: {max_stock})", min_value=1, max_value=max_stock, key=f"qty_{item}")
            
            subtotal = qty * unit_price
            total_bill += subtotal
            purchases.append({"Item": item, "Qty": qty, "Price": unit_price, "Subtotal": subtotal})

        st.divider()
        
        # --- Discount Logic ---
        final_amount = total_bill
        discount_applied = 0
        
        if total_bill > 50000:
            discount_applied = total_bill * 0.10
            final_amount = total_bill - discount_applied
            st.info(f"🎉 10% Discount Applied: -Rs {discount_applied}")
        
        st.subheader(f"Total Amount: Rs {final_amount}")

        if st.button("Confirm Purchase & Print Bill"):
            # Update Inventory Stock
            for p in purchases:
                idx = st.session_state.inventory.index[st.session_state.inventory["Item"] == p["Item"]][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]
            
            # Record Sale
            st.session_state.sales_history.append({
                "Customer": customer_name,
                "Total Items": len(purchases),
                "Bill Amount": final_amount
            })
            
            st.success(f"Bill Generated for {customer_name}! Stock updated.")
            st.balloons()

# --- Tab 2: Inventory Management ---
with tab2:
    st.subheader("Manage Product Stock")
    
    # Add New Product Form
    with st.expander("➕ Add New Product to Shop"):
        new_col1, new_col2, new_col3 = st.columns(3)
        with new_col1: new_name = st.text_input("Product Name")
        with new_col2: new_price = st.number_input("Selling Price", min_value=0)
        with new_col3: new_stock = st.number_input("Initial Stock", min_value=0)
        
        if st.button("Update Inventory List"):
            if new_name:
                new_row = pd.DataFrame([[new_name, new_price, new_stock]], columns=["Item", "Price", "Stock"])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.rerun()

    st.write("### Current Stock Status")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- Tab 3: Sales Reports ---
with tab3:
    st.subheader("Performance & Sales History")
    
    if st.session_state.sales_history:
        sales_df = pd.DataFrame(st.session_state.sales_history)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Sales Count", len(sales_df))
        col_m2.metric("Total Revenue", f"Rs {sales_df['Bill Amount'].sum():,.2f}")
        
        st.write("### Recent Transactions")
        st.table(sales_df)
    else:
        st.warning("No sales recorded yet.")

# --- Footer ---
st.markdown("---")
st.caption("Electronic Shop Management System | Built with Streamlit")
