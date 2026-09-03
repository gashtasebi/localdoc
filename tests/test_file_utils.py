from src.file_utils import calculate_file_hash


def test_calculate_file_hash(tmp_path):
    file_path = tmp_path / "test.txt"

    file_path.write_text(
        "LocalDoc test"
    )

    first_hash = calculate_file_hash(
        file_path
    )

    second_hash = calculate_file_hash(
        file_path
    )

    assert first_hash == second_hash
    assert len(first_hash) == 64
