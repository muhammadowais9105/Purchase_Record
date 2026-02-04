import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Electronic Shop: Management System",
    page_icon="⚡",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item": ["Laptop", "Mobile", "TV", "Headphones", "Keyboard"],
        "Price": [85000, 35000, 50000, 2000, 1200],
        "Stock": [10, 20, 15, 50, 40]
    })

if "sales_history" not in st.session_state:
    st.session_state.sales_history = []

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")
st.markdown("Manage your stock and generate professional bills with automatic discounts.")

tab1, tab2, tab3 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report"
])

# ================= TAB 1 : POS =================
with tab1:
    st.subheader("Create New Bill")

    customer = st.text_input("Customer Name")

    items_available = st.session_state.inventory[
        st.session_state.inventory["Stock"] > 0
    ]["Item"].tolist()

    selected_items = st.multiselect("Select Products", items_available)

    total_bill = 0
    purchases = []

    for item in selected_items:
        row = st.session_state.inventory[
            st.session_state.inventory["Item"] == item
        ].iloc[0]

        qty = st.number_input(
            f"Quantity for {item}",
            min_value=1,
            max_value=int(row["Stock"]),
            key=item
        )

        subtotal = qty * row["Price"]
        total_bill += subtotal

        purchases.append({"Item": item, "Qty": qty})

    if total_bill > 0:
        discount = 0
        if total_bill > 50000:
            discount = total_bill * 0.10
            total_bill -= discount
            st.info(f"🎉 10% Discount Applied: Rs {discount:,.0f}")

        st.subheader(f"Final Bill: Rs {total_bill:,.0f}")

        if st.button("Confirm Purchase"):
            for p in purchases:
                idx = st.session_state.inventory.index[
                    st.session_state.inventory["Item"] == p["Item"]
                ][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]

            st.session_state.sales_history.append({
                "Customer": customer,
                "Total Items": len(purchases),
                "Bill Amount": total_bill
            })

            st.success("Bill Generated Successfully 🎉")
            st.balloons()

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    with st.expander("➕ Add New Product"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0)
        stock = st.number_input("Stock", min_value=0)

        if st.button("Add Product"):
            if name:
                st.session_state.inventory.loc[len(st.session_state.inventory)] = [
                    name, price, stock
                ]
                st.rerun()

    st.dataframe(st.session_state.inventory, use_container_width=True)

# ================= TAB 3 : SALES REPORT =================
with tab3:
    st.subheader("Performance & Sales History")

    if st.session_state.sales_history:
        sales_df = pd.DataFrame(st.session_state.sales_history)

        c1, c2 = st.columns(2)
        c1.metric("Total Sales", len(sales_df))
        c2.metric("Total Revenue", f"Rs {sales_df['Bill Amount'].sum():,.0f}")

        st.write("### Recent Transactions")
        st.table(sales_df)

        # -------- CSV DOWNLOAD (ERROR FREE) --------
        csv = sales_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Sales Report (CSV)",
            csv,
            "sales_report.csv",
            "text/csv"
        )

    else:
        st.info("No sales data available")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Electronic Shop Management System | Streamlit App")
