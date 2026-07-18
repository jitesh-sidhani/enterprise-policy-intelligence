from rag.embeddings import get_embedding_model
from rag.vectorstore import load_vectorstore, search_documents


def retrieve_context(question):

    embedding_model = get_embedding_model()

    vectorstore = load_vectorstore(embedding_model)

    docs = search_documents(
        vectorstore,
        question,
        k=7
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context