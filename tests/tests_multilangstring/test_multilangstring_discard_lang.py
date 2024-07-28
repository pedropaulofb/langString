import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_contents, lang_to_discard, expected_contents",
    [
        ({"en": {"Hello", "World"}, "fr": {"Bonjour"}}, "en", {"fr": {"Bonjour"}}),
        ({"en": {"Hello"}, "fr": {"Bonjour", "Salut"}, "es": {"Hola"}}, "fr", {"en": {"Hello"}, "es": {"Hola"}}),
        ({"en": {"Hello"}}, "es", {"en": {"Hello"}}),  # Discard a non-existing language
        ({}, "en", {}),  # Discard from an empty MultiLangString
        (
            {"en": {"Hello"}, "de": {"Hallo"}, "fr": {"Bonjour"}},
            "de",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),  # Discard one of multiple existing languages
        (
            {"en": set(), "fr": {"Bonjour"}},
            "en",
            {"fr": {"Bonjour"}},
        ),  # Discard a language with an empty set of texts
        (
            {"": {"AnonLangText"}, "en": {"Hello"}, "fr": {"Bonjour"}},
            "",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),  # Discard texts without a specified language
        ({"": {"NoLang"}, "en": {"Hello"}}, "", {"en": {"Hello"}}),  # Only discard entries without a language
        ({"": {"OnlyNoLangText"}}, "", {}),  # Discard the only language which is an empty string
        (
            {"en": {"Hello"}, "fr": {"Bonjour"}},
            "",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),  # Attempt to discard an empty string in a dict without it
    ],
)
def test_discard_lang_various_scenarios(initial_contents, lang_to_discard, expected_contents):
    """
    Test the `discard_lang` method across various scenarios, including discarding existing and non-existing languages.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param lang_to_discard: The language to discard.
    :param expected_contents: Expected contents of the MultiLangString after discarding the language.
    """
    mls = MultiLangString(initial_contents)
    mls.discard_lang(lang_to_discard)
    assert (
        mls.mls_dict == expected_contents
    ), "MultiLangString contents did not match expected after discarding a language."


def test_discard_lang_with_invalid_type():
    """
    Test that passing an invalid type to `discard_lang` raises a TypeError.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_lang(123)  # Invalid type passed


def test_discard_lang_with_null_value():
    """
    Test that attempting to discard a null (None) language raises an appropriate error.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_lang(None)  # Passing None as a language code
