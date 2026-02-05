import streamlit as st
import pandas as pd
from datetime import datetime

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

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "show_details" not in st.session_state:
    st.session_state.show_details = False

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")

tab1, tab2, tab3 = st.tabs([
    "🛒 POS",
    "📦 Inventory Manager",
    "📊 Sales Report"
])

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    # ---------- LOGIN ----------
    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            password = st.text_input(
                "Enter Admin Password",
                type="password",
                key="admin_password"
            )
            login = st.form_submit_button("Login")

            if login:
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True

                    # 🔥 PASSWORD COMPLETELY REMOVE
                    del st.session_state["admin_password"]

                    st.success("✅ Login Successful")
                    st.experimental_rerun()
                else:
                    st.error("❌ Wrong Password")

    # ---------- AFTER LOGIN ----------
    else:
        st.success("🟢 Admin Logged In")

        # 🔹 DETAILS OPTION (ONLY AFTER LOGIN)
        if st.button("📂 Open Details"):
            st.session_state.show_details = True

        # ---------- DETAILS PANEL ----------
        if st.session_state.show_details:
            st.info("🛠️ Inventory Details")

            with st.expander("➕ Add New Product"):
                name = st.text_input("Product Name")
                price = st.number_input("Price", min_value=0, step=100)
                stock = st.number_input("Stock", min_value=0, step=1)

                if st.button("Add Product"):
                    if name and name not in st.session_state.inventory["Item"].values:
                        st.session_state.inventory.loc[len(st.session_state.inventory)] = [
                            name, price, stock
                        ]
                        st.success("Product Added")
                        st.experimental_rerun()

            st.markdown("### Current Inventory")
            st.dataframe(st.session_state.inventory, use_container_width=True)

        # ---------- LOGOUT ----------
        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.session_state.show_details = False
            st.experimental_rerun()

# ================= TAB 3 : SALES REPORT =================
with tab3:
    if st.session_state.sales_history:
        st.dataframe(pd.DataFrame(st.session_state.sales_history))
    else:
        st.info("No sales data yet")
