def json2query(json_data):
    receipt = json_data["receipt_or_invoice"]

    receipt_query = f"""
    INSERT INTO receipt_or_invoice (id, category, date, subtotal, discount, tax, tip, total, balance, payment_method, payment_details, notes)
    VALUES (
        '{receipt["id"]}',
        '{receipt["category"]}',
        '{receipt["date"]}',
        {receipt["totals"]["subtotal"] or "NULL"},
        {receipt["totals"]["discount"] or "NULL"},
        {receipt["totals"]["tax"] or "NULL"},
        {receipt["totals"]["tip"] or "NULL"},
        {receipt["totals"]["total"] or "NULL"},
        {receipt["totals"]["balance"] or "NULL"},
        '{receipt["payment"]["method"] or "NULL"}',
        '{receipt["payment"]["details"] or "NULL"}',
        '{receipt["notes"].replace("'", "''")}'
    );
    """

    vendor = receipt["vendor"]
    address = vendor["address"]
    vendor_query = f"""
    INSERT INTO vendor (receipt_id, name, street, city, state_or_province, postal_code, country, phone, email)
    VALUES (
        '{receipt["id"]}',
        '{vendor["name"].replace("'", "''")}',
        '{address["street"].replace("'", "''")}',
        '{address["city"].replace("'", "''")}',
        '{address["state_or_province"]}',
        '{address["postal_code"]}',
        '{address["country"]}',
        '{address["phone"]}',
        '{address["email"]}'
    );
    """

    items_queries = []
    for item in receipt["items"]:
        item_query = f"""
        INSERT INTO items (receipt_id, description, unit_price, quantity, line_total)
        VALUES (
            '{receipt["id"]}',
            '{item["description"].replace("'", "''")}',
            {item["unit_price"]},
            {item["quantity"]},
            {item["line_total"]}
        );
        """
        items_queries.append(item_query)

    queries = [receipt_query.strip(), vendor_query.strip()] + [
        query.strip() for query in items_queries
    ]
    return queries