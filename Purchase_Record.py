def show_receipt_invoice(inv, logo=None):
    html = f"""
    <div style="
        width: 320px;
        margin: auto;
        font-family: monospace;
        border: 1px dashed #000;
        padding: 10px;
    ">
        <h3 style="text-align:center;">SALE INVOICE</h3>

        {"<div style='text-align:center;'><img src='data:image/png;base64," + logo + "' width='120'></div>" if logo else ""}

        <h2 style="text-align:center; margin:5px 0;">ELECTRONIC SHOP</h2>
        <p style="text-align:center; font-size:12px;">
            Main Market, Karachi<br>
            Ph: 0300-1234567
        </p>

        <hr>

        <p style="font-size:12px;">
        Invoice#: {inv['Invoice No']}<br>
        Date: {inv['Date']}<br>
        Customer: {inv['Customer']}<br>
        </p>

        <hr>

        <table width="100%" style="font-size:12px;">
            <tr>
                <th align="left">Item</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
    """

    for item in inv["Items"]:
        html += f"""
        <tr>
            <td>{item['Item']}</td>
            <td align="center">{item['Qty']}</td>
            <td align="right">{item['Price']}</td>
            <td align="right">{item['Total']}</td>
        </tr>
        """

    html += f"""
        </table>

        <hr>

        <p style="font-size:12px;">
        Sub Total: Rs {inv['Sub Total']:,.0f}<br>
        Discount: Rs {inv['Discount']:,.0f}<br>
        GST: Rs {inv['GST']:,.0f}<br>
        </p>

        <h3 style="text-align:center;">
            NET TOTAL: Rs {inv['Grand Total']:,.0f}
        </h3>

        <hr>

        <p style="font-size:12px;">
        Payment Method: Cash
        </p>

        <p style="text-align:center; font-size:11px;">
        Thank you for shopping!<br>
        Goods once sold will not be returned.
        </p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
