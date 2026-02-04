import streamlit as st
import pandas as pd
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="ShopMaster: Electronic Store",
    page_icon="⚡",
    layout="wide"
)

# --- Initialize Session State ---
if 'inventory' not in st.session_state:
    default_data = {
        "Item": ["Laptop", "Mobile", "TV", "Headphones", "Keyboard"],
        "Price": [85000, 35000, 50000, 2000, 1200],
        "Stock": [10, 20, 15, 50, 40]
    }
    st.session_state.inventory = pd.DataFrame(default_data)

if 'sales_history' not in st.session_state:
    st.session_state.sales_history = []

# --- Header ---
st.title("🏪 Electronic Shop: Management System")
st.markdown("Manage your stock and generate professional bills with automatic discounts.")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report"
])

# -------------------------------------------------
# TAB 1: POINT OF SALE
# -------------------------------------------------
with tab1:
    st.subheader("Create New Bill")

    col1, col2 = st.columns([2, 1])

    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter name here...")
        available_items = st.session_state.inventory[
            st.session_state.inventory["Stock"] > 0
        ]["Item"].tolist()

        selected_items = st.multiselect(
            "Select Products to Buy:",
            available_items
        )

    purchases = []
    total_bill = 0

    if selected_items:
        st.divider()

        for item in selected_items:
            row = st.session_state.inventory[
                st.session_state.inventory["Item"] == item
            ].iloc[0]

            max_stock = int(row["Stock"])
            price = int(row["Price"])

            qty = st.number_input(
                f"Quantity for {item} (Available: {max_stock})",
                min_value=1,
                max_value=max_stock,
                key=f"qty_{item}"
            )

            subtotal = qty * price
            total_bill += subtotal

            purchases.append({
                "Item": item,
                "Qty": qty,
                "Price": price,
                "Subtotal": subtotal
            })

        st.divider()

        discount = 0
        final_amount = total_bill

        if total_bill > 50000:
            discount = total_bill * 0.10
            final_amount -= discount
            st.info(f"🎉 10% Discount Applied: - Rs {discount:,.0f}")

        st.subheader(f"Total Amount: Rs {final_amount:,.0f}")

        if st.button("Confirm Purchase & Print Bill"):
            for p in purchases:
                idx = st.session_state.inventory.index[
                    st.session_state.inventory["Item"] == p["Item"]
                ][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]

            st.session_state.sales_history.append({
                "Customer": customer_name,
                "Total Items": len(purchases),
                "Bill Amount": final_amount
            })

            st.success(f"Bill Generated for {customer_name}")
            st.balloons()

# -------------------------------------------------
# TAB 2: INVENTORY MANAGER
# -------------------------------------------------
with tab2:
    st.subheader("Manage Product Stock")

    with st.expander("➕ Add New Product"):
        c1, c2, c3 = st.columns(3)
        with c1:
            new_name = st.text_input("Product Name")
        with c2:
            new_price = st.number_input("Price", min_value=0)
        with c3:
            new_stock = st.number_input("Stock", min_value=0)

        if st.button("Add Product"):
            if new_name:
                new_row = pd.DataFrame(
                    [[new_name, new_price, new_stock]],
                    columns=["Item", "Price", "Stock"]
                )
                st.session_state.inventory = pd.concat(
                    [st.session_state.inventory, new_row],
                    ignore_index=True
                )
                st.rerun()

    st.write("### Current Inventory")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# -------------------------------------------------
# TAB 3: SALES REPORT + DOWNLOAD
# -------------------------------------------------
with tab3:
    st.subheader("Performance & Sales History")

    if st.session_state.sales_history:
        sales_df = pd.DataFrame(st.session_state.sales_history)

        col1, col2 = st.columns(2)
        col1.metric("Total Sales Count", len(sales_df))
        col2.metric(
            "Total Revenue",
            f"Rs {sales_df['Bill Amount'].sum():,.2f}"
        )

        st.write("### Recent Transactions")
        st.table(sales_df)

        st.divider()
        st.subheader("⬇️ Download Sales Report")

        # CSV DOWNLOAD
        csv = sales_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="sales_report.csv",
            mime="text/csv"
        )

        # EXCEL DOWNLOAD
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            sales_df.to_excel(writer, index=False, sheet_name="Sales Report")

        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="sales_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.warning("No sales recorded yet.")

# --- Footer ---
st.markdown("---")
st.caption("Electronic Shop Management System | Built with Streamlit")
