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

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "invoice_no" not in st.session_state:
    st.session_state.invoice_no = 1000

if "shop_logo" not in st.session_state:
    st.session_state.shop_logo = None

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🛒 POS", "📦 Inventory", "📊 Sales", "🏷️ Settings"]
)

# ================= SETTINGS =================
with tab4:
    logo = st.file_uploader("Upload Shop Logo", type=["png", "jpg", "jpeg"])
    if logo:
        st.session_state.shop_logo = logo
        st.success("Logo Uploaded")

# ================= POS =================
with tab1:
    customer = st.text_input("Customer Name")

    items = st.session_state.inventory[
        st.session_state.inventory["Stock"] > 0
    ]["Item"].tolist()

    selected = st.multiselect("Select Products", items)

    subtotal = 0
    purchases = []

    for item in selected:
        row = st.session_state.inventory[
            st.session_state.inventory["Item"] == item
        ].iloc[0]

        qty = st.number_input(
            f"Qty for {item}", 1, int(row["Stock"]), key=item
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
        discount = subtotal * 0.1 if subtotal > 50000 else 0
        gst = (subtotal - discount) * 0.05
        grand = subtotal - discount + gst

        if st.button("Confirm Purchase"):
            st.session_state.invoice_no += 1
            st.session_state.invoice = {
                "Invoice": f"INV-{st.session_state.invoice_no}",
                "Customer": customer,
                "Date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "Items": purchases,
                "SubTotal": subtotal,
                "Discount": discount,
                "GST": gst,
                "NetTotal": grand
            }

    # ================= RECEIPT + AUTO PDF =================
    if st.session_state.invoice:
        inv = st.session_state.invoice

        st.markdown(
            """
            <style>
            .invoice-wrap{display:flex;justify-content:center}
            .invoice{
                max-width:380px;
                width:100%;
                padding:15px;
                border:1px dashed #555;
                text-align:center;
                font-family:monospace;
            }
            @media print{
                body *{visibility:hidden}
                .invoice,.invoice *{visibility:visible}
                .invoice{position:absolute;left:50%;transform:translateX(-50%)}
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="invoice-wrap"><div class="invoice">', unsafe_allow_html=True)

        if st.session_state.shop_logo:
            st.image(st.session_state.shop_logo, width=90)

        st.markdown("### 🧾 RECEIPT")
        st.write(f"Invoice: {inv['Invoice']}")
        st.write(f"Date: {inv['Date']}")
        st.write(f"Customer: {inv['Customer']}")
        st.markdown("---")

        st.table(pd.DataFrame(inv["Items"]))

        st.markdown("---")
        st.write(f"Subtotal: Rs {inv['SubTotal']:,.0f}")
        st.write(f"Discount: Rs {inv['Discount']:,.0f}")
        st.write(f"GST: Rs {inv['GST']:,.0f}")
        st.markdown(f"### 💰 NET TOTAL: Rs {inv['NetTotal']:,.0f}")

        st.markdown("---")
        st.write("Thank you for shopping with us")

        # AUTO PDF PRINT BUTTON
        st.markdown(
            """
            <button onclick="
                setTimeout(()=>{window.print();},200);
            " style="
                margin-top:10px;
                padding:10px 20px;
                font-size:16px;
                background:#198754;
                color:white;
                border:none;
                border-radius:5px;
                cursor:pointer;">
                📄 Print / Save PDF
            </button>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div></div>", unsafe_allow_html=True)

# ================= INVENTORY =================
with tab2:
    st.dataframe(st.session_state.inventory)

# ================= SALES =================
with tab3:
    if st.session_state.sales_history:
        st.table(pd.DataFrame(st.session_state.sales_history))
