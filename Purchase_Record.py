import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Electronic Shop POS",
    page_icon="🧾",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item": ["Laptop", "Mobile", "TV"],
        "Price": [85000, 35000, 50000],
        "Stock": [10, 20, 15]
    })

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "invoice_no" not in st.session_state:
    st.session_state.invoice_no = 17128

if "logo" not in st.session_state:
    st.session_state.logo = None

# ---------------- RECEIPT FUNCTION ----------------
def show_receipt(inv, logo_base64=None):
    html = f"""
    <div style="
        width:300px;
        margin:auto;
        font-family:monospace;
        border:1px dashed black;
        padding:10px;
        background:#fff;
    ">
        <h3 style="text-align:center;">SALE INVOICE</h3>

        {"<div style='text-align:center;'><img src='data:image/png;base64,"+logo_base64+"' width='120'></div>" if logo_base64 else ""}

        <p style="text-align:center;">
        <b>ELECTRONIC SHOP</b><br>
        Main Market, Karachi<br>
        Ph: 0300-1234567
        </p>

        <hr>

        <p>
        Invoice #: {inv['Invoice No']}<br>
        Date: {inv['Date']}<br>
        Customer: {inv['Customer']}
        </p>

        <hr>

        <table width="100%">
            <tr>
                <th align="left">Item</th>
                <th>Qty</th>
                <th align="right">Total</th>
            </tr>
    """

    for i in inv["Items"]:
        html += f"""
        <tr>
            <td>{i['Item']}</td>
            <td align="center">{i['Qty']}</td>
            <td align="right">{i['Total']}</td>
        </tr>
        """

    html += f"""
        </table>

        <hr>

        <p>
        Sub Total: {inv['Sub Total']}<br>
        GST (5%): {inv['GST']}<br>
        Discount: {inv['Discount']}
        </p>

        <h3 style="text-align:center;">
        NET TOTAL: Rs {inv['Grand Total']}
        </h3>

        <hr>

        <p style="text-align:center;">
        Payment: Cash<br>
        Thank you for shopping!
        </p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🧾 Electronic Shop POS System")

tab1, tab2 = st.tabs(["🛒 POS", "⚙️ Settings"])

# ---------------- SETTINGS ----------------
with tab2:
    st.subheader("Shop Logo")
    logo = st.file_uploader("Upload Logo", type=["png", "jpg"])
    if logo:
        st.session_state.logo = base64.b64encode(logo.read()).decode()

# ---------------- POS ----------------
with tab1:
    customer = st.text_input("Customer Name")

    items = st.multiselect(
        "Select Items",
        st.session_state.inventory["Item"].tolist()
    )

    purchases = []
    subtotal = 0

    for item in items:
        row = st.session_state.inventory[
            st.session_state.inventory["Item"] == item
        ].iloc[0]

        qty = st.number_input(
            f"Qty for {item}",
            1, int(row["Stock"])
        )

        total = qty * row["Price"]
        subtotal += total

        purchases.append({
            "Item": item,
            "Qty": qty,
            "Total": total
        })

    if subtotal > 0:
        gst = int(subtotal * 0.05)
        discount = int(subtotal * 0.10) if subtotal > 50000 else 0
        grand_total = subtotal + gst - discount

        st.write(f"**Payable: Rs {grand_total}**")

        if st.button("Confirm Order"):
            st.session_state.invoice_no += 1

            st.session_state.invoice = {
                "Invoice No": f"INV-{st.session_state.invoice_no}",
                "Customer": customer,
                "Date": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
                "Items": purchases,
                "Sub Total": subtotal,
                "GST": gst,
                "Discount": discount,
                "Grand Total": grand_total
            }

            st.success("Order Confirmed ✔️")

    # -------- SHOW RECEIPT --------
    if st.session_state.invoice:
        st.markdown("### 🧾 Receipt")
        show_receipt(
            st.session_state.invoice,
            st.session_state.logo
        )
