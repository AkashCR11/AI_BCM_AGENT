from bcm_data import products, modules

def repo_agent(query):
    query = query.lower()

    for product in products:
        if product.lower() in query:
            data = products[product]

            return f"""
### 🏦 Product: {product}

📖 Description:
{data['description']}

🔗 Repo Link:
{data['repo_link']}

🧩 Modules:
{", ".join(data['modules'])}
"""

    for module in modules:
        if module.lower() in query:
            data = modules[module]

            return f"""
### 🧩 Module: {module}

📖 Description:
{data['description']}

🏦 Used in:
{", ".join(data['products'])}
"""

    return None
