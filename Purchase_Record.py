# ================= TAB 2 : INVENTORY =================
with tab2:
    st.subheader("Inventory Manager")

    ADMIN_PASSWORD = "admin123"

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password to manage inventory:", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Access Granted! You can now manage inventory.")
                st.experimental_rerun()
            else:
                st.error("Incorrect password! Access denied.")
    else:
        st.info("You are logged in as Admin. You can add new products and adjust stock/price. Renaming allowed.")

        # -------- Add New Product --------
        with st.expander("Add New Product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0, step=100)
            stock = st.number_input("Stock", min_value=0, step=1)

            if st.button("Add Product"):
                if name:
                    if name in st.session_state.inventory["Item"].values:
                        st.error(f"Item '{name}' already exists! Cannot add duplicate.")
                    else:
                        st.session_state.inventory.loc[len(st.session_state.inventory)] = [
                            name, price, stock
                        ]
                        st.success(f"Product '{name}' added successfully!")
                        st.experimental_rerun()

        # -------- Editable Inventory Table --------
        st.markdown("### Current Inventory")
        for i, row in st.session_state.inventory.iterrows():
            col1, col2, col3, col4 = st.columns([3,2,2,1])
            with col1:
                new_name = st.text_input(f"Rename Item {i}", row["Item"], key=f"name_{i}")
            with col2:
                new_price = st.number_input(f"Price {i}", min_value=0, step=100, value=row["Price"], key=f"price_{i}")
            with col3:
                new_stock = st.number_input(f"Stock {i}", min_value=0, step=1, value=row["Stock"], key=f"stock_{i}")
            with col4:
                if st.button(f"Update {i}"):
                    # Update inventory
                    st.session_state.inventory.at[i, "Item"] = new_name
                    st.session_state.inventory.at[i, "Price"] = new_price
                    st.session_state.inventory.at[i, "Stock"] = new_stock
                    st.success(f"Item '{new_name}' updated!")
                    st.experimental_rerun()

        # Show inventory table
        st.dataframe(st.session_state.inventory, use_container_width=True)

        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.experimental_rerun()
