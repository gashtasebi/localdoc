from src.models import EmbeddedChunk


def build_context(
    embedded_chunks: list[EmbeddedChunk],
) -> str:
    return "\n\n".join(
        chunk.chunk.text
        for chunk in embedded_chunks
    )



def build_prompt(
    question: str,
    context: str,
) -> str:
    return f"""Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:"""



from src.llm import generate_answer
from src.retriever import retrieve_by_text


def answer_question(
    question: str,
    embedded_chunks,
    embedder,
    llm,
    top_k: int = 3,
) -> str:
    relevant_chunks = retrieve_by_text(
        query=question,
        embedded_chunks=embedded_chunks,
        embedder=embedder,
        top_k=top_k,
    )

    context = build_context(relevant_chunks)

    return generate_answer(
        question=question,
        context=context,
        llm=llm,
    )
