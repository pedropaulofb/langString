from typing import Optional
from typing import Set
from typing import Union

import pytest
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, expected_texts, expected_lang_str",
    [
        (None, "lang", set(), "lang"),
        ({"texts"}, None, {"texts"}, ""),
        (None, None, set(), ""),
        ({"hello", "world"}, "en", {"hello", "world"}, "en"),
        (set(), "en", set(), "en"),  # Adjusted to use set directly for comparison
        ([], "en", set(), "en"),  # Adjusted to use set directly for comparison
        ([], "", set(), ""),  # Adjusted to use set directly for comparison
        ({"привет", "мир"}, "ru", {"привет", "мир"}, "ru"),
        ({"😊", "😂"}, "en", {"😊", "😂"}, "en"),
        ({"", " "}, "en", {"", " "}, "en"),
        ({"UPPER", "lower"}, "en", {"UPPER", "lower"}, "en"),
        ({"   leading", "trailing   "}, "en", {"   leading", "trailing   "}, "en"),
        ({"Γειά", "σου"}, "el", {"Γειά", "σου"}, "el"),
        ({"mixedCASE", "TEXT"}, "en", {"mixedCASE", "TEXT"}, "en"),
        ({"    "}, "en", {"    "}, "en"),  # Strings with only spaces
        ({"", "non-empty"}, "en", {"", "non-empty"}, "en"),  # Empty and non-empty
        (["hello", "world"], "en", {"hello", "world"}, "en"),
        (["привет", "мир"], "ru", {"привет", "мир"}, "ru"),
        (["😊", "😂"], "en", {"😊", "😂"}, "en"),
        (["", " "], "en", {"", " "}, "en"),
        (["UPPER", "lower"], "en", {"UPPER", "lower"}, "en"),
        (["   leading", "trailing   "], "en", {"   leading", "trailing   "}, "en"),
        (["Γειά", "σου"], "el", {"Γειά", "σου"}, "el"),
        (["mixedCASE", "TEXT"], "en", {"mixedCASE", "TEXT"}, "en"),
        (["    "], "en", {"    "}, "en"),  # Strings with only spaces
        (["", "non-empty"], "en", {"", "non-empty"}, "en"),  # Empty and non-empty
    ],
)
def test_setlangstring_texts_and_lang_initialization(
    texts: Optional[Union[Set[str], list[str]]], lang: str, expected_texts: Set[str], expected_lang_str: str
) -> None:
    """
    Test the initialization of SetLangString with various sets of texts and languages.

    :param texts: The set of texts to initialize the SetLangString with.
    :param lang: The language code to initialize the SetLangString with.
    :param expected_texts: The expected set of texts after initialization.
    :param expected_lang_str: The expected language code after initialization.
    :return: None. Asserts if the texts and language are correctly initialized and represented.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    assert set_lang_string.texts == expected_texts, (
        f"Expected texts {expected_texts} but got {set_lang_string.texts} "
        f"when initializing with texts {texts} and language '{lang}'"
    )
    assert set_lang_string.lang == expected_lang_str, (
        f"Expected language '{expected_lang_str}' but got '{set_lang_string.lang}' "
        f"when initializing with language '{lang}'"
    )


@pytest.mark.parametrize(
    "invalid_texts, exception",
    [
        (["list", 123], TypeError),
        ({"set", 123}, TypeError),
        (["list", True], TypeError),
        ({"set", True}, TypeError),
        ("string", TypeError),
        (123, TypeError),
        (({"nested": "dict"},), TypeError),
        (["valid", ["nested"]], TypeError),  # Nested list
        ({"valid", ("nested",)}, TypeError),  # Tuple inside set
    ],
)
def test_setlangstring_invalid_texts_initialization(
    invalid_texts: Optional[Union[Set[str], list[str]]], exception: Exception
) -> None:
    """
    Test the initialization of SetLangString with invalid types for texts.

    :param invalid_texts: The invalid type of texts to initialize the SetLangString with.
    :param exception: The exception type that is expected to be raised.
    :param match: The regex pattern that the exception message is expected to match.
    :return: None. Asserts if the correct exception is raised with the expected message.
    """
    with pytest.raises(exception, match=TYPEERROR_MSG_SINGULAR):
        SetLangString(texts=invalid_texts)


@pytest.mark.parametrize(
    "invalid_lang, exception",
    [
        (123, TypeError),
        ([], TypeError),
        (set(), TypeError),
    ],
)
def test_setlangstring_invalid_lang_initialization(invalid_lang: str, exception: Exception) -> None:
    """
    Test the initialization of SetLangString with invalid types for lang.

    :param invalid_lang: The invalid type of language to initialize the SetLangString with.
    :param exception: The exception type that is expected to be raised.
    :param match: The regex pattern that the exception message is expected to match.
    :return: None. Asserts if the correct exception is raised with the expected message.
    """
    with pytest.raises(exception, match=TYPEERROR_MSG_SINGULAR):
        SetLangString(texts={"valid", "set"}, lang=invalid_lang)


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({" singleword "}, "en"),
        ({"UPPERCASE", "lowercase", "Numbers123"}, "en"),
        ({"Καλημέρα", "κόσμε"}, "el"),  # Greek characters
        ({"Привет", "мир"}, "ru"),  # Cyrillic characters
        ({"Emoji😊", "Symbols#@"}, "en"),
        # Additional valid but unusual usages
        ({" leading space", "trailing space "}, "en"),  # Leading and trailing spaces
        ({"MixedCASEusage", "anotherOne"}, "en"),  # Mixed case usage
        ({"", "  "}, "en"),  # Empty string and string with spaces
        ({"123", "@!#"}, "en"),  # Numbers and special characters
        ({"\nNewLine", "\tTab"}, "en"),  # Escape sequences
    ],
)
def test_setlangstring_unusual_but_valid_usage(texts: Set[str], lang: str) -> None:
    """
    Test SetLangString initialization and usage with unusual but valid texts and languages.

    :param texts: A set of strings representing the texts to be used for initialization.
    :param lang: A string representing the language code.
    :return: None. Asserts if the SetLangString instance does not correctly initialize or represent the texts and language.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    assert (
        set_lang_string.texts == texts
    ), f"Failed to initialize or represent texts correctly. Expected {texts}, got {set_lang_string.texts}."

    assert (
        set_lang_string.lang == lang
    ), f"Failed to initialize or represent the language correctly. Expected {lang}, got {set_lang_string.lang}."


