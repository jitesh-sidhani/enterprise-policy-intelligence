from langchain_community.vectorstores import FAISS


def create_vectorstore(chunks, embedding_model):

    return FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )


def save_vectorstore(vectorstore):

    vectorstore.save_local("db/faiss_index")


def load_vectorstore(embedding_model):

    return FAISS.load_local(
        "db/faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )


def search_documents(vectorstore, query, k=3):
    """
    Returns the top-k most relevant chunks.
    """

    docs = vectorstore.similarity_search(query, k=k)

    return docs