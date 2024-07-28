import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "original_text, prefix, expected_text",
    [
        ("Hello, World!", "Hello, ", "World!"),
        ("Hello, World!", "World", "Hello, World!"),
        ("Hello, World!", "", "Hello, World!"),
        ("", "Hello", ""),
        ("Hello, World!", "Goodbye, ", "Hello, World!"),
        ("SpecialPrefixText", "SpecialPrefix", "Text"),
        ("INoPrefix", "No", "INoPrefix"),
        ("NoPrefix", "No", "Prefix"),
    ],
)
def test_removeprefix_variations(original_text: str, prefix: str, expected_text: str) -> None:
    """
    Test the `removeprefix` method with various combinations of original text and prefixes.

    :param original_text: The original text of the LangString.
    :param prefix: The prefix to remove.
    :param expected_text: The expected text after removing the prefix.
    :return: None
    """
    lang_string = LangString(original_text, "en")
    modified_lang_string = lang_string.removeprefix(prefix)
    assert modified_lang_string.text == expected_text, f"Expected '{expected_text}' after removing prefix '{prefix}'"


import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "invalid_prefix",
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
def test_removeprefix_invalid_type(invalid_prefix) -> None:
    """
    Test the `removeprefix` method with various invalid types for the prefix.

    :param invalid_prefix: An invalid prefix of various types.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="argument must be str, not"):
        lang_string.removeprefix(invalid_prefix)


def test_removeprefix_unusual_valid_prefix() -> None:
    """
    Test the `removeprefix` method with a prefix that is a substring but not at the start.

    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    modified_lang_string = lang_string.removeprefix("World")
    assert (
        modified_lang_string.text == "Hello, World!"
    ), "removeprefix should not alter LangString if prefix is not at the start"
