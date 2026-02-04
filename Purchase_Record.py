import streamlit as st
from streamlit_sortable import sortable_list  # pip install streamlit-sortable

# Products
products = ["Laptop", "Mobile", "TV", "Headphones", "Keyboard", "Mouse", "Fan", "Iron"]

st.subheader("🛒 Drag & Drop to select products in order")

# Create draggable sortable list
selected_items = sortable_list(products, direction="vertical")

st.write("Selected Items (in order):", selected_items)

# Quantity input for each item
purchases = {}
if selected_items:
    for item in selected_items:
        qty = st.number_input(f"Quantity for {item}:", min_value=1, value=1, key=item)
        purchases[item] = qty

st.write("Purchase record:", purchases)
