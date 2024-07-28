import pytest
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, expected",
    [
        ({"Hello", "Hi"}, "en", True),
        ({"Bonjour", "Salut"}, "fr", False),
        ({"Hola"}, "es", True),
        ({"Ciao"}, "it", False),
        ({"こんにちは"}, "jp", False),  # Non-Latin script
        ({"Hello", ""}, "en", False),  # Includes empty string as a text
        ({" "}, "en", False),  # Text only contains a space
    ],
)
def test_contains_setlangstring_with_various_languages_and_texts(texts: set, lang: str, expected: bool):
    """
    Test if MultiLangString.contains_setlangstring correctly identifies the presence of a SetLangString
    in various languages and text combinations.

    :param texts: A set of texts to be encapsulated in a SetLangString.
    :param lang: The language code for the SetLangString.
    :param expected: The expected result (True if all texts in SetLangString should be found, False otherwise).
    """
    mls = MultiLangString({"en": {"Hello", "Hi"}, "es": {"Hola", "Adiós"}})
    sls = SetLangString(texts, lang)
    assert mls.contains_setlangstring(sls) == expected, (
        f"Expected {'to find' if expected else 'not to find'} all texts from SetLangString with language '{lang}' "
        f"and texts {texts} in MultiLangString."
    )


@pytest.mark.parametrize(
    "invalid_type",
    [
        123,
        [{"test": "value"}],
        None,
        "string",  # A single string instead of a SetLangString
        {},  # An empty dictionary
        True,  # A boolean value
    ],
)
def test_contains_setlangstring_with_invalid_type(invalid_type):
    """
    Test MultiLangString.contains_setlangstring with invalid type arguments, expecting a TypeError.

    :param invalid_type: An invalid type to pass to contains_setlangstring, expecting a TypeError.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.contains_setlangstring(invalid_type)


def test_contains_setlangstring_with_empty_setlangstring():
    """
    Test if MultiLangString.contains_setlangstring correctly handles an empty SetLangString.
    An empty SetLangString should always return False, as it technically contains no texts to check for.
    """
    mls = MultiLangString({"en": {"Hello", "Hi"}})
    sls = SetLangString(set(), "en")
    assert mls.contains_setlangstring(sls), "Expected to not find an empty SetLangString in MultiLangString."


def test_contains_setlangstring_with_nonexistent_language():
    """
    Test if MultiLangString.contains_setlangstring correctly returns False when the SetLangString's language
    does not exist in the MultiLangString instance.
    """
    mls = MultiLangString({"en": {"Hello", "Hi"}})
    sls = SetLangString({"Hola"}, "es")
    assert (
        mls.contains_setlangstring(sls) is False
    ), "Expected to not find SetLangString with a non-existent language 'es' in MultiLangString."


def test_contains_setlangstring_empty_multi_lang_string():
    """
    Test MultiLangString.contains_setlangstring behavior with an empty MultiLangString instance.
    """
    mls = MultiLangString()
    sls = SetLangString({"Hello"}, "en")
    assert not mls.contains_setlangstring(sls), "Empty MultiLangString should not contain any SetLangString."


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"Hello", "Hi"}, "en"),  # Large number of texts
        ({"A" * 1000}, "en"),  # Extremely large text
        (set("abcdefghijklmnopqrstuvwxyz"), "en"),  # Single characters as texts
        ({"Hello", "Hello", "Hello"}, "en"),  # Repetitive texts
    ],
)
def test_contains_setlangstring_edge_cases(texts: set, lang: str):
    """
    Test edge cases for MultiLangString.contains_setlangstring.
    """
    mls = MultiLangString({"en": texts})
    sls = SetLangString(texts, lang)
    assert mls.contains_setlangstring(sls), "MultiLangString should contain the SetLangString in edge cases."
