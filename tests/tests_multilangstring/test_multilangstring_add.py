import pytest
from langstring import Controller
from langstring import LangString
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from langstring import SetLangString


# Testing addition of simple text in the preferred language
@pytest.mark.parametrize(
    "text, expected_dict",
    [
        ("Hello", {"en": {"Hello"}}),
    ],
)
def test_add_simple_text(text: str, expected_dict: dict):
    mls = MultiLangString()
    with pytest.raises(TypeError, match="Argument .+ must be of type"):
        mls.add(text)


# Testing addition of LangString object
@pytest.mark.parametrize(
    "langstring, expected_dict",
    [
        (LangString(text="Hello", lang="en"), {"en": {"Hello"}}),
    ],
)
def test_add_langstring(langstring: LangString, expected_dict: dict):
    mls = MultiLangString()
    mls.add(langstring)
    assert mls.mls_dict == expected_dict, "Failed to add LangString object correctly."


# Testing addition of SetLangString object
@pytest.mark.parametrize(
    "setlangstring, expected_dict",
    [
        (SetLangString(texts={"Hello", "World"}, lang="en"), {"en": {"Hello", "World"}}),
    ],
)
def test_add_setlangstring(setlangstring: SetLangString, expected_dict: dict):
    mls = MultiLangString()
    mls.add(setlangstring)
    assert mls.mls_dict == expected_dict, "Failed to add SetLangString object correctly."


# Testing addition of tuple (text, lang)
@pytest.mark.parametrize(
    "text_lang_tuple, expected_dict",
    [
        (("Hello", "en"), {"en": {"Hello"}}),
    ],
)
def test_add_text_lang_tuple(text_lang_tuple: tuple[str, str], expected_dict: dict):
    mls = MultiLangString()
    mls.add(text_lang_tuple)
    assert mls.mls_dict == expected_dict, "Failed to add tuple (text, lang) correctly."


# Testing invalid argument type
@pytest.mark.parametrize(
    "invalid_arg",
    [
        123,
        3.14,
        ["not", "valid"],
    ],
)
def test_add_invalid_type(invalid_arg):
    mls = MultiLangString()
    with pytest.raises(
        TypeError,
        match="Argument .+ must be of type .+, but got",
    ):
        mls.add(invalid_arg)


# Testing addition of an empty string
@pytest.mark.parametrize(
    "text, expected_dict",
    [
        ("", {"en": {""}}),  # Assuming 'en' is the preferred language
    ],
)
def test_add_empty_string(text: str, expected_dict: dict):
    mls = MultiLangString()
    with pytest.raises(TypeError, match="Argument .+ must be of type"):
        mls.add(text)


# Testing addition of a very long string
@pytest.mark.parametrize(
    "text, expected_dict",
    [
        ("a" * 10000, {"en": {"a" * 10000}}),
    ],
)
def test_add_very_long_string(text: str, expected_dict: dict):
    mls = MultiLangString()
    with pytest.raises(TypeError, match="Argument .+ must be of type"):
        mls.add(text)


# Testing addition with unusual language codes
@pytest.mark.parametrize(
    "arg, expected_dict",
    [
        (("Hello", "xx"), {"xx": {"Hello"}}),  # Adding text with an unusual but valid language code
        (LangString(text="Bonjour", lang="xx"), {"xx": {"Bonjour"}}),  # LangString with an unusual language code
    ],
)
def test_add_unusual_language_codes(arg, expected_dict):
    mls = MultiLangString()
    mls.add(arg)
    assert mls.mls_dict == expected_dict, "Failed to handle unusual language codes correctly."


# Test for flags' effects: Assuming LOWERCASE_LANG flag affects the language code processing
@pytest.mark.parametrize(
    "text, lang, flag, expected_dict",
    [
        ("Hello", "EN", MultiLangStringFlag.LOWERCASE_LANG, {"en": {"Hello"}}),  # Testing LOWERCASE_LANG effect
    ],
)
def test_add_with_flag_effect(text: str, lang: str, flag, expected_dict: dict):
    Controller.set_flag(flag, True)
    mls = MultiLangString()
    mls.add((text, lang))  # Assuming the tuple (text, lang) is an acceptable input format
    assert mls.mls_dict == expected_dict, f"Flag {flag.name} effect not applied correctly."
    Controller.reset_flag(flag)  # Reset flag after test


# Expanding test cases for testing flag effects
@pytest.mark.parametrize(
    "text, expected_dict, flag",
    [
        ("  Hello  ", {"en": {"Hello"}}, MultiLangStringFlag.STRIP_TEXT),  # STRIP_TEXT effect
    ],
)
def test_add_with_strip_text_flag_effect(text: str, expected_dict: dict, flag):
    Controller.set_flag(flag, True)
    mls = MultiLangString()
    with pytest.raises(TypeError, match="Argument .+ must be of type"):
        mls.add(text)


# Expanding test cases for invalid argument types
@pytest.mark.parametrize(
    "invalid_arg",
    [
        {},  # Testing with a dictionary
        {1, 2, 3},  # Testing with a set
        # Other data structures as needed
    ],
)
def test_add_invalid_data_structure(invalid_arg):
    mls = MultiLangString()
    with pytest.raises(TypeError):
        mls.add(invalid_arg)


# Testing addition of MultiLangString object
@pytest.mark.parametrize(
    "initial_contents, adding_mls_contents, expected_dict",
    [
        # Test adding MultiLangString with the same language
        ({"en": {"Hello"}}, {"en": {"World"}}, {"en": {"Hello", "World"}}),
        # Test adding MultiLangString with different languages
        ({"en": {"Hello"}}, {"fr": {"Bonjour"}}, {"en": {"Hello"}, "fr": {"Bonjour"}}),
        # Test adding MultiLangString with overlapping contents
        ({"en": {"Hello", "World"}}, {"en": {"World", "Everyone"}}, {"en": {"Hello", "World", "Everyone"}}),
    ],
)
def test_add_multilangstring(initial_contents, adding_mls_contents, expected_dict):
    mls_initial = MultiLangString(initial_contents)
    mls_adding = MultiLangString(adding_mls_contents)
    mls_initial.add(mls_adding)
    assert mls_initial.mls_dict == expected_dict, "Failed to add MultiLangString object correctly."
