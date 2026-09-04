
from src.models import Chunk, EmbeddedChunk
from src.qa import (
    NO_ANSWER_MESSAGE,
    build_context,
    build_prompt,
    format_answer,
    get_source_pages,
    is_no_answer,
)


def make_embedded_chunk(
    chunk_id: int,
    page_number: int,
    text: str,
) -> EmbeddedChunk:
    chunk = Chunk(
        chunk_id=chunk_id,
        page_number=page_number,
        text=text,
    )

    return EmbeddedChunk(
        chunk=chunk,
        vector=[1.0, 0.0, 0.0],
    )


def test_build_context_includes_page_numbers():
    chunks = [
        make_embedded_chunk(
            chunk_id=1,
            page_number=2,
            text="First page content.",
        ),
        make_embedded_chunk(
            chunk_id=2,
            page_number=5,
            text="Second page content.",
        ),
    ]

    context = build_context(chunks)

    assert "[Page 2]" in context
    assert "First page content." in context
    assert "[Page 5]" in context
    assert "Second page content." in context


def test_build_context_separates_chunks():
    chunks = [
        make_embedded_chunk(
            chunk_id=1,
            page_number=1,
            text="First chunk.",
        ),
        make_embedded_chunk(
            chunk_id=2,
            page_number=1,
            text="Second chunk.",
        ),
    ]

    context = build_context(chunks)

    assert "First chunk.\n\n[Page 1]\nSecond chunk." in context


def test_build_prompt_contains_question_and_context():
    question = "What machine is described?"
    context = "[Page 1]\nThe document describes machine M42."

    prompt = build_prompt(
        question=question,
        context=context,
    )

    assert question in prompt
    assert context in prompt


def test_build_prompt_requires_context_only():
    prompt = build_prompt(
        question="What is the machine?",
        context="Machine M42 is described.",
    )

    assert "Use only information explicitly contained in the context." in prompt
    assert "Do not use outside knowledge." in prompt
    assert "Do not guess or infer information" in prompt
    assert NO_ANSWER_MESSAGE in prompt


def test_is_no_answer_detects_standard_message():
    assert is_no_answer(NO_ANSWER_MESSAGE)


def test_is_no_answer_detects_german_message():
    answer = (
        "Die Antwort ist nicht im bereitgestellten Text enthalten."
    )

    assert is_no_answer(answer)


def test_is_no_answer_ignores_whitespace_and_case():
    answer = (
        "  THE ANSWER IS NOT AVAILABLE IN THE "
        "PROVIDED DOCUMENT.  "
    )

    assert is_no_answer(answer)


def test_is_no_answer_rejects_real_answer():
    answer = "Die Maschine M42 wird im Dokument beschrieben."

    assert not is_no_answer(answer)


def test_get_source_pages_returns_unique_sorted_pages():
    chunks = [
        make_embedded_chunk(
            chunk_id=1,
            page_number=5,
            text="Page five.",
        ),
        make_embedded_chunk(
            chunk_id=2,
            page_number=2,
            text="Page two.",
        ),
        make_embedded_chunk(
            chunk_id=3,
            page_number=5,
            text="Another chunk on page five.",
        ),
        make_embedded_chunk(
            chunk_id=4,
            page_number=1,
            text="Page one.",
        ),
    ]

    pages = get_source_pages(chunks)

    assert pages == [1, 2, 5]


def test_get_source_pages_returns_empty_list_for_no_chunks():
    assert get_source_pages([]) == []


def test_format_answer_adds_source_pages():
    answer = "Machine M42 is described."

    result = format_answer(
        answer=answer,
        source_pages=[1, 3],
    )

    assert result == (
        "Machine M42 is described.\n\n"
        "Source: Page 1, 3"
    )


def test_format_answer_does_not_add_source_when_no_pages():
    answer = "Machine M42 is described."

    result = format_answer(
        answer=answer,
        source_pages=[],
    )

    assert result == answer
    assert "Source:" not in result


def test_format_answer_removes_source_for_no_answer():
    result = format_answer(
        answer=NO_ANSWER_MESSAGE,
        source_pages=[1],
    )

    assert result == NO_ANSWER_MESSAGE
    assert "Source:" not in result


def test_format_answer_removes_source_for_german_no_answer():
    result = format_answer(
        answer=(
            "Die Antwort ist nicht im bereitgestellten "
            "Text enthalten."
        ),
        source_pages=[1],
    )

    assert result == NO_ANSWER_MESSAGE
    assert "Source:" not in result


def test_format_answer_strips_answer_whitespace():
    result = format_answer(
        answer="  Machine M42 is described.  ",
        source_pages=[2],
    )

    assert result == (
        "Machine M42 is described.\n\n"
        "Source: Page 2"
    )
