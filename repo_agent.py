from database import (
    get_products,
    get_modules,
    get_product_modules,
    get_module_products
)

def repo_agent(query):
    query = query.lower()

    products = get_products()
    modules = get_modules()

    # ✅ PRODUCT MATCH
    for name, desc, link in products:
        if name.lower() in query:
            module_list = get_product_modules(name)

            return f"""
### 🏦 Product: {name}

📖 Description:
{desc}

🔗 Repo Link:
{link}

🧩 Modules:
{", ".join(module_list)}
"""

    # ✅ MODULE MATCH
    for name, desc in modules:
        if name.lower() in query:
            product_list = get_module_products(name)

            return f"""
### 🧩 Module: {name}

📖 Description:
{desc}

🏦 Used in Products:
{", ".join(product_list)}
"""

    return None
