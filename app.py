import streamlit as st
from database import (
    init_db, seed_data,
    get_products, get_modules,
    get_product_modules, get_module_products
)
from agent import agent_router

# -----------------------------------
# ✅ INITIALIZE DATABASE (RUN ONCE)
# -----------------------------------
init_db()
seed_data()

# -----------------------------------
# ✅ PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="BCM AI Repo", layout="wide")

# -----------------------------------
# ✅ SESSION INIT
# -----------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------
# ✅ FETCH DATA
# -----------------------------------
product_data = get_products()
module_data = get_modules()

products = [p[0] for p in product_data]
modules = [m[0] for m in module_data]

# -----------------------------------
# ✅ CSS UI
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

.section-title {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# ✅ HEADER
# -----------------------------------
st.markdown("<div class='main-title'>🏦 BCM AI REPO</div>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------
# ✅ UI LAYOUT
# -----------------------------------
col1, col2 = st.columns(2)

# ✅ PRODUCTS
with col1:
    st.markdown("<div class='section-title'>📦 Products</div>", unsafe_allow_html=True)

    for product in products:
        if st.button(product, key=f"product_{product}"):
            st.session_state.selected_product = product

# ✅ MODULES
with col2:
    st.markdown("<div class='section-title'>🧩 Modules</div>", unsafe_allow_html=True)

    for module in modules:
        if st.button(module, key=f"module_{module}"):
            st.session_state.selected_module = module

# -----------------------------------
# ✅ DISPLAY DETAILS
# -----------------------------------
st.markdown("---")
col3, col4 = st.columns(2)

# ✅ PRODUCT DETAILS
with col3:
    if "selected_product" in st.session_state:
        selected_product = st.session_state.selected_product

        product_info = next(p for p in product_data if p[0] == selected_product)
        name, desc, repo = product_info

        st.markdown(f"### ✅ {name}")
        st.write(desc)
        st.markdown(f"🔗 {repo}")

        modules_list = get_product_modules(name)

        st.markdown("#### 📦 Modules")
        for m in modules_list:
            st.markdown(f"- 🔗 {m}")

# ✅ MODULE DETAILS
with col4:
    if "selected_module" in st.session_state:
        selected_module = st.session_state.selected_module

        module_info = next(m for m in module_data if m[0] == selected_module)
        name, desc = module_info

        st.markdown(f"### ✅ {name}")
        st.write(desc)

        product_list = get_module_products(name)

        st.markdown("#### 🏦 Used in Products")
        for p in product_list:
            st.markdown(f"- 🔗 {p}")

# -----------------------------------
# ✅ FILE UPLOAD
# -----------------------------------
st.markdown("---")
st.markdown("### 📂 Upload Document")

uploaded_file = st.file_uploader("Upload PDF or Excel", type=["pdf", "xlsx"])

if uploaded_file:
    file_path = f"temp.{uploaded_file.name.split('.')[-1]}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully")
    st.session_state.file_path = file_path

# -----------------------------------
# ✅ CHAT SECTION (COPILOT STYLE)
# -----------------------------------
st.markdown("---")
st.markdown("### 💬 Ask Anything")

# ✅ DISPLAY CHAT HISTORY
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ INPUT
user_input = st.chat_input("Ask about products, modules, banking...")

if user_input:
    # ✅ user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ AI response
    with st.spinner("Thinking..."):
        response = agent_router(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

# -----------------------------------
# ✅ CLEAR CHAT BUTTON
# -----------------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
