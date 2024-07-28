from typing import Set

import pytest
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


def test_discard_langstring_removes_existing_langstring():
    """Test discarding a LangString that exists within the MultiLangString.

    :param langstring: The LangString to discard.
    :type langstring: LangString
    :return: None
    """
    langstring = LangString("Hello", "en")
    mls = MultiLangString({"en": {"Hello", "World"}})
    mls.discard_langstring(langstring)
    assert "Hello" not in mls.mls_dict["en"], "Expected 'Hello' to be removed from the 'en' language set."


def test_discard_langstring_nonexistent_does_nothing():
    """Test discarding a LangString that does not exist does not modify the MultiLangString.

    :param langstring: Nonexistent LangString to discard.
    :type langstring: LangString
    :return: None
    """
    langstring = LangString("Bonjour", "fr")
    mls = MultiLangString({"en": {"Hello"}})
    mls.discard_langstring(langstring)
    assert "Bonjour" not in mls.mls_dict.get(
        "fr", set()
    ), "Discarding a nonexistent LangString should not modify MultiLangString."


@pytest.mark.parametrize(
    "initial_contents, langstring, expected_contents",
    [
        ({"en": {"Hello", "World"}}, LangString("Hello", "en"), {"en": {"World"}}),
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, LangString("Bonjour", "fr"), {"en": {"Hello"}, "fr": set()}),
        ({"en": {"Hello"}}, LangString("Hola", "es"), {"en": {"Hello"}}),
        ({"de": {"Hallo"}, "en": {"Hello", "World"}}, LangString("Hello", "en"), {"de": {"Hallo"}, "en": {"World"}}),
        (
            {"en": {"Hello"}, "es": {"Hola"}, "fr": {"Bonjour"}},
            LangString("Bonjour", "fr"),
            {"en": {"Hello"}, "es": {"Hola"}, "fr": set()},
        ),
        (
            {"en": {"Hello"}},
            LangString("Hello", "en"),
            {"en": set()},
        ),  # Confirm removal leads to an empty set for the language
    ],
)
def test_discard_langstring_various_scenarios(
    initial_contents: dict[str, Set[str]], langstring: LangString, expected_contents: dict[str, Set[str]]
):
    """Test discarding LangString across various scenarios including existing and non-existing LangStrings.

    :param initial_contents: Initial contents of the MultiLangString.
    :param langstring: The LangString to discard.
    :param expected_contents: Expected contents of the MultiLangString after discarding.
    :type initial_contents: dict[str, Set[str]]
    :type langstring: LangString
    :type expected_contents: dict[str, Set[str]]
    :return: None
    """
    mls = MultiLangString(initial_contents)
    mls.discard_langstring(langstring)
    assert (
        mls.mls_dict == expected_contents
    ), f"Expected contents after discarding LangString {langstring} did not match."


def test_discard_langstring_with_invalid_type_raises_error():
    """Test that attempting to discard an invalid type instead of a LangString raises a TypeError.

    :param langstring: Invalid type to test.
    :type langstring: Any
    :return: None
    :raises TypeError: If the argument is not a LangString.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_langstring("not a LangString")  # Invalid type passed


@pytest.mark.parametrize(
    "langstring",
    [
        None,
        123,
    ],
)
def test_discard_langstring_with_null_and_invalid_types_raises_error(langstring):
    """
    Test that attempting to discard a null or an invalid type instead of a LangString raises appropriate errors.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_langstring(langstring)


def test_discard_langstring_empty_langstring():
    """
    Test discarding an empty LangString (i.e., a LangString with an empty string and language code).
    """
    langstring = LangString("", "")
    mls = MultiLangString({"": {""}})
    mls.discard_langstring(langstring)
    assert mls.mls_dict == {"": set()}, "Expected empty LangString to be removed."


def test_discard_langstring_unusual_but_valid_usage():
    """
    Test discarding a LangString from a language different than its content suggests, an unusual but valid usage.
    """
    langstring = LangString("Hello", "fr")  # 'Hello' typically an English word, marked as French
    mls = MultiLangString({"fr": {"Hello"}})
    mls.discard_langstring(langstring)
    assert "Hello" not in mls.mls_dict.get("fr", set()), "Expected 'Hello' to be removed from the 'fr' set."


def test_discard_langstring_clean_empty_lang_flag_effect():
    """
    Test the effect of the clean_empty arg on discard_langstring method, ensuring that languages with no remaining
    strings are removed from the MultiLangString instance.
    """

    langstring = LangString("Adieu", "fr")
    mls = MultiLangString({"fr": {"Adieu"}, "en": {"Goodbye"}})
    mls.discard_langstring(langstring, True)
    assert (
        "fr" not in mls.mls_dict
    ), "Expected 'fr' language to be removed after discarding its only string with clean_empty arg enabled."


def test_discard_langstring_without_clean_empty_lang_flag_effect():
    """
    Verify that without the clean_empty arg enabled, languages with no remaining strings are not removed.
    """
    langstring = LangString("Goodbye", "en")
    mls = MultiLangString({"en": {"Goodbye"}})
    mls.discard_langstring(langstring, True)
    assert "en" not in mls.mls_dict, "Expected 'en' language not to remain."


@pytest.mark.parametrize(
    "initial_contents, langstring, clean_empty, expected_contents",
    [
        # Case where language should be removed after discarding LangString, with clean_empty=True
        ({"en": {"Hello"}}, LangString("Hello", "en"), True, {}),
        # Case where language remains but is empty, with clean_empty=False
        ({"en": {"Hello"}}, LangString("Hello", "en"), False, {"en": set()}),
    ],
)
def test_discard_langstring_with_clean_empty(
    initial_contents: dict[str, Set[str]],
    langstring: LangString,
    clean_empty: bool,
    expected_contents: dict[str, Set[str]],
):
    """Test discarding a LangString with the clean_empty parameter affecting the final state of mls_dict.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param langstring: The LangString to be discarded.
    :param clean_empty: Determines whether empty language sets are removed after discarding.
    :param expected_contents: Expected state of mls_dict after discarding the LangString.
    :type initial_contents: dict
    :type langstring: LangString
    :type clean_empty: bool
    :type expected_contents: dict
    """
    mls = MultiLangString(initial_contents)
    mls.discard_langstring(langstring, clean_empty=clean_empty)
    assert mls.mls_dict == expected_contents, "mls_dict did not match expected contents after discarding LangString."
