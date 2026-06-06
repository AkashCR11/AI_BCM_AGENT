products = {
    "FIS Finnacle": {
        "description": "Core banking solution for retail and corporate banking",
        "modules": ["Deposits", "Loans", "Payments", "Accounts"],
        "repo_link": "https://github.com/example/finnacle"
    },
    "FlexCube": {
        "description": "Universal banking platform supporting multi-entity operations",
        "modules": ["Loans", "Cards", "AML", "KYC"],
        "repo_link": "https://github.com/example/flexcube"
    },
    "Q2": {
        "description": "Digital banking platform for customer engagement",
        "modules": ["Payments", "Cards", "Accounts"],
        "repo_link": "https://github.com/example/q2"
    }
}

modules = {
    "Deposits": {
        "description": "Handles savings and deposit accounts",
        "products": ["FIS Finnacle"]
    },
    "Loans": {
        "description": "Loan lifecycle and processing",
        "products": ["FIS Finnacle", "FlexCube"]
    },
    "Payments": {
        "description": "Handles NEFT, RTGS, UPI payments",
        "products": ["FIS Finnacle", "Q2"]
    },
    "Cards": {
        "description": "Credit/Debit card management",
        "products": ["FlexCube", "Q2"]
    },
    "Accounts": {
        "description": "Customer account handling",
        "products": ["FIS Finnacle", "Q2"]
    },
    "AML": {
        "description": "Anti-money laundering monitoring",
        "products": ["FlexCube"]
    },
    "KYC": {
        "description": "Customer verification process",
        "products": ["FlexCube"]
    }
}
