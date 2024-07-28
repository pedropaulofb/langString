import pytest
from langstring.langstring import LangString


@pytest.mark.parametrize(
    "text, sub, start, end, expected_count",
    [
        ("Hello World", "o", 0, None, 2),
        ("Hello World", "l", 2, 5, 2),
        ("Hello World", "World", 0, 5, 0),
        ("Hello World", "x", 0, None, 0),
        ("", "x", 0, None, 0),
        ("Hello World", "", 0, None, 12),
        ("Hello World", "o", 5, 4, 0),
        ("Hello World", "o", -1, None, 0),
        ("Hello World", "o", None, 5, 1),
    ],
)
def test_count_normal_cases(text, sub, start, end, expected_count):
    """Test count method with various normal cases."""
    lang_str = LangString(text, "en")
    assert lang_str.count(sub, start, end) == expected_count


@pytest.mark.parametrize(
    "text, sub, start, end",
    [
        ("Hello World", 123, 0, None),
        ("Hello World", None, 0, None),
        ("Hello World", ["o"], 0, None),
    ],
)
def test_count_invalid_substring_types(text, sub, start, end):
    """Test count method with invalid substring types."""
    lang_str = LangString(text, "en")
    with pytest.raises(TypeError, match="must be str, not"):
        _ = lang_str.count(sub, start, end)


@pytest.mark.parametrize(
    "text, sub, start, end",
    [
        ("Hello World", "o", "a", None),
        ("Hello World", "o", None, "b"),
        ("Hello World", "o", 1.5, 4),
    ],
)
def test_count_invalid_index_types(text, sub, start, end):
    """Test count method with invalid index types."""
    lang_str = LangString(text, "en")
    with pytest.raises(TypeError, match="slice indices must be integers or None"):
        _ = lang_str.count(sub, start, end)
