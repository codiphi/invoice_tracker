import sqlite3

def init_database(database_path):
    """
    Creates an SQLite database and sets up tables for the receipt/invoice schema.
    """
    # Connect to SQLite database (creates the file if it doesn't exist)
    connection = sqlite3.connect(database_path)

    try:
        cursor = connection.cursor()

        # Create the receipt_or_invoice table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipt_or_invoice (
                id TEXT PRIMARY KEY,
                category TEXT CHECK (category IN ('Travel', 'Food', 'Miscellaneous', 'Office Supplies', 'Software', 'Repairs')),
                date TEXT,
                subtotal NUMERIC,
                discount NUMERIC,
                tax NUMERIC,
                tip NUMERIC,
                total NUMERIC,
                balance NUMERIC,
                payment_method TEXT,
                payment_details TEXT,
                notes TEXT
            );
        """)

        # Create the vendor table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id TEXT,
                name TEXT,
                street TEXT,
                city TEXT,
                state_or_province TEXT,
                postal_code TEXT,
                country TEXT,
                phone TEXT,
                email TEXT,
                FOREIGN KEY (receipt_id) REFERENCES receipt_or_invoice(id)
            );
        """)

        # Create the items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id TEXT,
                description TEXT,
                unit_price NUMERIC,
                quantity NUMERIC,
                line_total NUMERIC,
                FOREIGN KEY (receipt_id) REFERENCES receipt_or_invoice(id)
            );
        """)

        connection.commit()
        print(f"Database and tables created successfully at '{database_path}'.")
    finally:
        connection.close()
        
def insert_data(connection, queries):
    with connection:
        for inserts in queries:
            connection.execute(inserts)