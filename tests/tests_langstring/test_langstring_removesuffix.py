import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "original_text, suffix, expected_text",
    [
        ("Hello, World!", "World!", "Hello, "),
        ("Hello, World!", "Hello", "Hello, World!"),
        ("Hello, World!", "", "Hello, World!"),
        ("", "World", ""),
        ("Hello, World!", "Goodbye", "Hello, World!"),
        ("TextWithSpecialSuffix", "SpecialSuffix", "TextWith"),
        ("SuffixNot", "Not", "Suffix"),
        ("SuffixNo", "Not", "SuffixNo"),
    ],
)
def test_removesuffix_variations(original_text: str, suffix: str, expected_text: str) -> None:
    """
    Test the `removesuffix` method with various combinations of original text and suffixes.

    :param original_text: The original text of the LangString.
    :param suffix: The suffix to remove.
    :param expected_text: The expected text after removing the suffix.
    :return: None
    """
    lang_string = LangString(original_text, "en")
    modified_lang_string = lang_string.removesuffix(suffix)
    assert modified_lang_string.text == expected_text, f"Expected '{expected_text}' after removing suffix '{suffix}'"


import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "invalid_suffix",
    [
        123,  # Integer
        True,  # Boolean
        123.45,  # Float (Real number)
        ["list"],  # List
        {"set"},  # Set
        {"key": "value"},  # Dictionary
        (1, 2, 3),  # Tuple
    ],
)
def test_removesuffix_invalid_type(invalid_suffix) -> None:
    """
    Test the `removesuffix` method with various invalid types for the suffix.

    :param invalid_suffix: An invalid suffix of various types.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="argument must be str"):
        lang_string.removesuffix(invalid_suffix)


def test_removesuffix_unusual_valid_suffix() -> None:
    """
    Test the `removesuffix` method with a suffix that is a substring but not at the end.

    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    modified_lang_string = lang_string.removesuffix("Hello")
    assert (
        modified_lang_string.text == "Hello, World!"
    ), "removesuffix should not alter LangString if suffix is not at the end"
