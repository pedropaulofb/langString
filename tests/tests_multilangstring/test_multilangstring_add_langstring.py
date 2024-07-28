import pytest
from langstring import Controller
from langstring import LangString
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_dict, langstring, expected_dict",
    [
        # Adding a new LangString to an empty MultiLangString
        ({}, LangString(text="Hello", lang="en"), {"en": {"Hello"}}),
        # Adding a LangString to an existing language
        ({"en": {"Hello"}}, LangString(text="World", lang="en"), {"en": {"Hello", "World"}}),
        # Adding a LangString in a new language
        ({"en": {"Hello"}}, LangString(text="Bonjour", lang="fr"), {"en": {"Hello"}, "fr": {"Bonjour"}}),
        # Adding multiple LangStrings in the same language
        (
            {"en": {"Hello"}},
            [LangString(text="World", lang="en"), LangString(text="Greetings", lang="en")],
            {"en": {"Hello", "World", "Greetings"}},
        ),
    ],
)
def test_add_langstring(initial_dict: dict, langstring, expected_dict: dict):
    """Tests adding a LangString object to the MultiLangString.

    :param initial_dict: Initial state of mls_dict in MultiLangString.
    :param langstring: The LangString object(s) to be added.
    :param expected_dict: Expected state of mls_dict after adding the LangString(s).
    """
    mls = MultiLangString(mls_dict=initial_dict)
    if isinstance(langstring, list):
        for ls in langstring:
            mls.add_langstring(ls)
    else:
        mls.add_langstring(langstring)
    assert mls.mls_dict == expected_dict, "The LangString was not added correctly to the MultiLangString."


@pytest.mark.parametrize("invalid_langstring", [123, "not a LangString"])
def test_add_langstring_invalid_type(invalid_langstring):
    """Tests adding an invalid type as LangString to the MultiLangString, expecting a TypeError.

    :param invalid_langstring: Invalid LangString object to be added.
    :param match_message: Expected error message or pattern.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.add_langstring(invalid_langstring)


# Test for handling None as input
def test_add_langstring_with_none():
    """Tests adding None as a LangString, expecting TypeError."""
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.add_langstring(None)


# Test for edge cases: adding extremely long string and unusual but valid language codes
@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("a" * 10000, "en", {"en": {"a" * 10000}}),  # Extremely long text
        ("Hello", "xx", {"xx": {"Hello"}}),  # Unusual but valid language code
        # Adding a LangString with special characters
        ("Special@#&*Chars", "en", {"en": {"Special@#&*Chars"}}),
        # Adding a LangString with numeric content
        ("123456", "en", {"en": {"123456"}}),
    ],
)
def test_add_langstring_edge_cases(text, lang, expected_result):
    """Tests adding LangString with edge case scenarios."""
    ls = LangString(text=text, lang=lang)
    mls = MultiLangString()
    mls.add_langstring(ls)
    assert mls.mls_dict == expected_result, "LangString with edge cases not handled correctly."


# Test for flags' effects: Assuming LOWERCASE_LANG flag affects the language code processing
def test_add_langstring_with_lowercase_flag():
    """Tests LOWERCASE_LANG flag effect on adding LangString."""
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, True)
    ls = LangString(text="Hello", lang="EN")
    mls = MultiLangString()
    mls.add_langstring(ls)
    assert "en" in mls.mls_dict and "Hello" in mls.mls_dict["en"], "LOWERCASE_LANG flag effect not applied."


# Test for unusual but valid usage: adding empty strings or whitespace
@pytest.mark.parametrize(
    "text",
    [
        "",  # Empty string
        "  ",  # Whitespace string
        "@#&*",  # special characters
        "123",  # numeric string
    ],
)
def test_add_langstring_unusual_valid_usage(text):
    """Tests adding LangString with unusual but valid text values."""
    ls = LangString(text=text, lang="en")
    mls = MultiLangString()
    mls.add_langstring(ls)
    assert text in mls.mls_dict["en"], "Unusual but valid text not handled correctly."
