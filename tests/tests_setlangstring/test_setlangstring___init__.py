import pytest
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


# Test cases for valid initialization
@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"hello", "world"}, "en"),
        (set(), ""),
        (None, "fr"),
        ({"こんにちは", "世界"}, "jp"),
        ({"😊", "😂"}, "en"),
        ({"1", "2", "3"}, "en"),
    ],
)
def test_setlangstring_init_valid(texts, lang) -> None:
    """
    Test valid initializations of SetLangString.

    :param texts: A set of strings or None.
    :param lang: A language string.
    :return: None. Asserts if SetLangString is initialized correctly.
    """
    set_lang_string = SetLangString(texts, lang)
    expected_texts = texts if texts is not None else set()
    assert set_lang_string.texts == expected_texts, (
        f"Expected texts {expected_texts} but got {set_lang_string.texts} "
        f"when initializing with texts {texts} and language '{lang}'"
    )

    assert (
        set_lang_string.lang == lang
    ), f"Expected language '{lang}' but got '{set_lang_string.lang}' when initializing with language '{lang}'"


# Test cases for invalid 'texts' input
@pytest.mark.parametrize(
    "invalid_texts",
    [
        "hello",  # String instead of set
        123,  # Integer instead of set
        {"hello", 123},  # Set with invalid element type
        "",  # Empty string
        ["valid", 123],  # Mixed types in list
        {"valid", 123},  # Mixed types in set
        ["valid", ["nested"]],  # Nested list
        {"valid", ("nested",)},  # Tuple inside set
        [1.5, "valid"],  # Float in list
        {1.5, "valid"},  # Float in set
        "a",  # Single character string
        True,  # Boolean type
        False,  # Boolean type
        object(),  # Object type
    ],
)
def test_setlangstring_init_invalid_texts(invalid_texts) -> None:
    """
    Test invalid 'texts' input during initialization of SetLangString.

    :param invalid_texts: Invalid 'texts' input.
    :return: None. Asserts if TypeError is raised for invalid 'texts' input.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        SetLangString(invalid_texts, "en")


# Test cases for invalid 'lang' input
@pytest.mark.parametrize(
    "invalid_lang",
    [123, ["en"], {"lang": "en"}],  # Integer instead of string  # List instead of string  # Dict instead of string
)
def test_setlangstring_init_invalid_lang(invalid_lang) -> None:
    """
    Test invalid 'lang' input during initialization of SetLangString.

    :param invalid_lang: Invalid 'lang' input.
    :return: None. Asserts if TypeError is raised for invalid 'lang' input.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        SetLangString({"hello", "world"}, invalid_lang)


# Additional test cases for unusual but valid scenarios
@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"hello", "こんにちは", "😊"}, "en123"),  # Mixed language and emoji texts with numeric lang
        (
            {"long_text_" * 100, "another_long_text_" * 100},
            "special_@_lang",
        ),  # Extremely long texts and special character lang
    ],
)
def test_setlangstring_init_unusual_valid(texts, lang) -> None:
    """
    Test unusual but valid initializations of SetLangString.

    :param texts: A set of strings with mixed types.
    :param lang: A language string with non-standard characters.
    :return: None. Asserts if SetLangString is initialized correctly with unusual inputs.
    """
    set_lang_string = SetLangString(texts, lang)

    assert set_lang_string.texts == texts, (
        f"Expected texts {texts} but got {set_lang_string.texts} "
        f"when initializing with texts {texts} and language '{lang}'"
    )

    assert (
        set_lang_string.lang == lang
    ), f"Expected language '{lang}' but got '{set_lang_string.lang}' when initializing with language '{lang}'"


# Test for default initialization


def test_setlangstring_init_default() -> None:
    """

    Test default initialization of SetLangString.



    :return: None. Asserts if SetLangString is initialized correctly with default values.

    """

    set_lang_string = SetLangString()

    assert (
        set_lang_string.texts == set()
    ), f"Expected texts to be empty set but got {set_lang_string.texts} when initializing with default values"

    assert (
        set_lang_string.lang == ""
    ), f"Expected language to be empty string but got '{set_lang_string.lang}' when initializing with default values"
