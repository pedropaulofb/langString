import pytest
from langstring.langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "main_text, search_text, expected_result",
    [
        ("Hello World", "World", True),
        ("Hello World", "world", False),  # Case sensitive
        ("Hello World", "", True),  # Empty string is always contained
        ("", "Text", False),  # Empty main string
        ("12345", "23", True),
        ("Special chars !@#", "@#", True),
    ],
)
def test_contains_with_valid_substrings(main_text, search_text, expected_result):
    """Test __contains__ with various valid substrings."""
    lang_str = LangString(main_text, "en")
    assert (search_text in lang_str) == expected_result


@pytest.mark.parametrize(
    "main_text, search_text",
    [("Hello World", 123), ("Hello World", None), ("Hello World", [1, 2, 3]), ("Hello World", {"key": "value"})],
)
def test_contains_with_invalid_substrings(main_text, search_text):
    """Test __contains__ with invalid substring types."""
    lang_str = LangString(main_text, "en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        _ = search_text in lang_str


def test_contains_does_not_modify_original():
    """Test __contains__ does not modify the original LangString."""
    original_text = "Hello World"
    lang_str = LangString(original_text, "en")
    _ = "Hello" in lang_str
    assert lang_str.text == original_text
