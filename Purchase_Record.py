import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Electronic Shop: Management System",
    page_icon="⚡",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault(
    "inventory",
    pd.DataFrame({
        "Item": ["Laptop", "Mobile", "TV", "Headphones", "Keyboard"],
        "Price": [85000, 35000, 50000, 2000, 1200],
        "Stock": [10, 20, 15, 50, 40]
    })
)
st.session_state.setdefault("sales_history", [])
st.session_state.setdefault("invoice", None)
st.session_state.setdefault("invoice_no", 1000)
st.session_state.setdefault("shop_logo", None)
st.session_state.setdefault("admin_logged_in", False)
st.session_state.setdefault("active_tab", "🛒 Point of Sale")

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")
st.markdown("Manage your stock and generate professional bills.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report",
    "🏷️ Shop Settings"
])

# ================= TAB 1 : POS =================
with tab1:
    if st.session_state.active_tab == "📦 Inventory Manager":
        st.session_state.admin_logged_in = False
    st.session_state.active_tab = "🛒 Point of Sale"

    st.subheader("Create New Bill")
    customer = st.text_input("Customer Name")

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.session_state.active_tab = "📦 Inventory Manager"
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            pwd = st.text_input("Admin Password", type="password")
            login = st.form_submit_button("Login")

            if login:
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("Admin Logged In")
                else:
                    st.error("Wrong Password")
    else:
        st.success("Admin Mode Active")

        with st.expander("Add New Product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0, step=100)
            stock = st.number_input("Stock", min_value=0, step=1)

            if st.button("Add Product"):
                if name and name not in st.session_state.inventory["Item"].values:
                    st.session_state.inventory.loc[
                        len(st.session_state.inventory)
                    ] = [name, price, stock]
                    st.success("Product Added")

        st.dataframe(st.session_state.inventory, use_container_width=True)

# ================= TAB 3 : SALES REPORT =================
with tab3:
    if st.session_state.active_tab == "📦 Inventory Manager":
        st.session_state.admin_logged_in = False
    st.session_state.active_tab = "📊 Sales Report"

    st.subheader("Sales Report")
    if st.session_state.sales_history:
        df = pd.DataFrame(st.session_state.sales_history)
        st.table(df)
    else:
        st.info("No sales yet")

# ================= TAB 4 : SHOP SETTINGS =================
with tab4:
    if st.session_state.active_tab == "📦 Inventory Manager":
        st.session_state.admin_logged_in = False
    st.session_state.active_tab = "🏷️ Shop Settings"

    st.subheader("Upload Shop Logo")
    logo = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    if logo:
        st.session_state.shop_logo = logo
        st.success("Logo uploaded")

    if st.session_state.shop_logo:
        st.image(st.session_state.shop_logo, width=200)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Electronic Shop Management System | Streamlit App")
