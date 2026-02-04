import streamlit as st
from fpdf import FPDF
import base64

# --- Page Config ---
st.set_page_config(page_title="Electronic Shop", page_icon="🛒")

# Custom CSS for the Beautiful Invoice Box
st.markdown("""
    <style>
    .bill-box {
        border: 2px solid #2E7D32;
        border-radius: 15px;
        padding: 25px;
        background-color: #ffffff;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        color: #1E1E1E;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .total-text {
        font-size: 24px;
        font-weight: bold;
        color: #2E7D32;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Variables ---
shop_name = "Electronic Shop"
shop_city = "Karachi"

# Products Data
products = {
    "laptop": 85000, "mobile": 35000, "tv": 50000,
    "headphones": 2000, "keyboard": 1200, "mouse": 700,
    "fan": 4000, "iron": 2500, "speaker": 3000,
    "charger": 900, "camera": 60000, "washing_machine": 55000
}

st.title(f"🏪 Welcome to {shop_name}")
st.write(f"📍 Location: **{shop_city}**")

# --- Selection Section ---
st.divider()
st.subheader("🛍️ Select Your Products")
selected_items = st.multiselect("Pick items from the list:", list(products.keys()))

purchases = {}
if selected_items:
    cols = st.columns(2)
    for i, item in enumerate(selected_items):
        with cols[i % 2]:
            qty = st.number_input(f"Qty for {item.title()}:", min_value=1, value=1, key=item)
            purchases[item] = qty

# --- PDF Generation Function ---
def create_pdf(pur_dict, total, discount, final):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{shop_name} - Invoice", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Location: {shop_city}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(100, 10, txt="Item", border=1)
    pdf.cell(40, 10, txt="Qty", border=1)
    pdf.cell(50, 10, txt="Price (Rs)", border=1, ln=True)
    
    for item, qty in pur_dict.items():
        pdf.cell(100, 10, txt=item.title(), border=1)
        pdf.cell(40, 10, txt=str(qty), border=1)
        pdf.cell(50, 10, txt=f"{products[item]*qty:,}", border=1, ln=True)
    
    pdf.ln(5)
    if discount > 0:
        pdf.cell(200, 10, txt=f"Discount: -Rs {discount:,}", ln=True, align='R')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Final Total: Rs {final:,}", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# --- Generate Bill Button Logic ---
if st.button("🚀 Generate Beautiful Bill"):
    if not purchases:
        st.error("Please select at least one item first!")
    else:
        # Calculations
        total_raw = sum(products[item] * qty for item, qty in purchases.items())
        discount = total_raw * 0.10 if total_raw > 50000 else 0
        final_amount = total_raw - discount

        # 1. Display the Beautiful Box
        st.markdown('<div class="bill-box">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>📄 INVOICE</h2>", unsafe_allow_html=True)
        
        for item, qty in purchases.items():
            cost = products[item] * qty
            st.write(f"**{item.title()}** × {qty} <span style='float:right;'>Rs {cost:,}</span>", unsafe_allow_html=True)
        
        st.divider()
        if discount > 0:
            st.write(f"✨ Discount Applied: <span style='float:right; color:red;'>-Rs {discount:,}</span>", unsafe_allow_html=True)
        
        st.markdown(f'<p class="total-text">Final Amount: Rs {final_amount:,}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Add Download Button
        pdf_data = create_pdf(purchases, total_raw, discount, final_amount)
        st.download_button(
            label="📥 Download PDF Invoice",
            data=pdf_data,
            file_name="invoice.pdf",
            mime="application/pdf"
        )
