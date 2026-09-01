def generate_answer(
    question: str,
    context: str,
    llm,
) -> str:
    from src.qa import build_prompt

    prompt = build_prompt(
        question=question,
        context=context,
    )

    return llm.generate(prompt)
