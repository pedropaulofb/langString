import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


# Test cases for mls_dict getter and setter
@pytest.mark.parametrize(
    "input_dict, expected_output",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, {"en": {"Hello"}, "fr": {"Bonjour"}}),
        ({}, {}),
        (None, {}),
        ({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}),
        ({"en": set()}, {"en": set()}),  # Testing with an empty set for a language
    ],
)
def test_mls_dict_getter_setter(input_dict: dict, expected_output: dict):
    """Tests the getter and setter for mls_dict.

    :param input_dict: The input dictionary to set for mls_dict.
    :param expected_output: The expected dictionary to be retrieved from mls_dict.
    """
    mls = MultiLangString()
    mls.mls_dict = input_dict
    assert mls.mls_dict == expected_output, "mls_dict getter or setter does not work as expected"


# Test cases for pref_lang getter and setter
@pytest.mark.parametrize(
    "input_lang, expected_output",
    [
        ("en", "en"),
        ("fr", "fr"),
        (None, "en"),
        ("", ""),
        ("es", "es"),
    ],
)
def test_pref_lang_getter_setter(input_lang: str, expected_output):
    """Tests the getter and setter for pref_lang.

    :param input_lang: The input language code to set for pref_lang.
    :param expected_output: The expected language code to be retrieved from pref_lang or the expected error.
    """
    mls = MultiLangString()
    if expected_output is TypeError:
        with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
            mls.pref_lang = input_lang
    else:
        mls.pref_lang = input_lang
        assert mls.pref_lang == expected_output, "pref_lang getter or setter does not work as expected"


# Testing invalid types within mls_dict values
@pytest.mark.parametrize(
    "input_dict, expected_error",
    [
        ({"en": [123]}, TypeError),  # List instead of set
        ({"en": "Hello"}, TypeError),  # String instead of set
    ],
)
def test_mls_dict_setter_invalid_value_types(input_dict: dict, expected_error):
    """Tests setting mls_dict with invalid value types."""
    mls = MultiLangString()
    with pytest.raises(expected_error, match=TYPEERROR_MSG_SINGULAR):
        mls.mls_dict = input_dict


@pytest.mark.parametrize(
    "flags, input_dict, input_pref_lang, expected_dict, expected_pref_lang",
    [
        # Test LOWERCASE_LANG impact
        ({MultiLangStringFlag.LOWERCASE_LANG: True}, {"EN": {"Hello"}}, "EN", {"en": {"Hello"}}, "en"),
        # Test STRIP_TEXT impact on pref_lang (assuming implementation allows)
        ({MultiLangStringFlag.STRIP_TEXT: True}, {"en": {"  Hello  "}}, "en", {"en": {"Hello"}}, "en"),
        # Combination of flags, assuming possible cumulative effects
        (
            {MultiLangStringFlag.LOWERCASE_LANG: True, MultiLangStringFlag.STRIP_TEXT: True},
            {"EN": {"  Hello  "}},
            "EN",
            {"en": {"Hello"}},
            "en",
        ),
    ],
)
def test_flags_impact_on_getter_setter(flags, input_dict, input_pref_lang, expected_dict, expected_pref_lang):
    """Tests the impact of flags on mls_dict and pref_lang getters and setters.

    :param flags: Dictionary of flags to set.
    :param input_dict: The input dictionary for mls_dict.
    :param input_pref_lang: The input preferred language.
    :param expected_dict: The expected mls_dict state considering the flag effects.
    :param expected_pref_lang: The expected pref_lang considering the flag effects.
    """
    for flag, value in flags.items():
        Controller.set_flag(flag, value)
    mls = MultiLangString()
    mls.mls_dict = input_dict
    mls.pref_lang = input_pref_lang
    assert mls.mls_dict == expected_dict, "mls_dict not affected as expected by the flags."
    assert mls.pref_lang == expected_pref_lang, "pref_lang not affected as expected by the flags."
