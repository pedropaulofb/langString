import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag


@pytest.mark.parametrize(
    "input_dict, expected_result",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, ["en", "fr"]),
        ({"EN": {"Hello"}, "FR": {"Bonjour"}}, ["EN", "FR"]),
        ({}, []),
        ({"": {" "}}, [""]),  # Empty key with whitespace value
        ({"en": {"Hello "}, "fr": {" Bonjour"}}, ["en", "fr"]),  # Values with leading/trailing spaces
        ({"ру": {"Привет"}, "ελ": {"Γειά"}}, ["ру", "ελ"]),  # Cyrillic and Greek characters
        ({"🌎": {"Hello"}}, ["🌎"]),  # Emoji as key
        ({"en": {"Hello"}, "en-US": {"Hello"}}, ["en", "en-US"]),  # Locale-specific codes
    ],
)
def test_get_langs_default_behavior(input_dict: dict, expected_result: list[str]) -> None:
    """Test the default behavior of get_langs without case folding.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and text sets.
    :param expected_result: Expected list of language codes returned by get_langs.
    """
    mls = MultiLangString(mls_dict=input_dict)
    assert mls.get_langs() == expected_result, "get_langs should return all language codes as is by default"


@pytest.mark.parametrize(
    "input_dict, expected_result",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, ["en", "fr"]),
        ({"EN": {"Hello"}, "FR": {"Bonjour"}}, ["en", "fr"]),
        ({"EN": {" Hello "}, "fr": {"Bonjour"}}, ["en", "fr"]),  # Mixed case with spaces
        ({"ру": {"Привет"}, "ελ": {"Γειά"}}, ["ру", "ελ"]),  # Cyrillic and Greek characters, no case folding applied
        ({"🌎": {"Hello"}}, ["🌎"]),  # Emoji as key, no case folding applied
    ],
)
def test_get_langs_with_case_folding(input_dict: dict, expected_result: list[str]) -> None:
    """Test get_langs with case folding enabled.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and text sets.
    :param expected_result: Expected list of language codes returned by get_langs with case folding enabled.
    """
    mls = MultiLangString(mls_dict=input_dict)
    assert (
        mls.get_langs(casefold=True) == expected_result
    ), "get_langs with casefold=True should return all language codes in lowercase"


def test_get_langs_edge_case_empty_string_key() -> None:
    """Test get_langs with an edge case of an empty string as a language key."""
    mls = MultiLangString(mls_dict={"": {"Hello"}})
    assert mls.get_langs() == [""], "get_langs should correctly handle an empty string as a key"


def test_get_langs_unusual_valid_usage() -> None:
    """Test get_langs with an unusual, but technically valid, usage."""
    mls = MultiLangString(mls_dict={"123": {"One"}, "True": {"Yes"}})
    assert mls.get_langs() == ["123", "True"], "get_langs should handle unusual but valid keys correctly"


def test_get_langs_lowercase_flag_effect() -> None:
    """Test the effect of the LOWERCASE_LANG flag on the get_langs method."""
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, True)
    mls = MultiLangString(mls_dict={"EN": {"Hello"}, "FR": {"Bonjour"}})
    assert mls.get_langs() == [
        "en",
        "fr",
    ], "get_langs should return lowercase language codes when LOWERCASE_LANG flag is set"
