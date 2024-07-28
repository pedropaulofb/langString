from typing import Optional

import pytest
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_data, lang_to_pop, expected_pop_result, expected_remaining_data",
    [
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}},
            "en",
            ("en", {"Hello", "World"}),
            {"fr": {"Bonjour", "Monde"}},
        ),
        (
            {"de": {"Hallo", "Welt"}, "es": {"Hola", "Mundo"}},
            "es",
            ("es", {"Hola", "Mundo"}),
            {"de": {"Hallo", "Welt"}},
        ),
        ({"it": {"Ciao", "Mondo"}}, "it", ("it", {"Ciao", "Mondo"}), {}),
        (
            {"jp": {"こんにちは", "世界"}, "kr": {"안녕하세요", "세계"}, "cn": {"你好", "世界"}},
            "kr",
            ("kr", {"안녕하세요", "세계"}),
            {"jp": {"こんにちは", "世界"}, "cn": {"你好", "世界"}},
        ),
        # Test with empty strings and spaces
        ({"  ": {"   "}}, "  ", ("  ", {"   "}), {}),
        # Test with different case sensitivity
        (
            {"EN": {"HELLO", "WORLD"}, "en": {"hello", "world"}},
            "EN",
            ("EN", {"world", "hello", "HELLO", "WORLD"}),
            {},
        ),
        # Test with Greek and Cyrillic characters, and emojis
        (
            {"el": {"Γειά", "Κόσμος"}, "ru": {"Привет", "Мир"}, "emoji": {"😊", "🌍"}},
            "el",
            ("el", {"Γειά", "Κόσμος"}),
            {"ru": {"Привет", "Мир"}, "emoji": {"😊", "🌍"}},
        ),
        # Test with special characters
        ({"special": {"#", "@", "!", "*"}}, "special", ("special", {"#", "@", "!", "*"}), {}),
    ],
)
def test_pop_setlangstring_existing_language_parametrized(
    initial_data: dict[str, set[str]],
    lang_to_pop: str,
    expected_pop_result: tuple,
    expected_remaining_data: dict[str, set[str]],
):
    """
    Test that pop_setlangstring correctly removes and returns a SetLangString for an existing language, across various scenarios.
    :param initial_data: The initial data to populate the MultiLangString with.
    :param lang_to_pop: The language code to pop from the MultiLangString.
    :param expected_pop_result: The expected result of the pop operation, as a tuple of language code and set of texts.
    :param expected_remaining_data: The expected remaining data in the MultiLangString after the pop operation.
    :return: None
    """
    mls = MultiLangString(initial_data)
    sls: Optional[SetLangString] = mls.pop_setlangstring(lang_to_pop)
    assert (
        sls is not None and sls.lang == expected_pop_result[0] and sls.texts == expected_pop_result[1]
    ), f"pop_setlangstring should return a SetLangString with language '{lang_to_pop}' and correct texts."
    assert (
        mls.mls_dict == expected_remaining_data
    ), f"After popping language '{lang_to_pop}', remaining data should match expected data."


@pytest.mark.parametrize(
    "initial_data, non_existing_lang",
    [
        ({"en": {"Hello", "World"}}, "de"),
        ({"fr": {"Bonjour", "Monde"}}, "es"),
        ({}, "en"),  # Testing on an empty MultiLangString
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "jp"),
        # Test with spaces and special characters as non-existing languages
        ({"en": {"Hello", "World"}}, " "),
        ({"en": {"Hello", "World"}}, "@"),
        # Test with emojis and non-Latin scripts as non-existing languages
        ({"en": {"Hello", "World"}}, "😊"),
        ({"en": {"Hello", "World"}}, "Γειά"),
    ],
)
def test_pop_setlangstring_non_existing_language_parametrized(initial_data, non_existing_lang):
    """
    Test that pop_setlangstring returns None for various non-existing languages across different initial data sets.
    :param initial_data: The initial data to populate the MultiLangString with.
    :param non_existing_lang: The non-existing language code to attempt to pop from the MultiLangString.
    :return: None
    """
    mls = MultiLangString(initial_data)
    sls = mls.pop_setlangstring(non_existing_lang)
    assert sls is None, f"pop_setlangstring should return None for a non-existing language '{non_existing_lang}'."


@pytest.mark.parametrize("lang", [None, 123, 5.5, [], {}, True])
def test_pop_setlangstring_invalid_language_type(lang):
    """
    Test that pop_setlangstring raises TypeError for invalid language types.
    :param lang: Invalid language type.
    :return: None
    :raises TypeError: If the language type is not str.
    """
    mls = MultiLangString({"en": {"Hello", "World"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.pop_setlangstring(lang)


def test_pop_setlangstring_empty_language():
    """
    Test that pop_setlangstring behaves correctly when attempting to pop an empty language entry.
    :return: None
    """
    mls = MultiLangString({"en": set(), "fr": {"Bonjour"}})
    sls = mls.pop_setlangstring("en")
    assert (
        sls is not None and sls.lang == "en" and len(sls.texts) == 0
    ), "pop_setlangstring should return a SetLangString with an empty text set for an empty language."


def test_pop_setlangstring_after_adding_text():
    """
    Test the pop_setlangstring method after adding text to ensure it pops the updated SetLangString.
    :return: None
    """
    mls = MultiLangString()
    mls.add_entry("Hello", "en")
    mls.add_entry("World", "en")
    sls = mls.pop_setlangstring("en")
    assert sls.texts == {
        "Hello",
        "World",
    }, "pop_setlangstring should return the updated SetLangString after new texts are added."
    assert sls.lang == "en"


@pytest.mark.parametrize(
    "lang, expected_exception",
    [
        (None, TypeError),
    ],
)
def test_pop_setlangstring_invalid_or_empty_language_code(lang, expected_exception):
    """
    Test that pop_setlangstring raises the correct exception for invalid or empty language codes.
    :param lang: The language code to test with, which could be invalid or empty.
    :param expected_exception: The type of exception expected to be raised.
    :param expected_message: The expected error message.
    :return: None
    """
    mls = MultiLangString({"en": {"Hello", "World"}})
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.pop_setlangstring(lang)


def test_pop_setlangstring_unusual_valid_usage():
    """
    Test unusual but valid usage of pop_setlangstring, such as popping a language after modifying its SetLangString directly.
    :return: None
    """
    mls = MultiLangString({"en": {"Hello", "World"}})
    mls.mls_dict["en"].add("Greetings")
    sls = mls.pop_setlangstring("en")
    assert sls.texts == {"Hello", "World", "Greetings"}, "Expected modified SetLangString to be popped with new entry."


def test_pop_setlangstring_self_operation():
    """
    Test pop_setlangstring method's behavior when attempting to pop a language and re-insert it into the same MultiLangString.
    :return: None
    """
    mls = MultiLangString({"en": {"Hello"}})
    sls = mls.pop_setlangstring("en")
    assert sls == SetLangString(texts={"Hello"}, lang="en"), "Expected non-None SetLangString after pop."
    assert mls == MultiLangString(mls_dict={}, pref_lang="en"), "Expected 'en' to be re-inserted correctly."
    mls.add_setlangstring(sls)
    assert sls == SetLangString(texts={"Hello"}, lang="en"), "Expected non-None SetLangString after pop."
    assert mls == MultiLangString({"en": {"Hello"}}), "Expected 'en' to be re-inserted correctly."
