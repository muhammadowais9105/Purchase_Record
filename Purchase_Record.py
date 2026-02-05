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

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")
st.markdown("Manage your stock and generate professional bills.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report",
    "🏷️ Shop Settings"
])

# ================= TAB 4 : SHOP SETTINGS =================
with tab4:
    st.subheader("Upload Shop Logo")
    logo = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    if logo:
        st.session_state.shop_logo = logo
        st.success("Logo uploaded")

    if st.session_state.shop_logo:
        st.image(st.session_state.shop_logo, width=180)

# ================= TAB 1 : POS =================
with tab1:
    st.subheader("Create New Bill")

    customer = st.text_input("Customer Name")

    available = st.session_state.inventory[
        st.session_state.inventory["Stock"] > 0
    ]

    selected_items = st.multiselect(
        "Select Products",
        available["Item"].tolist()
    )

    subtotal = 0
    purchases = []

    for item in selected_items:
        row = available[available["Item"] == item].iloc[0]

        qty = st.number_input(
            f"Quantity - {item}",
            min_value=1,
            max_value=int(row["Stock"]),
            key=f"qty_{item}"
        )

        total = qty * row["Price"]
        subtotal += total

        purchases.append({
            "Product": item,
            "Qty": qty,
            "Price": row["Price"],
            "Total": total
        })

    if subtotal > 0:
        discount = subtotal * 0.10 if subtotal > 50000 else 0
        gst = (subtotal - discount) * 0.05
        grand_total = subtotal - discount + gst

        st.success(f"Grand Total: Rs {grand_total:,.0f}")

        if st.button("Confirm Purchase"):
            for p in purchases:
                idx = st.session_state.inventory.index[
                    st.session_state.inventory["Item"] == p["Product"]
                ][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]

            st.session_state.invoice_no += 1
            inv_no = f"INV-{st.session_state.invoice_no}"

            st.session_state.invoice = {
                "Invoice": inv_no,
                "Customer": customer,
                "Date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "Items": purchases,
                "NetTotal": grand_total
            }

            st.session_state.sales_history.append({
                "Invoice": inv_no,
                "Customer": customer,
                "Amount": grand_total
            })

            st.balloons()

    if st.session_state.invoice:
        inv = st.session_state.invoice
        st.markdown("### 🧾 Invoice")
        st.write(f"Invoice #: {inv['Invoice']}")
        st.write(f"Customer: {inv['Customer']}")
        st.write(f"Date: {inv['Date']}")
        st.table(pd.DataFrame(inv["Items"]))
        st.success(f"Net Total: Rs {inv['NetTotal']:,.0f}")

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    # -------- LOGIN --------
    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            pwd = st.text_input("Enter Admin Password", type="password")
            login = st.form_submit_button("Login")

            if login:
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("Access Granted")
                else:
                    st.error("Incorrect password")

    # -------- ADMIN PANEL --------
    else:
        st.info("Admin Mode Active")

        with st.expander("➕ Add New Product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0, step=100)
            stock = st.number_input("Stock", min_value=0, step=1)

            if st.button("Add Product"):
                if name:
                    st.session_state.inventory.loc[
                        len(st.session_state.inventory)
                    ] = [name, price, stock]
                    st.success("Product added")

        st.markdown("### 🛠️ Edit Inventory")

        for i, row in st.session_state.inventory.iterrows():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 1])

            with c1:
                new_name = st.text_input("Item", row["Item"], key=f"name_{i}")
            with c2:
                new_price = st.number_input("Price", value=row["Price"], key=f"price_{i}")
            with c3:
                new_stock = st.number_input("Stock", value=row["Stock"], key=f"stock_{i}")
            with c4:
                if st.button("Update", key=f"update_{i}"):
                    st.session_state.inventory.loc[i] = [
                        new_name, new_price, new_stock
                    ]
                    st.success("Updated")

        st.dataframe(st.session_state.inventory, use_container_width=True)

        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False

# ================= TAB 3 : SALES REPORT =================
with tab3:
    st.subheader("Sales Report")

    if st.session_state.sales_history:
        df = pd.DataFrame(st.session_state.sales_history)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            "sales_report.csv",
            "text/csv"
        )
    else:
        st.info("No sales data yet")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Electronic Shop Management System | Streamlit App")
