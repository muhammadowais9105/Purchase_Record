# --- Tab 1: Billing System (Point of Sale) ---
with tab1:
    st.subheader("Create New Bill")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter name here...")
        available_items = st.session_state.inventory[st.session_state.inventory["Stock"] > 0]["Item"].tolist()
        selected_items = st.multiselect("Select Products to Buy:", available_items)

    purchases = []
    total_bill = 0

    if selected_items:
        st.write("---")
        for item in selected_items:
            # Get item details
            item_row = st.session_state.inventory[st.session_state.inventory["Item"] == item].iloc[0]
            max_stock = int(item_row["Stock"])
            unit_price = int(item_row["Price"])
            
            # Quantity Input
            qty = st.number_input(f"Quantity for {item} (Available: {max_stock})", min_value=1, max_value=max_stock, key=f"qty_{item}")
            
            subtotal = qty * unit_price
            total_bill += subtotal
            purchases.append({"Item": item, "Qty": qty, "Price": unit_price, "Subtotal": subtotal})

        st.divider()
        
        # --- Discount Logic ---
        final_amount = total_bill
        discount_applied = 0
        
        if total_bill > 50000:
            discount_applied = total_bill * 0.10
            final_amount = total_bill - discount_applied
        
        # --- Display Professional Invoice ---
        if st.button("Generate Professional Invoice"):
            st.markdown("## 🧾 Invoice")
            st.markdown("**ShopMaster Electronics**  \n123 Tech Street, City, Country  \nPhone: +91-1234567890")
            st.markdown(f"**Customer Name:** {customer_name}")
            st.markdown("---")
            
            # Itemized Table
            invoice_df = pd.DataFrame(purchases)
            invoice_df["Price"] = invoice_df["Price"].map("Rs {:,.2f}".format)
            invoice_df["Subtotal"] = invoice_df["Subtotal"].map("Rs {:,.2f}".format)
            st.table(invoice_df)
            
            st.markdown("---")
            st.markdown(f"**Total Amount:** Rs {total_bill:,.2f}")
            if discount_applied > 0:
                st.markdown(f"**Discount Applied:** Rs {discount_applied:,.2f}")
            st.markdown(f"**Final Amount:** Rs {final_amount:,.2f}")
            st.markdown("---")
            st.markdown("Thank you for shopping with **ShopMaster Electronics!** 🎉")
            
            # --- Update Inventory & Record Sale ---
            for p in purchases:
                idx = st.session_state.inventory.index[st.session_state.inventory["Item"] == p["Item"]][0]
                st.session_state.inventory.at[idx, "Stock"] -= p["Qty"]
            
            st.session_state.sales_history.append({
                "Customer": customer_name,
                "Total Items": len(purchases),
                "Bill Amount": final_amount,
                "Items": purchases
            })
            
            st.success("✅ Bill Generated and Stock Updated!")
            st.balloons()
