# --- Tab 3: Sales Reports ---
with tab3:
    st.subheader("Performance & Sales History")
    
    if st.session_state.sales_history:
        sales_df = pd.DataFrame(st.session_state.sales_history)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total Sales Count", len(sales_df))
        col_m2.metric("Total Revenue", f"Rs {sales_df['Bill Amount'].sum():,.2f}")
        
        st.write("### Recent Transactions")
        st.table(sales_df)
        
        st.write("### Sales Visualization 📊")
        
        # 1️⃣ Total revenue per customer
        revenue_by_customer = sales_df.groupby("Customer")["Bill Amount"].sum()
        st.bar_chart(revenue_by_customer)
        
        # 2️⃣ Sales trend (optional: if we had timestamps, we could plot over time)
        # For now, plot number of items per sale
        st.write("### Items Sold per Transaction")
        items_sold = sales_df["Total Items"]
        st.line_chart(items_sold)
        
        # 3️⃣ Inventory Status Chart
        st.write("### Current Inventory Stock")
        inv_df = st.session_state.inventory.set_index("Item")
        st.bar_chart(inv_df["Stock"])
        
    else:
        st.warning("No sales recorded yet.")
