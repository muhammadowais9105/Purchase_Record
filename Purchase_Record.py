import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import io
import random

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop Invoice", page_icon="🧾")

# --- Shop Info ---
shop_name = "Electronic Shop"
shop_city = "Karachi"

st.title("🏪 Electronic Shop")
st.caption("📍 Karachi")

# --- Customer Info ---
st.subheader("👤 Customer Details")
customer_name = st.text_input("Customer Name")

payment_method = st.selectbox(
    "Payment Method",
    ["Cash", "Credit Card", "Debit Card", "JazzCash", "EasyPaisa"]
)

# --- Products ---
products = {
    "Laptop": 85000,
    "Mobile": 35000,
    "TV": 50000,
    "Headphones": 2000,
    "Keyboard": 1200,
    "Mouse": 700,
    "Fan": 4000,
}

st.divider()
st.subheader("🛍️ Select Products")

selected_items = st.multiselect("Products:", products.keys())
purchases = {}

if selected_items:
    for item in selected_items:
        qty = st.number_input(
            f"Quantity for {item}",
            min_value=1,
            value=1,
            key=item
        )
        purchases[item] = qty


# --- PDF Invoice Generator ---
def generate_pdf_invoice(customer, payment, purchases):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, shop_name)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 70, f"Location: {shop_city}")

    invoice_no = random.randint(1000, 9999)
    date = datetime.now().strftime("%d-%m-%Y")

    pdf.drawRightString(width - 50, height - 50, f"Invoice #: {invoice_no}")
    pdf.drawRightString(width - 50, height - 70, f"Date: {date}")

    # Customer
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 110, "Bill To:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 130, customer)

    # Table Header
    y = height - 170
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Product")
    pdf.drawString(250, y, "Qty")
    pdf.drawString(320, y, "Price")
    pdf.drawString(420, y, "Total")

    pdf.line(50, y - 5, width - 50, y - 5)

    # Table Content
    pdf.setFont("Helvetica", 11)
    total_amount = 0
    y -= 25

    for item, qty in purchases.items():
        price = products[item]
        cost = price * qty
        total_amount += cost

        pdf.drawString(50, y, item)
        pdf.drawString(250, y, str(qty))
        pdf.drawString(320, y, f"Rs {price}")
        pdf.drawString(420, y, f"Rs {cost}")
        y -= 20

    # Discount
    discount = total_amount * 0.10 if total_amount > 50000 else 0
    final_amount = total_amount - discount

    # Summary
    y -= 20
    pdf.line(300, y, width - 50, y)
    y -= 20

    pdf.drawRightString(width - 50, y, f"Subtotal: Rs {total_amount}")
    y -= 20
    pdf.drawRightString(width - 50, y, f"Discount: Rs {int(discount)}")
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(width - 50, y, f"Final Amount: Rs {int(final_amount)}")

    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Payment Method: {payment}")

    # Footer
    pdf.drawCentredString(width / 2, 40, "Thank you for shopping with us!")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer


# --- Generate Invoice ---
if st.button("🧾 Generate PDF Invoice"):
    if not customer_name:
        st.warning("Please enter customer name")
    elif not purchases:
        st.warning("Please select at least one product")
    else:
        pdf_file = generate_pdf_invoice(
            customer_name,
            payment_method,
            purchases
        )

        st.success("Invoice generated successfully!")

        st.download_button(
            label="📥 Download Invoice (PDF)",
            data=pdf_file,
            file_name=f"{customer_name}_invoice.pdf",
            mime="application/pdf"
        )
