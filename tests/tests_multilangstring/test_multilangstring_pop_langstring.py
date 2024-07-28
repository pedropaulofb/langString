import pytest
from langstring import LangString
from langstring import MultiLangString
from pytest import raises
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "init_dict, pop_text, pop_lang, expected_text, expected_lang, expected_remaining",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "Hello", "en", "Hello", "en", {"en": set(), "fr": {"Bonjour"}}),
        (
            {"en": {"Hello", "Goodbye"}, "fr": {"Bonjour"}},
            "Goodbye",
            "en",
            "Goodbye",
            "en",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        (
            {"en": {"Hello"}, "fr": {"Bonjour", "Au revoir"}},
            "Au revoir",
            "fr",
            "Au revoir",
            "fr",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        ({"de": {"Hallo"}, "fr": {"Bonjour"}}, "Bonjour", "fr", "Bonjour", "fr", {"de": {"Hallo"}, "fr": set()}),
        # Cases considering spaces, case insensitivity, and special characters
        ({"en": {" Hello "}, "fr": {"Bonjour"}}, " Hello ", "en", " Hello ", "en", {"en": set(), "fr": {"Bonjour"}}),
        ({"en": {"Hello"}, "gr": {"Γειά"}}, "Γειά", "GR", "Γειά", "GR", {"en": {"Hello"}, "gr": set()}),
        ({"en": {"Hello👋"}, "fr": {"Bonjour"}}, "Hello👋", "en", "Hello👋", "en", {"en": set(), "fr": {"Bonjour"}}),
        ({"en": {"Hello"}, "ru": {"Привет"}}, "Привет", "RU", "Привет", "RU", {"en": {"Hello"}, "ru": set()}),
    ],
)
def test_pop_langstring_existing_entry_parametrized(
    init_dict, pop_text, pop_lang, expected_text, expected_lang, expected_remaining
):
    """
    Test popping existing LangString entries from MultiLangString with various configurations.

    :param init_dict: Initial dictionary to create MultiLangString.
    :param pop_text: Text to pop from the MultiLangString.
    :param pop_lang: Language of the text to pop.
    :param expected_text: Expected text of the popped LangString.
    :param expected_lang: Expected language of the popped LangString.
    :param expected_remaining: Expected remaining entries in the MultiLangString after popping.
    :return: None
    """
    mls = MultiLangString(init_dict)
    popped_langstring = mls.pop_langstring(pop_text, pop_lang)
    assert isinstance(popped_langstring, LangString), "The popped object must be an instance of LangString."
    assert (
        popped_langstring.text == expected_text and popped_langstring.lang == expected_lang
    ), f"Popped LangString should have text '{expected_text}' and lang '{expected_lang}'."
    assert (
        mls.mls_dict == expected_remaining
    ), "The remaining entries in MultiLangString do not match the expected state."


@pytest.mark.parametrize(
    "text, lang",
    [
        ("Goodbye", "en"),  # Non-existing text in existing language
        ("Hello", "de"),  # Existing text in non-existing language
        ("Goodbye", "de"),  # Non-existing text in non-existing language
        ("こんにちは", "jp"),  # Non-existing text in non-standard language code
        ("Hello", "en-GB"),  # Existing text in valid but not specified language variant
        # Additional cases for non-existing texts considering case insensitivity and spaces
        (" HELLO ", "en"),  # Non-existing text with leading/trailing spaces in existing language
        ("HELLO", "en"),  # Non-Existing text in case-insensitive language code
        ("hello", "EN"),  # Non-Existing text in case-insensitive language code
        ("Χαίρετε", "gr"),  # Non-existing text in Greek
        ("Привет", "RU"),  # Existing text in Russian with uppercase language code
        ("Hello👋", "EN"),  # Non-existing text with emoji in case-insensitive language code
    ],
)
def test_pop_langstring_non_existing_text_parametrized(text, lang):
    """
    Test popping a non-existing text from MultiLangString with various text and language combinations.

    :param text: The text to attempt to pop.
    :param lang: The language code from which to attempt to pop the text.
    :return: None
    """
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
    new_mls = mls.pop_langstring(text, lang)
    assert new_mls is None, f"Expected None when popping non-existing text '{text}' from language '{lang}'"
    assert mls == MultiLangString(
        {"en": {"Hello"}, "fr": {"Bonjour"}}
    ), "The MultiLangString object should remain unchanged after attempting to pop a non-existing text."


def test_pop_langstring_invalid_text_type():
    """
    Test that passing an invalid text type (not str) to pop_langstring raises TypeError.

    :param None
    :return: None
    :raises TypeError: If the text parameter is not a string.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.pop_langstring(123, "en")  # 123 is not a valid text


@pytest.mark.parametrize("text,lang", [(None, "en"), ("Hello", None), (123, "en"), ("Hello", 123)])
def test_pop_langstring_invalid_arg_types(text, lang):
    """
    Test popping with invalid values for text and language, expecting ValueError or TypeError.

    :param text: Potentially invalid text value.
    :param lang: Potentially invalid language value.
    :return: None
    :raises ValueError: If text or language is None or empty, when respective flags are set.
    :raises TypeError: If text or language is not a string.
    """
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
    with pytest.raises((ValueError, TypeError), match=TYPEERROR_MSG_SINGULAR):
        mls.pop_langstring(text, lang)


@pytest.mark.parametrize(
    "text,lang,expected_result",
    [
        ("Very long text... (snipped)", "en", None),
        ("Hello", "special-characters-é", None),
    ],
)
def test_pop_langstring_edge_cases(text, lang, expected_result):
    """
    Test popping langstrings in edge cases including unusual but valid language codes.

    :param text: Text to be popped.
    :param lang: Language code, potentially unusual but valid.
    :param expected_result: Expected exception, if any.
    :return: None
    :raises Exception: Expected exception based on the test scenario.
    """
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "en-gb": {"Hello"}})
    result = mls.pop_langstring(text, lang)
    assert result is None
