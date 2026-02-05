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
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item": ["Laptop", "Mobile", "TV", "Headphones", "Keyboard"],
        "Price": [85000, 35000, 50000, 2000, 1200],
        "Stock": [10, 20, 15, 50, 40]
    })

if "sales_history" not in st.session_state:
    st.session_state.sales_history = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "invoice_no" not in st.session_state:
    st.session_state.invoice_no = 1000

if "shop_logo" not in st.session_state:
    st.session_state.shop_logo = None

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "🛒 Point of Sale"

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")

# ---------------- TAB SELECTOR ----------------
tab = st.radio(
    "Navigation",
    ["🛒 Point of Sale", "📦 Inventory Manager", "📊 Sales Report", "🏷️ Shop Settings"],
    horizontal=True
)

# -------- AUTO LOGOUT WHEN TAB CHANGES --------
if tab != "📦 Inventory Manager":
    st.session_state.admin_logged_in = False

# ================= POS =================
if tab == "🛒 Point of Sale":
    st.subheader("Create New Bill")
    st.write("POS working normally")

# ================= INVENTORY =================
elif tab == "📦 Inventory Manager":
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    if not st.session_state.admin_logged_in:
        with st.form("login"):
            pwd = st.text_input("Admin Password", type="password")
            login = st.form_submit_button("Login")

            if login:
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("Access Granted")
                    st.stop()
                else:
                    st.error("Wrong password")

    else:
        st.success("Admin Logged In")

        with st.expander("Add Product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0)
            stock = st.number_input("Stock", min_value=0)

            if st.button("Add"):
                st.session_state.inventory.loc[len(st.session_state.inventory)] = [
                    name, price, stock
                ]
                st.success("Product Added")

        st.dataframe(st.session_state.inventory, use_container_width=True)

# ================= SALES =================
elif tab == "📊 Sales Report":
    st.subheader("Sales Report")
    st.write("Sales data here")

# ================= SETTINGS =================
elif tab == "🏷️ Shop Settings":
    st.subheader("Shop Settings")
    logo = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    if logo:
        st.image(logo, width=200)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Electronic Shop Management System")
