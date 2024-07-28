import pytest
from langstring import Converter
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_text, input_lang, expected_dict, expected_pref_lang",
    [
        ("Hello", "en", {"en": {"Hello"}}, "en"),
        ("Bonjour", "fr", {"fr": {"Bonjour"}}, "fr"),
        ("", "", {"": {""}}, ""),
        (None, "x", {"x": {""}}, "x"),
        ("z", None, {"": {"z"}}, ""),
        (None, None, {"": {""}}, ""),
        ("Hola", "", {"": {"Hola"}}, ""),
        ("", "en", {"en": {""}}, "en"),
        ("   Spaced   ", "en", {"en": {"   Spaced   "}}, "en"),
        ("Γειά σου", "el", {"el": {"Γειά σου"}}, "el"),  # Greek
        ("Привет", "ru", {"ru": {"Привет"}}, "ru"),  # Cyrillic
        ("😊", "emoji", {"emoji": {"😊"}}, "emoji"),  # Emoji as text
        ("Hello", "EN", {"EN": {"Hello"}}, "EN"),  # Uppercase language code
        (" hello ", "en", {"en": {" hello "}}, "en"),  # Leading and trailing spaces
        ("HELLO", "en", {"en": {"HELLO"}}, "en"),  # Uppercase text
        ("<script>alert('XSS')</script>", "en", {"en": {"<script>alert('XSS')</script>"}}, "en"),  # Special characters
    ],
)
def test_from_langstring_to_multilangstring_valid_cases(
    input_text: str, input_lang: str, expected_dict: dict, expected_pref_lang: str
):
    """
    Test `from_langstring_to_multilangstring` with valid input cases.

    :param input_text: The text of the LangString to convert.
    :param input_lang: The language of the LangString to convert.
    :param expected_dict: The expected dictionary representation of the resulting MultiLangString.
    :param expected_pref_lang: The expected preferred language of the resulting MultiLangString.
    """
    lang_string = LangString(input_text, input_lang)
    result = Converter.from_langstring_to_multilangstring(lang_string)

    assert isinstance(result, MultiLangString), "Result should be an instance of MultiLangString"
    assert result.mls_dict == expected_dict, f"Expected dict representation {expected_dict}, got {result.mls_dict}"
    assert (
        result.pref_lang == expected_pref_lang
    ), f"Expected preferred language '{expected_pref_lang}', got '{result.pref_lang}'"


@pytest.mark.parametrize("input_arg", [123, 4.56, True, None, [], {}])
def test_from_langstring_to_multilangstring_invalid_type(input_arg):
    """
    Test `from_langstring_to_multilangstring` with invalid types of input.

    :param input_arg: The input argument of invalid type.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_langstring_to_multilangstring(input_arg)


def test_from_langstring_to_multilangstring_empty_langstring():
    """
    Test `from_langstring_to_multilangstring` with an empty LangString.
    """
    lang_string = LangString("", "")
    result = Converter.from_langstring_to_multilangstring(lang_string)

    assert isinstance(result, MultiLangString), "Result should be an instance of MultiLangString"
    assert result.mls_dict == {"": {""}}, "Expected dict representation with empty text and lang"
    assert result.pref_lang == "", "Expected preferred language to be empty"


def test_from_langstring_to_multilangstring_unusual_valid_usage():
    """
    Test `from_langstring_to_multilangstring` with unusual, but valid usage.
    """
    # Assuming unusual usage can mean creating a LangString with unconventional language codes or text.
    lang_string = LangString("∆§∆§∆", "xx-lolspeak")
    result = Converter.from_langstring_to_multilangstring(lang_string)

    assert "xx-lolspeak" in result.mls_dict, "Expected 'xx-lolspeak' as a language in the result"
    assert "∆§∆§∆" in result.mls_dict["xx-lolspeak"], "Expected '∆§∆§∆' as text in the result for 'xx-lolspeak'"
