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
            key=item
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

    # ================= RESPONSIVE CENTER INVOICE =================
    if st.session_state.invoice:
        inv = st.session_state.invoice

        # RESPONSIVE CSS (Desktop + Mobile)
        st.markdown(
            """
            <style>
            .invoice-wrapper {
                display: flex;
                justify-content: center;
                width: 100%;
            }
            .invoice-box {
                width: 100%;
                max-width: 380px;
                padding: 15px;
                border: 1px dashed #777;
                font-family: monospace;
                text-align: center;
            }
            @media (max-width: 600px) {
                .invoice-box {
                    max-width: 95%;
                }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="invoice-wrapper"><div class="invoice-box">', unsafe_allow_html=True)

        if st.session_state.shop_logo:
            st.image(st.session_state.shop_logo, width=90)

        st.markdown("### 🧾 RECEIPT")
        st.markdown("**Electronic Shop**  \nMain Market, Karachi")
        st.markdown("---")

        st.write(f"Invoice #: {inv['Invoice']}")
        st.write(f"Date: {inv['Date']}")
        st.write(f"Customer: {inv['Customer']}")
        st.write("Payment: Cash")

        st.markdown("---")

        st.table(pd.DataFrame(inv["Items"]))

        st.markdown("---")
        st.write(f"Items Sold: {len(inv['Items'])}")
        st.write(f"Sub Total: Rs {inv['SubTotal']:,.0f}")
        st.write(f"Discount: Rs {inv['Discount']:,.0f}")
        st.write(f"GST (5%): Rs {inv['GST']:,.0f}")

        st.markdown(f"### 💰 NET TOTAL: Rs {inv['NetTotal']:,.0f}")

        st.markdown("---")
        st.write("Thank you for shopping with us")
        st.write("Goods once sold will not be returned")

        st.markdown("</div></div>", unsafe_allow_html=True)

# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    with st.expander("Add New Product"):
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
