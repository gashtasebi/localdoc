from src.text_cleaner import clean_text

def test_clean_text():
    raw_text = "Frequenz-\numrichter\n\n\nMaschine     M42\tWartung"

    cleaned_text = clean_text(raw_text)
    assert cleaned_text == "Frequenzumrichter\nMaschine M42 Wartung"
