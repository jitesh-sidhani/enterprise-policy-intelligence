import streamlit as st
from policy_service import ask

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Enterprise Policy Intelligence",
    page_icon="🏢",
    layout="wide"
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------
st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

.main-title{
    font-size:42px;
    font-weight:700;
    margin-bottom:0px;
}

.subtitle{
    color:#8b8b8b;
    font-size:18px;
    margin-bottom:30px;
}

.response-box{
    border:1px solid #444;
    border-radius:12px;
    padding:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">🏢 Enterprise Policy Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Multi-Agent Enterprise Policy Intelligence Platform</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("🤖 Agent Pipeline")

    st.success("Safety Agent")
    st.success("Router Agent")
    st.success("Retriever Agent")
    st.success("Generator Agent")
    st.success("Verifier Agent")

    st.divider()

    st.markdown("### Tech Stack")

    st.write("• LangChain")
    st.write("• Groq")
    st.write("• FAISS")
    st.write("• HuggingFace Embeddings")
    st.write("• Streamlit")

# ---------------------------------------------------
# Main Layout
# ---------------------------------------------------

left, right = st.columns([1, 1])

# ---------------- Left ----------------

with left:

    st.subheader("📝 Ask a Policy Question")

    question = st.text_area(
        "",
        placeholder="Example: How many annual leave days do permanent managers receive?",
        height=180
    )

    col1, col2 = st.columns(2)

    ask_btn = col1.button(
        "Submit",
        use_container_width=True,
        type="primary"
    )

    clear_btn = col2.button(
        "Clear",
        use_container_width=True
    )

    if clear_btn:
        st.rerun()

# ---------------- Right ----------------

with right:

    st.subheader("🤖 AI Response")

    if ask_btn:

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:

            with st.spinner("Analyzing policy..."):

                response = ask(question)

            st.markdown(response)

    else:

        st.info("Your answer will appear here.")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption(
    "Powered by RAG • LangChain • Groq • FAISS"
)