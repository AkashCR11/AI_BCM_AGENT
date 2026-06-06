import streamlit as st
from bcm_data import products, modules
from agent import agent_router
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(page_title="BCM AI", layout="wide")

# ----------------------------------
# DARK THEME (EY STYLE)
# ----------------------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #4B8BBE;
}

.stButton button {
    background-color: #1E1E1E;
    color: white;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
}

.stButton button:hover {
    background-color: #4B8BBE;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("<h1 style='text-align:center;'>🌙 BCM AI REPO</h1>", unsafe_allow_html=True)

# ----------------------------------
# 🔍 SEARCH BAR
# ----------------------------------
search = st.text_input("🔍 Search Products / Modules")

# ----------------------------------
# FILTER DATA
# ----------------------------------
filtered_products = [
    p for p in products if search.lower() in p.lower()
] if search else list(products.keys())

filtered_modules = [
    m for m in modules if search.lower() in m.lower()
] if search else list(modules.keys())

# ----------------------------------
# CARD GRID FUNCTION
# ----------------------------------
def show_cards(items, key_prefix):
    cols = st.columns(4)

    for i, item in enumerate(items):
        with cols[i % 4]:
            if st.button(item, key=f"{key_prefix}_{item}"):
                st.session_state.selected = item

# ----------------------------------
# PRODUCTS GRID
# ----------------------------------
st.subheader("📦 Products")
show_cards(filtered_products, "product")

# ----------------------------------
# MODULES GRID
# ----------------------------------
st.subheader("🧩 Modules")
show_cards(filtered_modules, "module")

# ----------------------------------
# POPUP PANEL (DETAIL VIEW)
# ----------------------------------
st.markdown("---")

if "selected" in st.session_state:
    name = st.session_state.selected

    if name in products:
        data = products[name]

        st.markdown(f"### ✅ Product: {name}")
        st.write(data["description"])

        st.markdown(f"🔗 {data['repo_link']}")

        st.write("### Modules")
        for m in data["modules"]:
            st.write(f"➡️ {m}")

    elif name in modules:
        data = modules[name]

        st.markdown(f"### ✅ Module: {name}")
        st.write(data["description"])

        st.write("### Used in Products")
        for p in data["products"]:
            st.write(f"➡️ {p}")

# ----------------------------------
# GRAPH VISUALIZATION
# ----------------------------------
st.markdown("---")
st.subheader("📊 Product ↔ Module Graph")

G = nx.Graph()

# Add edges
for p, pdata in products.items():
    for m in pdata["modules"]:
        G.add_edge(p, m)

fig, ax = plt.subplots()
nx.draw(G, with_labels=True, node_color="skyblue", node_size=2000, ax=ax)

st.pyplot(fig)

# ----------------------------------
# CHATBOT
# ----------------------------------
st.markdown("---")
st.subheader("💬 AI Assistant")

user_input = st.chat_input("Ask anything...")

if user_input:
    with st.spinner("Thinking..."):
        response = agent_router(user_input)

    st.markdown("### 🤖 Response")
    st.markdown(response)
