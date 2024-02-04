import pytest

from langstring import Controller
from langstring import Converter
from langstring import LangString
from langstring import SetLangString
from langstring import SetLangStringFlag


def test_setlangstring_to_langstrings_with_multiple_texts():
    """
    Test converting a SetLangString with multiple texts to a list of LangStrings.
    """
    set_lang_string = SetLangString(texts={"Hello", "Hi"}, lang="en")
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    expected = [LangString("Hello", "en"), LangString("Hi", "en")]
    assert all(
        langstring in result for langstring in expected
    ), "setlangstring_to_langstrings should return LangStrings for all texts"


def test_setlangstring_to_langstrings_with_single_text():
    """
    Test converting a SetLangString with a single text to a list of LangStrings.
    """
    set_lang_string = SetLangString(texts={"Hello"}, lang="en")
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    expected = [LangString("Hello", "en")]
    assert result == expected, "setlangstring_to_langstrings should handle single text correctly"


@pytest.mark.parametrize("invalid_input", [123, 5.5, True, None, [], {}, "string", LangString("Hello", "en")])
def test_setlangstring_to_langstrings_invalid_type(invalid_input):
    """
    Test conversion with invalid input types, expecting a TypeError.

    :param invalid_input: An input of invalid type (not SetLangString).
    :return: None
    :raises TypeError: If input is not of type SetLangString.
    """
    with pytest.raises(TypeError, match="Argument '.+' must be of type 'SetLangString', but"):
        Converter.from_setlangstring_to_langstrings(invalid_input)


@pytest.mark.parametrize(
    "lang, expected_lang",
    [
        ("EN", "EN"),  # Test with uppercase language code
        ("en-gb", "en-gb"),  # Test with language subtag
    ],
)
def test_setlangstring_to_langstrings_language_preservation(lang: str, expected_lang: str):
    """Test that the language code is preserved in the conversion from SetLangString to LangStrings.

    :param lang: The language code of the SetLangString.
    :param expected_lang: The expected language code in the resulting LangStrings.
    :return: None
    """
    set_lang_string = SetLangString(texts={"Hello", "Bonjour"}, lang=lang)
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    assert all(
        langstring.lang == expected_lang for langstring in result
    ), "Language code should be preserved in each converted LangString"


@pytest.mark.parametrize(
    "texts",
    [
        ({"   ", "\n"}),  # Test texts that are only whitespace or newline
        ({"", " "}),  # Test empty string and a single space
    ],
)
def test_setlangstring_to_langstrings_whitespace_texts(texts: set[str]):
    """Test converting a SetLangString containing texts with whitespace or newline characters to LangStrings.

    :param texts: A set of text strings containing whitespace or newline characters.
    :return: None
    """
    set_lang_string = SetLangString(texts=texts, lang="en")
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    expected = [LangString(text, "en") for text in texts]
    assert all(
        any(langstring.text == expected_text.text for langstring in result) for expected_text in expected
    ), "All whitespace or newline texts should be correctly converted to LangStrings"


@pytest.mark.parametrize(
    "texts, expected_length",
    [
        ({"Hello", "hello", "HELLO"}, 3),  # Testing with unique case-sensitive texts
    ],
)
def test_setlangstring_to_langstrings_unique_case_sensitive_texts(texts: set[str], expected_length: int):
    """Test the handling of case-sensitive unique texts in the conversion from SetLangString to LangStrings.

    :param texts: A set of text strings with case-sensitive variations.
    :param expected_length: The expected number of unique LangStrings based on case sensitivity.
    :return: None
    """
    set_lang_string = SetLangString(texts=texts, lang="en")
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    assert len(result) == expected_length, "Each case-sensitive text should result in a unique LangString"


def test_setlangstring_to_langstrings_empty_set():
    """Test converting an empty SetLangString to an empty list of LangStrings.

    :return: None
    """
    set_lang_string = SetLangString(texts=set(), lang="en")
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    assert not result, "Converting an empty SetLangString should result in an empty list of LangStrings"


@pytest.mark.parametrize(
    "lang, flag",
    [
        (" en ", SetLangStringFlag.STRIP_LANG),  # Assuming STRIP_LANG trims whitespace from language codes
    ],
)
def test_setlangstring_to_langstrings_flag_effects(lang: str, flag: SetLangStringFlag):
    """Test the effects of SetLangString flags on the lang attribute during conversion to LangStrings.

    :param lang: A sample language code to include in the SetLangString.
    :param flag: The SetLangString flag to test.
    :param expected_effect: Whether the flag is expected to have an effect on the lang attribute.
    :return: None
    """
    Controller.set_flag(flag, True)
    set_lang_string = SetLangString(texts={"Text"}, lang=lang)
    result = Converter.from_setlangstring_to_langstrings(set_lang_string)
    Controller.reset_flags()  # Reset flags to avoid side effects

    trimmed_lang = lang.strip()  # Expected lang attribute after applying STRIP_LANG
    assert all(
        langstring.lang == trimmed_lang for langstring in result
    ), f"Flag {flag.name} did not have the expected effect on lang"
