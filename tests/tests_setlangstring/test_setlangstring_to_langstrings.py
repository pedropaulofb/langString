import pytest
from langstring.langstring import LangString
from langstring.setlangstring import SetLangString


@pytest.mark.parametrize(
    "texts, lang, expected",
    [
        ({"Hello", "World"}, "en", [LangString("Hello", "en"), LangString("World", "en")]),
        (set(), "en", []),
        ({"こんにちは", "世界"}, "ja", [LangString("こんにちは", "ja"), LangString("世界", "ja")]),
        ({"Hello"}, "", [LangString("Hello", "")]),
        ({"Mixed", "Language"}, "fr", [LangString("Mixed", "fr"), LangString("Language", "fr")]),
    ],
)
def test_to_langstrings_various_texts(texts: set[str], lang: str, expected: list[LangString]):
    """
    Test the `to_langstrings` method for converting SetLangString texts to a list of LangString objects.

    :param texts: A set of strings to be converted.
    :param lang: The language code to be associated with each text.
    :param expected: The expected list of LangString objects.
    :return: Asserts if the conversion results in the expected list of LangString objects.
    """
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    # Sort results and expected by text to ensure order doesn't affect comparison
    sorted_result = sorted(result, key=lambda x: x.text)
    sorted_expected = sorted(expected, key=lambda x: x.text)
    assert sorted_result == sorted_expected, "Conversion to LangStrings did not match expected results."


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"", "   "}, "en"),
        ({"NoLang"}, ""),
    ],
)
def test_to_langstrings_edge_cases(texts: set[str], lang: str):
    """
    Test the `to_langstrings` method with edge cases, including empty strings and whitespaces.

    :param texts: A set of strings including edge cases to be converted.
    :param lang: The language code to be associated with each text.
    :return: Asserts if the conversion handles edge cases correctly.
    """
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert all(isinstance(ls, LangString) for ls in result), "Not all items in the result are LangString instances."
    assert all(ls.lang == lang for ls in result), "Language code mismatch in the converted LangString objects."


def test_to_langstrings_preserves_uniqueness():
    """
    Ensure that `to_langstrings` preserves the uniqueness of the SetLangString's texts when converting.

    :return: Asserts if the uniqueness of texts is preserved in the conversion.
    """
    texts = {"Unique", "Unique"}
    lang = "en"
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert len(result) == 1, "Conversion did not preserve uniqueness of texts."


@pytest.mark.parametrize("lang", ["en", "ja", ""])
def test_to_langstrings_with_different_languages(lang: str):
    """
    Test the `to_langstrings` method with various language codes.

    :param lang: The language code to test.
    :return: Asserts if the conversion correctly assigns the language code to the LangString objects.
    """
    texts = {"LanguageTest"}
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert all(ls.lang == lang for ls in result), f"Language code '{lang}' not correctly assigned in conversion."


def test_to_langstrings_empty_setlangstring():
    """
    Test the `to_langstrings` method on an empty SetLangString instance.

    :return: Asserts if the conversion correctly returns an empty list for an empty SetLangString.
    """
    set_lang_string = SetLangString()
    result = set_lang_string.to_langstrings()
    assert result == [], "Conversion of an empty SetLangString did not return an empty list."


@pytest.mark.parametrize(
    "texts, lang, expected_lang",
    [
        ({"Hello", "World"}, "123", "123"),
        ({"Text"}, "NonStandardLangCode", "NonStandardLangCode"),
    ],
)
def test_to_langstrings_non_standard_languages(texts: set[str], lang: str, expected_lang: str):
    """
    Test the `to_langstrings` method with non-standard but valid language codes.

    :param texts: A set of strings to be converted.
    :param lang: A non-standard language code.
    :param expected_lang: The expected language code in the LangString objects.
    :return: Asserts if non-standard language codes are handled correctly.
    """
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert all(ls.lang == expected_lang for ls in result), "Non-standard language codes were not handled correctly."


@pytest.mark.parametrize(
    "texts, lang, expected_length, expected_texts_contain",
    [
        ({" ", "\t", "\n"}, "en", 3, {" ", "\t", "\n"}),
        ({"caseSensitive", "CaseSensitive"}, "en", 2, {"caseSensitive", "CaseSensitive"}),
        ({"hello"}, "EN", 1, {"hello"}),
        ({"special!@#$%^&*()"}, "en", 1, {"special!@#$%^&*()"}),
        ({"long" * 1000}, "en", 1, {"long" * 1000}),
    ],
)
def test_to_langstrings_advanced_cases(
    texts: set[str], lang: str, expected_length: int, expected_texts_contain: set[str]
):
    """
    Test the `to_langstrings` method with advanced cases including whitespace, case sensitivity, special characters, and long strings.

    :param texts: A set of strings to be converted.
    :param lang: The language code.
    :param expected_length: The expected number of LangString objects.
    :param expected_texts_contain: A set containing expected texts to verify presence in the result.
    :return: Asserts if the advanced cases are handled correctly.
    """
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert len(result) == expected_length, f"Expected {expected_length} LangStrings, got {len(result)}"
    for expected_text in expected_texts_contain:
        assert any(ls.text == expected_text for ls in result), f"Expected text '{expected_text}' not found in result."


@pytest.mark.parametrize("lang", ["EN", "en"])
def test_to_langstrings_language_case_sensitivity(lang: str):
    """
    Test the `to_langstrings` method with language codes in different cases to check for case sensitivity.

    :param lang: The language code in different cases.
    :return: Asserts if language codes are handled in a case-sensitive manner.
    """
    texts = {"LanguageCaseTest"}
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_langstrings()
    assert all(
        ls.lang == lang for ls in result
    ), f"Language code '{lang}' not correctly assigned in a case-sensitive manner."
