import streamlit as st
from database import (
    init_db,
    seed_data,
   )    get_products,
    get_modules,
    get_product_modules,
    get_module_products,
    get_connection

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
# ✅ SIDEBAR NAVIGATION ✅✅✅
# -----------------------------------
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Admin Panel"]
)

# =========================================================
# ✅ DASHBOARD
# =========================================================
if menu == "Dashboard":

    # ✅ FETCH DATA (ALWAYS REFRESH)
    product_data = get_products()
    module_data = get_modules()

    products = [p[0] for p in product_data]
    modules = [m[0] for m in module_data]

    # -----------------------------------
    # ✅ HEADER
    # -----------------------------------
    st.markdown("<h1 style='text-align:center;'>🏦 BCM AI REPO</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # -----------------------------------
    # ✅ PRODUCTS + MODULES
    # -----------------------------------
    col1, col2 = st.columns(2)

    # ✅ PRODUCTS
    with col1:
        st.subheader("📦 Products")

        for product in sorted(products):
            if st.button(product, key=f"product_{product}"):
                st.session_state.selected_product = product

    # ✅ MODULES (FIXED)
    with col2:
        st.subheader("🧩 Modules")

        for module in sorted(modules):
            if st.button(module, key=f"module_{module}"):
                st.session_state.selected_module = module

    # -----------------------------------
    # ✅ DETAILS
    # -----------------------------------
    st.markdown("---")
    col3, col4 = st.columns(2)

    # ✅ PRODUCT DETAILS
    with col3:
        if "selected_product" in st.session_state:
            p = st.session_state.selected_product
            info = next(x for x in product_data if x[0] == p)

            st.markdown(f"### ✅ {p}")
            st.write(info[1])
            st.markdown(f"🔗 {info[2]}")

            st.markdown("#### 📦 Modules")
            for m in get_product_modules(p):
                st.write(f"➡️ {m}")

    # ✅ MODULE DETAILS
    with col4:
        if "selected_module" in st.session_state:
            m = st.session_state.selected_module
            info = next(x for x in module_data if x[0] == m)

            st.markdown(f"### ✅ {m}")
            st.write(info[1])

            st.markdown("#### 🏦 Used in Products")
            for p in get_module_products(m):
                st.write(f"➡️ {p}")

    # -----------------------------------
    # ✅ FILE UPLOAD
    # -----------------------------------
    st.markdown("---")
    st.subheader("📂 Upload Document")

    uploaded_file = st.file_uploader("Upload PDF/Excel", type=["pdf", "xlsx"])

    if uploaded_file:
        file_path = f"temp.{uploaded_file.name.split('.')[-1]}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("✅ File uploaded")
        st.session_state.file_path = file_path

    # -----------------------------------
    # ✅ CHAT (COPILOT STYLE)
    # -----------------------------------
    st.markdown("---")
    st.subheader("💬 Ask Anything")

    # ✅ DISPLAY CHAT HISTORY
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ INPUT
    user_input = st.chat_input("Ask about products, modules...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        response = agent_router(user_input)

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

    # -----------------------------------
    # ✅ DOWNLOAD REPORT ✅✅✅
    # -----------------------------------
    st.markdown("---")

    if st.button("📥 Download Chat Report"):
        report = ""

        for msg in st.session_state.chat_history:
            role = msg["role"].upper()
            report += f"{role}:\n{msg['content']}\n\n"

        st.download_button(
            label="Download",
            data=report,
            file_name="chat_report.txt"
        )

    # -----------------------------------
    # ✅ CLEAR CHAT
    # -----------------------------------
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

# =========================================================
# ✅ ADMIN PANEL ✅✅✅
# =========================================================
elif menu == "Admin Panel":

    st.title("⚙️ Admin Panel")

    conn = get_connection()
    cur = conn.cursor()

    # ✅ ADD PRODUCT
    st.subheader("➕ Add Product")

    p_name = st.text_input("Product Name")
    p_desc = st.text_area("Description")
    p_repo = st.text_input("Repo Link")

    if st.button("Add Product"):
        cur.execute(
            "INSERT OR IGNORE INTO products VALUES (?, ?, ?)",
            (p_name, p_desc, p_repo)
        )
        conn.commit()
        st.success("✅ Product added")
        st.experimental_rerun()

    # ✅ ADD MODULE
    st.subheader("➕ Add Module")

    m_name = st.text_input("Module Name")
    m_desc = st.text_area("Module Description")

    if st.button("Add Module"):
        cur.execute(
            "INSERT OR IGNORE INTO modules VALUES (?, ?)",
            (m_name, m_desc)
        )
        conn.commit()
        st.success("✅ Module added")
        st.experimental_rerun()

    # ✅ MAP PRODUCT ↔ MODULE
    st.subheader("🔗 Map Product ↔ Module")

    products_list = [p[0] for p in get_products()]
    modules_list = [m[0] for m in get_modules()]

    selected_product = st.selectbox("Select Product", products_list)
    selected_module = st.selectbox("Select Module", modules_list)

    if st.button("Create Mapping"):
        cur.execute(
            "INSERT OR IGNORE INTO product_module VALUES (?, ?)",
            (selected_product, selected_module)
        )
        conn.commit()
        st.success("✅ Mapping created")
        st.experimental_rerun()
    get_product_modules, get_module_products,
    get_connection
)
from agent import agent_router

# -----------------------------------
