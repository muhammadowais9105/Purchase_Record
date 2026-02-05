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

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report",
    "🏷️ Shop Settings"
])

# ================= TAB 1 =================
with tab1:
    # 🔴 AUTO LOGOUT when leaving Inventory
    st.session_state.admin_logged_in = False
    st.subheader("Point of Sale")

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            pwd = st.text_input("Admin Password", type="password")
            login = st.form_submit_button("Login")

            if login:
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("Access Granted")
                else:
                    st.error("Wrong Password")
    else:
        st.success("Admin Logged In")

        st.dataframe(st.session_state.inventory, use_container_width=True)

# ================= TAB 3 =================
with tab3:
    # 🔴 AUTO LOGOUT
    st.session_state.admin_logged_in = False
    st.subheader("Sales Report")

# ================= TAB 4 =================
with tab4:
    # 🔴 AUTO LOGOUT
    st.session_state.admin_logged_in = False
    st.subheader("Shop Settings")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Electronic Shop Management System")
