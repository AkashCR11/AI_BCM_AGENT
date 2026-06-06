import streamlit as st
from bcm_data import products, modules
from agent import agent_router

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
# DISPLAY DETAILS (CENTER PANEL)
# -----------------------------------
st.markdown("---")

col3, col4 = st.columns(2)

# ---------------- PRODUCT DETAILS
with col3:
    if "selected_product" in st.session_state:
        p = st.session_state.selected_product
        data = products[p]

        st.markdown(f"### ✅ {p}")
        st.write(data["description"])

        st.markdown(f"{data['repo_link']}")

        st.markdown("#### 📦 Modules")
        for m in data["modules"]:
            st.markdown(f"- 🔗 {m}")

# ---------------- MODULE DETAILS
with col4:
    if "selected_module" in st.session_state:
        m = st.session_state.selected_module
        data = modules[m]

        st.markdown(f"### ✅ {m}")
        st.write(data["description"])

        st.markdown("#### 🏦 Used in Products")
        for p in data["products"]:
            st.markdown(f"- 🔗 {p}")

# -----------------------------------
# CHAT AREA (BOTTOM)
# -----------------------------------
st.markdown("---")
st.markdown("### 💬 Ask Anything")

user_input = st.chat_input("Ask about products, modules, or banking concepts...")

if user_input:
    with st.spinner("Thinking..."):
        response = agent_router(user_input)

    st.markdown("### 🤖 Response")
    st.markdown(response)
