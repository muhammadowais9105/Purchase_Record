import streamlit as st
import pandas as pd
from io import BytesIO

# --- Page Config ---
st.set_page_config(page_title="ShopMaster Analytics", page_icon="📊", layout="wide")

# --- INITIALIZE DATA ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame()
if 'ledger' not in st.session_state:
    st.session_state.ledger = pd.DataFrame(columns=["Timestamp", "Type", "Details", "Amount", "Profit"])
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Timestamp", "Category", "Amount"])

# --- SECURITY ---
def check_password():
    if not st.session_state.authenticated:
        st.title("🛡️ ShopMaster Secure Login")
        with st.container(border=True):
            user_pwd = st.text_input("Enter Admin Password", type="password")
            if st.button("Access System", use_container_width=True):
                if user_pwd == "123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Password")
        return False
    return True

if check_password():
    st.sidebar.title("🚀 ShopMaster 2026")
    menu = st.sidebar.radio("Navigate", ["Connection Center", "Sell (POS)", "Buy (Restock)", "Expenses", "Profit & Loss"])
    
    # --- 1. CONNECTION CENTER ---
    if menu == "Connection Center":
        st.title("📂 Database Connection")
        uploaded_file = st.file_uploader("Upload Inventory Excel", type=["xlsx"])
        if uploaded_file:
            st.session_state.inventory = pd.read_excel(uploaded_file)
            st.success("✅ Records Synced!")
            st.dataframe(st.session_state.inventory, use_container_width=True)

    # --- 2. SELL (POS) ---
    elif menu == "Sell (POS)":
        st.title("🛒 Sales Counter")
        if st.session_state.inventory.empty:
            st.warning("⚠️ Upload inventory first!")
        else:
            options = st.session_state.inventory["Product"].tolist()
            selected = st.multiselect("Select products:", options)
            if selected:
                ts, tp = 0, 0
                details = []
                for item in selected:
                    row = st.session_state.inventory.loc[st.session_state.inventory["Product"] == item]
                    q = st.number_input(f"Qty for {item}", 1, int(row["Stock"].values[0]), key=item)
                    ts += q * row["Price"].values[0]
                    tp += q * (row["Price"].values[0] - row["Cost"].values[0])
                    details.append(f"{item}(x{q})")
                
                if st.button("Complete Sale", type="primary"):
                    for item in selected:
                        st.session_state.inventory.loc[st.session_state.inventory["Product"] == item, "Stock"] -= q
                    new_sale = {"Timestamp": pd.Timestamp.now(), "Type": "SALE", "Details": ", ".join(details), "Amount": ts, "Profit": tp}
                    st.session_state.ledger = pd.concat([st.session_state.ledger, pd.DataFrame([new_sale])], ignore_index=True)
                    st.success(f"Sale Recorded! Profit: Rs {tp:,}")

    # --- 3. EXPENSES ---
    elif menu == "Expenses":
        st.title("💸 Daily Expenses")
        with st.form("exp_form"):
            cat = st.selectbox("Category", ["Rent", "Electricity", "Salary", "Food", "Other"])
            amt = st.number_input("Amount", min_value=0)
            if st.form_submit_button("Save Expense"):
                new_exp = {"Timestamp": pd.Timestamp.now(), "Category": cat, "Amount": amt}
                st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_exp])], ignore_index=True)
                st.success("Expense Recorded!")

    # --- 4. PROFIT & LOSS (WITH GRAPHS) ---
    elif menu == "Profit & Loss":
        st.title("📉 Performance Analytics")
        
        # Financial Summary
        gross_profit = st.session_state.ledger["Profit"].sum()
        total_exp = st.session_state.expenses["Amount"].sum()
        net_profit = gross_profit - total_exp
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Profit", f"Rs {gross_profit:,}")
        c2.metric("Total Expenses", f"Rs {total_exp:,}", delta_color="inverse")
        c3.metric("NET PROFIT", f"Rs {net_profit:,}")

        st.divider()
        
        # --- VISUAL CHARTS ---
        st.subheader("📅 7-Day Performance Trends")
        if not st.session_state.ledger.empty:
            # Preparing data for chart
            chart_data = st.session_state.ledger.copy()
            chart_data['Date'] = chart_data['Timestamp'].dt.date
            daily_profit = chart_data.groupby('Date')['Profit'].sum()
            
            st.line_chart(daily_profit)
            
            # Expense Distribution
            if not st.session_state.expenses.empty:
                st.subheader("🍕 Expense Breakdown")
                exp_dist = st.session_state.expenses.groupby('Category')['Amount'].sum()
                st.bar_chart(exp_dist)
        else:
            st.info("No data available yet to show trends.")

        # Export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            st.session_state.inventory.to_excel(writer, index=False, sheet_name='Inventory')
            st.session_state.ledger.to_excel(writer, index=False, sheet_name='Profit_Report')
        st.download_button("📥 Download Final 2026 Report", output.getvalue(), "Business_Report_2026.xlsx")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
