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
st.markdown("Manage your stock and generate professional bills with automatic discounts.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 Point of Sale",
    "📦 Inventory Manager",
    "📊 Sales Report",
    "🏷️ Shop Settings"
])

# ================= TAB 4 : SHOP SETTINGS =================
with tab4:
    st.subheader("Upload Shop Logo")
    logo = st.file_uploader("Upload Shop Logo", type=["png", "jpg", "jpeg"])
    if logo:
        st.session_state.shop_logo = logo
        st.success("Logo uploaded successfully")
    if st.session_state.shop_logo:
        st.image(st.session_state.shop_logo, width=200)

# ================= TAB 1 : POS =================
with tab1:
    st.subheader("Create New Bill")

    customer = st.text_input("Customer Name")

    items_available = st.session_state.inventory[
        st.session_state.inventory["Stock"] > 0
    ]["Item"].tolist()

    selected_items = st.multiselect("Select Products", items_available)

    subtotal = 0
    purchases = []

    for item in selected_items:
        row = st.session_state.inventory[
            st.session_state.inventory["Item"] == item
        ].iloc[0]

        qty = st.number_input(
            f"Quantity for {item}",
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
        discount = 0
        if subtotal > 50000:
            discount = subtotal * 0.10
            st.info(f"10% Discount Applied: Rs {discount:,.0f}")

        after_discount = subtotal - discount
        gst = after_discount * 0.05
        grand_total = after_discount + gst

        st.subheader(f"Grand Total: Rs {grand_total:,.0f}")

        if st.button("Confirm Purchase"):
            for p in purchases:
                idx = st.session_state.inventory.index[
                    st.session_state.inventory["Item"] == p["Product"]
                ][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]

            st.session_state.invoice_no += 1
            inv_no = f"INV-{st.session_state.invoice_no}"

            st.session_state.sales_history.append({
                "Invoice": inv_no,
                "Customer": customer,
                "Amount": grand_total
            })

            st.session_state.invoice = {
                "Invoice": inv_no,
                "Customer": customer,
                "Date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "Items": purchases,
                "SubTotal": subtotal,
                "Discount": discount,
                "GST": gst,
                "NetTotal": grand_total
            }

            st.success("Invoice Generated Successfully")
            st.balloons()

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    # -------- LOGIN --------
    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            password = st.text_input(
                "🔐 Admin Password",
                type="password",
                placeholder="Enter admin password"
            )
            login = st.form_submit_button("Login")

            if login:
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("✅ Access Granted")
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect Password")

    # -------- AFTER LOGIN --------
    else:
        st.success("🟢 Admin Logged In")

        show_details = st.checkbox("📂 Show Details")

        if show_details:
            st.info("🛠️ Inventory Management Panel")

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
                    else:
                        st.error("Invalid or duplicate product")

            st.markdown("### Edit Inventory")
            for i, row in st.session_state.inventory.iterrows():
                c1, c2, c3, c4 = st.columns([3,2,2,1])
                with c1:
                    n = st.text_input("Name", row["Item"], key=f"n{i}")
                with c2:
                    p = st.number_input("Price", value=row["Price"], step=100, key=f"p{i}")
                with c3:
                    s = st.number_input("Stock", value=row["Stock"], step=1, key=f"s{i}")
                with c4:
                    if st.button("Update", key=f"u{i}"):
                        st.session_state.inventory.at[i, "Item"] = n
                        st.session_state.inventory.at[i, "Price"] = p
                        st.session_state.inventory.at[i, "Stock"] = s
                        st.success("Updated")
                        st.experimental_rerun()

            st.dataframe(st.session_state.inventory, use_container_width=True)

        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.experimental_rerun()

# ================= TAB 3 : SALES REPORT =================
with tab3:
    st.subheader("Sales Report")

    if st.session_state.sales_history:
        df = pd.DataFrame(st.session_state.sales_history)
        st.table(df)

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


