import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang, expected",
    [
        ("en", True),  # Language present
        ("EN", True),  # Language present
        ("es", True),  # Another language present
        ("Es", True),  # Another language present
        ("de", False),  # Language not present
        ("dE", False),  # Language not present
        ("", False),  # Empty string as language code
    ],
)
def test_contains_lang_valid_input(lang: str, expected: bool):
    """
    Test `contains_lang` method with valid language codes.

    :param lang: The language code to check for its presence.
    :param expected: The expected boolean outcome.
    :return: Asserts if `contains_lang` correctly identifies the presence or absence of a language code.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "es": {"Hola"}})
    assert mls.contains_lang(lang) == expected, f"contains_lang('{lang}') should return {expected}"
    mls = MultiLangString(mls_dict={"eN": {"Hello"}, "eS": {"Hola"}})
    assert mls.contains_lang(lang) == expected, f"contains_lang('{lang}') should return {expected}"


@pytest.mark.parametrize(
    "lang",
    [
        123,  # Integer as language code
        None,  # None as language code
        [],  # List as language code
        {},  # Dictionary as language code
    ],
)
def test_contains_lang_invalid_type(lang):
    """
    Test `contains_lang` method with invalid types for language code.

    :param lang: The invalid language code to test.
    :raises TypeError: If `lang` is not a string.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.contains_lang(lang)


@pytest.mark.parametrize(
    "flag, lang, setup_lang, expected",
    [
        (MultiLangStringFlag.LOWERCASE_LANG, "EN", "en", True),  # LOWERCASE_LANG flag effect
        (MultiLangStringFlag.LOWERCASE_LANG, "en", "EN", True),  # Ensuring LOWERCASE_LANG applies both ways
    ],
)
def test_contains_lang_with_flag_effect(flag: MultiLangStringFlag, lang: str, setup_lang: str, expected: bool):
    """
    Test `contains_lang` method considering the effect of MultiLangString flags.

    :param flag: The flag to test the effect of.
    :param lang: The language code to check.
    :param setup_lang: The language code used in the setup MultiLangString.
    :param expected: The expected outcome of the contains_lang call.
    """
    Controller.set_flag(flag, True)
    mls = MultiLangString(mls_dict={setup_lang: {"Hello"}})
    assert mls.contains_lang(lang) == expected, f"With '{flag}' flag, contains_lang('{lang}') should return {expected}"
