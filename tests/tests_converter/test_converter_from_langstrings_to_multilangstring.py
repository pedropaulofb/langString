import pytest
from langstring import Converter
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_langstrings, expected_dict, expected_pref_langs",
    [
        ([LangString("Hello", "en"), LangString("Bonjour", "fr")], {"en": {"Hello"}, "fr": {"Bonjour"}}, ["en", "fr"]),
        ([LangString("", "en"), LangString(" ", "fr")], {"en": {""}, "fr": {" "}}, ["en", "fr"]),
        ([LangString("😊", "emoji"), LangString("🚀", "emoji")], {"emoji": {"😊", "🚀"}}, ["emoji"]),
        ([LangString("Hello", "en"), LangString("World", "en")], {"en": {"Hello", "World"}}, ["en"]),
        ([], {}, []),
        (
            [LangString(" Привет ", "ru"), LangString("Γειά σου", "el")],
            {"ru": {" Привет "}, "el": {"Γειά σου"}},
            ["ru", "el"],
        ),
        ([LangString("   ", "en"), LangString("\t", "de")], {"en": {"   "}, "de": {"\t"}}, ["en", "de"]),
        ([LangString("lowercase", "en"), LangString("UPPERCASE", "EN")], {"en": {"lowercase", "UPPERCASE"}}, ["en"]),
        ([LangString("MixedCase", "en"), LangString("mIXEDcASE", "EN")], {"en": {"MixedCase", "mIXEDcASE"}}, ["en"]),
        (
            [LangString("στοιχείο", "el"), LangString("элемент", "ru")],
            {"el": {"στοιχείο"}, "ru": {"элемент"}},
            ["el", "ru"],
        ),
        ([LangString("!@#$%", "spec"), LangString("<>[]", "spec")], {"spec": {"!@#$%", "<>[]"}}, ["spec"]),
    ],
)
def test_from_langstrings_to_multilangstring_valid_cases(
    input_langstrings: list[LangString], expected_dict: dict, expected_pref_langs: list[str]
):
    """
    Test `from_langstrings_to_multilangstring` with valid lists of LangStrings.

    :param input_langstrings: A list of LangString objects to be converted.
    :param expected_dict: The expected dictionary representation of the resulting MultiLangString.
    :param expected_pref_langs: The expected list of preferred languages in the resulting MultiLangString.
    """
    result = Converter.from_langstrings_to_multilangstring(input_langstrings)

    assert isinstance(result, MultiLangString), "The result should be an instance of MultiLangString"
    assert result.mls_dict == expected_dict, f"Expected dict representation {expected_dict}, got {result.mls_dict}"
    for lang in expected_pref_langs:
        assert lang in result.mls_dict, f"Expected language '{lang}' to be in the result"


@pytest.mark.parametrize(
    "input_arg",
    [
        123,
        "string",
        True,
        [None, "test"],
        [LangString("Hello", "en"), 123],
        [None],
        [LangString("valid", "en"), None],
        ["Invalid Type"],
        [LangString("😊", "emoji"), "Not a LangString"],
    ],
)
def test_from_langstrings_to_multilangstring_invalid_type(input_arg):
    """
    Test `from_langstrings_to_multilangstring` with invalid types of input.

    :param input_arg: The input argument of invalid type.
    :param match_error: The error message expected to match when the exception is raised.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_langstrings_to_multilangstring(input_arg)


def test_from_langstrings_to_multilangstring_mixed_languages():
    """
    Test `from_langstrings_to_multilangstring` ensuring it can handle a mix of languages correctly.
    """
    input_langstrings = [LangString("Hello", "en"), LangString("Hola", "es"), LangString("Bonjour", "fr")]
    result = Converter.from_langstrings_to_multilangstring(input_langstrings)

    expected_langs = ["en", "es", "fr"]
    assert all(lang in result.mls_dict for lang in expected_langs), "The result should contain all expected languages"


def test_from_langstrings_to_multilangstring_identical_texts_different_langs():
    """
    Test `from_langstrings_to_multilangstring` with identical texts across different languages.
    """
    input_langstrings = [LangString("Test", "en"), LangString("Test", "fr")]
    result = Converter.from_langstrings_to_multilangstring(input_langstrings)

    assert "en" in result.mls_dict and "fr" in result.mls_dict, "Both languages should be present in the result"
    assert result.mls_dict["en"] == {"Test"} and result.mls_dict["fr"] == {
        "Test"
    }, "Identical texts should be correctly attributed to their respective languages"


@pytest.mark.parametrize(
    "input_langstrings, expected_dict, expected_pref_langs",
    [
        # Unusual but valid usage: Same text in different languages
        ([LangString("Yes", "en"), LangString("Yes", "fr")], {"en": {"Yes"}, "fr": {"Yes"}}, ["en", "fr"]),
        # Edge case: Texts with leading/trailing spaces in different languages
        (
            [LangString(" hello ", "en"), LangString(" bonjour ", "fr")],
            {"en": {" hello "}, "fr": {" bonjour "}},
            ["en", "fr"],
        ),
        # Unusual but valid usage: Mixed cases in language codes
        ([LangString("Hello", "EN"), LangString("Hola", "es")], {"EN": {"Hello"}, "es": {"Hola"}}, ["EN", "es"]),
        # Edge case: Multiple identical texts in the same language
        ([LangString("Repeat", "en"), LangString("Repeat", "en")], {"en": {"Repeat"}}, ["en"]),
        # Testing with special characters and different charset
        (
            [LangString("特殊字符", "zh"), LangString("спецсимволы", "ru")],
            {"zh": {"特殊字符"}, "ru": {"спецсимволы"}},
            ["zh", "ru"],
        ),
    ],
)
def test_from_langstrings_to_multilangstring_additional_valid_cases(
    input_langstrings, expected_dict, expected_pref_langs
):
    """Test `from_langstrings_to_multilangstring` with additional valid cases including edge cases and unusual but valid usages."""
    result = Converter.from_langstrings_to_multilangstring(input_langstrings)
    assert isinstance(result, MultiLangString), "The result should be an instance of MultiLangString"
    assert result.mls_dict == expected_dict, f"Expected {expected_dict}, got {result.mls_dict}"
    for lang in expected_pref_langs:
        assert lang in result.mls_dict, f"Expected language '{lang}' in result"