@pytest.mark.parametrize(
    "texts",
    [
        {"hello", "world"},  # Valid usage
        set(),  # Empty set
    ],
)
def test_setlangstring_operation_on_itself(texts: Set[str]) -> None:
    """Test operations on SetLangString instance itself if applicable."""
    lang_string = SetLangString(texts=texts, lang="en")
    lang_string.texts = texts  # Re-assigning to itself
    assert lang_string.texts == texts, "Failed operation on itself with texts reassignment."


class TypeValidator:
    @staticmethod
    def validate_type_iterable(value, expected_type, item_type, optional=False):
        if optional and value is None:
            return
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type}, got {type(value)}")
        for item in value:
            if not isinstance(item, item_type):
                raise TypeError(
                    f"Invalid argument with value '{item}'. Expected '{item_type.__name__}', but got '{type(item).__name__}'."
                )


def test_texts_setter_with_list_of_strings():
    """
    Test that the `texts` setter correctly converts a list of strings to a set and validates the types.

    :raises AssertionError: If the assertion fails.
    """
    sls = SetLangString()
    sls.texts = ["hello", "world"]
    assert sls.texts == {"hello", "world"}, "The list of strings should be converted to a set of strings"


@pytest.mark.parametrize(
    "invalid_list, error_message",
    [
        (["hello", 123], "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        ([None, "world"], "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
    ],
)
def test_texts_setter_with_invalid_list_items(invalid_list: list[Optional[str]], error_message: str):
    """
    Test that the `texts` setter raises a TypeError when a list contains non-string items.

    :param invalid_list: A list of items to be set as texts.
    :type invalid_list: List[Optional[str]]
    :param error_message: The expected error message.
    :type error_message: str
    :raises TypeError: When the list contains non-string items.
    """
    sls = SetLangString()
    with pytest.raises(TypeError, match=error_message):
        sls.texts = invalid_list


def test_texts_setter_with_none():
    """
    Test that the `texts` setter correctly handles None by converting it to an empty set.

    :raises AssertionError: If the assertion fails.
    """
    sls = SetLangString()
    sls.texts = None
    assert sls.texts == set(), "None should be converted to an empty set"


def test_texts_setter_with_set_of_strings():
    """
    Test that the `texts` setter correctly accepts a set of strings and validates the types.

    :raises AssertionError: If the assertion fails.
    """
    sls = SetLangString()
    sls.texts = {"hello", "world"}
    assert sls.texts == {"hello", "world"}, "The set of strings should be correctly assigned"


@pytest.mark.parametrize(
    "invalid_set, error_message",
    [
        ({"hello", 123}, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        ({None, "world"}, "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
    ],
)
def test_texts_setter_with_invalid_set_items(invalid_set: Set[Optional[str]], error_message: str):
    """
    Test that the `texts` setter raises a TypeError when a set contains non-string items.

    :param invalid_set: A set of items to be set as texts.
    :type invalid_set: Set[Optional[str]]
    :param error_message: The expected error message.
    :type error_message: str
    :raises TypeError: When the set contains non-string items.
    """
    sls = SetLangString()
    with pytest.raises(TypeError, match=error_message):
        sls.texts = invalid_set
