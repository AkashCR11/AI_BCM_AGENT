import sqlite3

# ✅ Create connection
def get_connection():
    return sqlite3.connect("bcm.db", check_same_thread=False)


# ✅ STEP 1 — Initialize DB
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        name TEXT PRIMARY KEY,
        description TEXT,
        repo_link TEXT
    )
    """)

    # ✅ Modules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        name TEXT PRIMARY KEY,
        description TEXT
    )
    """)

    # ✅ Mapping table (FIXED with PRIMARY KEY)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_module (
        product TEXT,
        module TEXT,
        PRIMARY KEY (product, module)
    )
    """)

    conn.commit()


# ✅ STEP 2 — Seed Data (SAFE INSERT)
def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Products
    products = [
        ("FIS Finnacle", "Core banking system", "https://example.com/finnacle"),
        ("FlexCube", "Universal banking solution", "https://example.com/flexcube"),
        ("Q2", "Digital banking platform", "https://example.com/q2")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products VALUES (?, ?, ?)", products
    )

    # ✅ Modules
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

    # ✅ Mapping (NO duplicates will be inserted)
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


# ✅ OPTIONAL — CLEAN EXISTING DUPLICATES (RUN ONCE)
def remove_duplicates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM product_module
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM product_module
        GROUP BY product, module
    )
    """)

    conn.commit()


# ✅ STEP 3 — FETCH FUNCTIONS

def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY name")
    return cursor.fetchall()


def get_modules():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modules ORDER BY name")
    return cursor.fetchall()


def get_product_modules(product):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT module
    FROM product_module
    WHERE product=?
    """, (product,))

    return [row[0] for row in cursor.fetchall()]


def get_module_products(module):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT product
    FROM product_module
    WHERE module=?
    """, (module,))

    return [row[0] for row in cursor.fetchall()]
