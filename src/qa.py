from src.models import EmbeddedChunk


def build_context(
    embedded_chunks: list[EmbeddedChunk],
) -> str:
    return "\n\n".join(
        f"[Page {item.chunk.page_number}]\n{item.chunk.text}"
        for item in embedded_chunks
    )


def build_prompt(
    question: str,
    context: str,
) -> str:
    return f"""Answer the question using only the provided context.

Rules:
- Use only information from the context.
- Do not use outside knowledge.
- If the answer is not contained in the context, say:
  "The answer is not available in the provided document."

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
