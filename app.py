import streamlit as st
from database import init_db, seed_data, get_products, get_modules, get_product_modules, get_module_products
from agent import agent_router

# -----------------------------------
# ✅ INITIALIZE DATABASE
# -----------------------------------
init_db()
seed_data()

# -----------------------------------
# GET DATA FROM DB
# -----------------------------------
product_data = get_products()   # [(name, desc, repo)]
module_data = get_modules()     # [(name, desc)]

products = [p[0] for p in product_data]
modules = [m[0] for m in module_data]

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="BCM AI Repo", layout="wide")

# -----------------------------------
# MODERN CSS (ENTERPRISE LOOK)
# -----------------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    padding: 15px;
    color: #0A2F5A;
}

.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f8f9fa;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
    cursor: pointer;
    margin-bottom: 10px;
    transition: 0.3s;
}

.card:hover {
    background-color: #e6f0ff;
    transform: scale(1.03);
}

.section-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("<div class='main-title'>🏦 BCM AI REPO</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------
# LAYOUT
# -----------------------------------
col1, col2 = st.columns(2)

# -----------------------------------
# PRODUCTS CARDS
# -----------------------------------
with col1:
    st.markdown("<div class='section-title'>📦 Products</div>", unsafe_allow_html=True)

    for product in products:
        if st.button(product, key=f"product_{product}"):
            st.session_state.selected_product = product

# -----------------------------------
# MODULES CARDS
# -----------------------------------
with col2:
    st.markdown("<div class='section-title'>🧩 Modules</div>", unsafe_allow_html=True)

    for module in modules:
        if st.button(module, key=f"module_{module}"):
            st.session_state.selected_module = module

# -----------------------------------
# DISPLAY DETAILS
# -----------------------------------
st.markdown("---")
col3, col4 = st.columns(2)

# ✅ PRODUCT DETAILS
with col3:
    if "selected_product" in st.session_state:
        selected_product = st.session_state.selected_product

        # Fetch product info
        product_info = [p for p in product_data if p[0] == selected_product][0]
        name, desc, repo = product_info

        st.markdown(f"### ✅ {name}")
        st.write(desc)
        st.markdown(f"🔗 {repo}")

        # Fetch modules
        modules_list = get_product_modules(name)

        st.markdown("#### 📦 Modules")
        for m in modules_list:
            st.markdown(f"- 🔗 {m}")

# ✅ MODULE DETAILS
with col4:
    if "selected_module" in st.session_state:
        selected_module = st.session_state.selected_module

        # Fetch module info
        module_info = [m for m in module_data if m[0] == selected_module][0]
        name, desc = module_info

        st.markdown(f"### ✅ {name}")
        st.write(desc)

        # Fetch related products
        product_list = get_module_products(name)

        st.markdown("#### 🏦 Used in Products")
        for p in product_list:
            st.markdown(f"- 🔗 {p}")

st.markdown("### 📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF / Excel",
    type=["pdf", "xlsx"]
)

if uploaded_file:
    file_path = "temp." + uploaded_file.name.split(".")[-1]

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File Uploaded")

    st.session_state.file_path = file_path
    
# -----------------------------------
# CHAT AREA
# -----------------------------------
st.markdown("---")
st.markdown("### 💬 Ask Anything")

user_input = st.chat_input("Ask about products, modules, or banking concepts...")

if user_input:
    with st.spinner("Thinking..."):
        response = agent_router(user_input)

    st.markdown("### 🤖 Response")
    st.markdown(response)
