import sqlite3

# ✅ Create connection
def get_connection():
    return sqlite3.connect("bcm.db", check_same_thread=False)


# ✅ STEP 1 — Initialize DB
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        name TEXT PRIMARY KEY,
        description TEXT,
        repo_link TEXT
    )
    """)

    # Modules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        name TEXT PRIMARY KEY,
        description TEXT
    )
    """)

    # Mapping table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_module (
        product TEXT,
        module TEXT
    )
    """)

    conn.commit()


# ✅ STEP 2 — Seed (Initial Data)
def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Products
    products = [
        ("FIS Finnacle", "Core banking system", "https://example.com/finnacle"),
        ("FlexCube", "Universal banking solution", "https://example.com/flexcube"),
        ("Q2", "Digital banking platform", "https://example.com/q2")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products VALUES (?, ?, ?)", products
    )

    # Modules
    modules = [
        ("Deposits", "Handles savings accounts"),
        ("Loans", "Loan lifecycle"),
        ("Payments", "NEFT/RTGS/UPI"),
        ("Cards", "Card management"),
        ("Accounts", "Customer accounts"),
        ("AML", "Anti-money laundering"),
        ("KYC", "Customer verification")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO modules VALUES (?, ?)", modules
    )

    # Mapping
    mapping = [
        ("FIS Finnacle", "Deposits"),
        ("FIS Finnacle", "Loans"),
        ("FlexCube", "Loans"),
        ("FlexCube", "Cards"),
        ("FlexCube", "AML"),
        ("Q2", "Payments"),
        ("Q2", "Cards"),
        ("Q2", "Accounts")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO product_module VALUES (?, ?)", mapping
    )

    conn.commit()


# ✅ STEP 3 — Fetch Functions

def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_modules():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modules")
    return cursor.fetchall()


def get_product_modules(product):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT module FROM product_module WHERE product=?",
        (product,)
    )
    return [row[0] for row in cursor.fetchall()]


def get_module_products(module):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT product FROM product_module WHERE module=?",
        (module,)
    )
    return [row[0] for row in cursor.fetchall()]
