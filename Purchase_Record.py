import pandas as pd

st.divider()
st.header("📈 Sales Analytics (Monthly / Yearly)")

try:
    df = pd.read_csv("daily_sales.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # --- Select Report Type ---
    report_type = st.selectbox(
        "Select Report Type:",
        ["Monthly Report", "Yearly Report"]
    )

    if report_type == "Monthly Report":
        df["Month"] = df["Date"].dt.to_period("M")
        summary = df.groupby("Month")["Amount"].sum().reset_index()

        st.subheader("📅 Monthly Sales Report")
        st.table(summary)

        st.bar_chart(summary.set_index("Month"))

        csv = summary.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Monthly Report",
            csv,
            "monthly_sales_report.csv",
            "text/csv"
        )

    else:
        df["Year"] = df["Date"].dt.year
        summary = df.groupby("Year")["Amount"].sum().reset_index()

        st.subheader("📆 Yearly Sales Report")
        st.table(summary)

        st.line_chart(summary.set_index("Year"))

        csv = summary.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Yearly Report",
            csv,
            "yearly_sales_report.csv",
            "text/csv"
        )

except FileNotFoundError:
    st.warning("No sales data available yet")
