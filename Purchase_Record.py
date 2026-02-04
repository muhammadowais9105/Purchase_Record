import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

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

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "invoice_no" not in st.session_state:
    st.session_state.invoice_no = 1000

# ---------------- HEADER ----------------
st.title("🏪 Electronic Shop: Management System")

# ================= POS =================
customer = st.text_input("Customer Name")

items = st.session_state.inventory["Item"].tolist()
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
    discount = subtotal * 0.10 if subtotal > 50000 else 0
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

    st.markdown("### 🧾 RECEIPT")
    st.table(pd.DataFrame(inv["Items"]))
    st.markdown(f"### 💰 Net Total: Rs {inv['NetTotal']:,.0f}")

    # -------- PDF GENERATION --------
    def generate_pdf(invoice):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, y, "ELECTRONIC SHOP RECEIPT")

        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Invoice #: {invoice['Invoice']}")
        y -= 15
        c.drawString(50, y, f"Customer: {invoice['Customer']}")
        y -= 15
        c.drawString(50, y, f"Date: {invoice['Date']}")

        y -= 30
        c.drawString(50, y, "Item")
        c.drawString(200, y, "Qty")
        c.drawString(250, y, "Price")
        c.drawString(330, y, "Total")

        y -= 10
        c.line(50, y, 550, y)

        for item in invoice["Items"]:
            y -= 20
            c.drawString(50, y, item["Product"])
            c.drawString(200, y, str(item["Qty"]))
            c.drawString(250, y, str(item["Price"]))
            c.drawString(330, y, str(item["Total"]))

        y -= 30
        c.drawString(50, y, f"Subtotal: Rs {invoice['SubTotal']:,.0f}")
        y -= 15
        c.drawString(50, y, f"Discount: Rs {invoice['Discount']:,.0f}")
        y -= 15
        c.drawString(50, y, f"GST: Rs {invoice['GST']:,.0f}")
        y -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"NET TOTAL: Rs {invoice['NetTotal']:,.0f}")

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf_file = generate_pdf(inv)

    # -------- DOWNLOAD BUTTON --------
    st.download_button(
        label="🖨️ Print Receipt (Download PDF)",
        data=pdf_file,
        file_name=f"{inv['Invoice']}.pdf",
        mime="application/pdf"
    )
