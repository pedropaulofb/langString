from typing import Optional

import pytest
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_dict, text, lang, expected_output",
    [
        ({"en": {"Hello", "World"}, "fr": {"Bonjour"}}, "Hello", "en", LangString(text="Hello", lang="en")),
        ({"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}}, "Monde", "fr", LangString(text="Monde", lang="fr")),
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "Hola", "es", LangString(lang="es")),
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "Hello", "fr", LangString(lang="fr")),
        ({"ru": {"Привет"}}, "Привет", "ru", LangString(text="Привет", lang="ru")),
        ({"emoji": {"😊", "😂"}}, "😊", "emoji", LangString(text="😊", lang="emoji")),
        ({"en": {" "}}, " ", "en", LangString(text=" ", lang="en")),  # Testing with whitespace
        (
            {"gr": {"Γειά σου"}},
            "Γειά σου",
            "gr",
            LangString(text="Γειά σου", lang="gr"),
        ),  # Non-Latin characters (Greek)
        ({"cy": {"Привет"}}, "Привет", "cy", LangString(text="Привет", lang="cy")),  # Cyrillic characters
        ({"special": {"@#$%"}}, "@#$%", "special", LangString(text="@#$%", lang="special")),  # Special characters
    ],
)
def test_get_langstring_valid_cases(
    input_dict: dict, text: str, lang: str, expected_output: Optional[LangString]
) -> None:
    """Test get_langstring method with various valid input cases.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and sets of texts.
    :param text: The text to search for within a specific language.
    :param lang: The language code to search the text in.
    :param expected_output: The expected LangString output or None if not found.
    :return: None
    """
    mls = MultiLangString(input_dict)
    result = mls.get_langstring(text=text, lang=lang)
    assert result == expected_output, f"Expected {expected_output} for text '{text}' in lang '{lang}', got {result}"


@pytest.mark.parametrize(
    "lang, text",
    [
        ("en", None),
        (None, "Hello"),
        (123, "Hello"),
        ("en", 123),
    ],
)
def test_get_langstring_invalid_inputs(lang, text) -> None:
    """Test get_langstring with invalid types and values for lang and text parameters.

    :param lang: The language code, which might be invalid.
    :param text: The text to search for, which might be invalid.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.get_langstring(text=text, lang=lang)


@pytest.mark.parametrize(
    "input_dict, text, lang, expected_output",
    [
        (
            {"mixedCase": {"HelloWorld"}},
            "HelloWorld",
            "mixedCase",
            LangString(text="HelloWorld", lang="mixedCase"),
        ),  # Mixed case lang
        ({"": {"emptyKey"}}, "emptyKey", "", LangString(text="emptyKey", lang="")),  # Empty string as lang
    ],
)
def test_get_langstring_edge_cases(
    input_dict: dict, text: str, lang: str, expected_output: Optional[LangString]
) -> None:
    """Test get_langstring method with edge cases including empty and mixed case language codes.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and sets of texts.
    :param text: The text to search for within a specific language.
    :param lang: The language code to search the text in, which may include unusual cases like empty strings or mixed cases.
    :param expected_output: The expected LangString output or None if not found.
    :return: None
    """
    mls = MultiLangString(input_dict)
    result = mls.get_langstring(text=text, lang=lang)
    assert result == expected_output, f"Expected {expected_output} for text '{text}' in lang '{lang}', got {result}"
