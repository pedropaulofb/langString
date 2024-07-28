import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_GENERAL


@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("Hello", "en", {"en": {"Hello"}}),
        ("Bonjour", "fr", {"fr": {"Bonjour"}}),
        ("Hello", "en", {"en": {"Hello", "World"}}),  # Assuming "World" already exists for "en"
        ("Hola", "", {"": {"Hola"}}),  # Adding text with default (empty) language
    ],
)
def test_add_entry_valid_input(text: str, lang: str, expected_result: dict):
    """Tests adding a text entry under a specified language with valid inputs.

    :param text: The text to be added.
    :param lang: The language under which the text should be added.
    :param expected_result: Expected state of mls_dict after adding the entry.
    """
    mls = MultiLangString()
    if "World" in expected_result.get("en", {}):  # Setup for existing text
        mls.add_entry("World", "en")
    mls.add_entry(text, lang)
    assert mls.mls_dict == expected_result, "The text was not added correctly to the specified language."


@pytest.mark.parametrize(
    "text, lang, error_type",
    [
        (123, "en", TypeError),
        ("Hello", 123, TypeError),
        (["en"], "en", TypeError),
        ("Hello", ["en"], TypeError),
        ({"en"}, "en", TypeError),
        ("Hello", {"en"}, TypeError),
    ],
)
def test_add_entry_invalid_type(text, lang, error_type):
    """Tests adding entries with invalid types for text and language parameters, expecting TypeError.

    :param text: The text to be added, potentially invalid type.
    :param lang: The language under which the text should be added, potentially invalid type.
    :param error_type: The expected error type.
    """
    mls = MultiLangString()
    with pytest.raises(error_type, match=TYPEERROR_MSG_GENERAL):
        mls.add_entry(text, lang)


@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("", "en", {"en": {""}}),  # Adding an empty string as text
        ("    ", "en", {"en": {"    "}}),  # Adding a string with spaces
        ("Hello\nWorld", "en", {"en": {"Hello\nWorld"}}),  # Adding multiline text
        ("LongText" * 1000, "en", {"en": {"LongText" * 1000}}),  # Adding an extremely long string
    ],
)
def test_add_entry_special_cases(text: str, lang: str, expected_result: dict):
    """Tests adding entries with special cases to ensure method robustness.

    :param text: Text to be added, covering empty, whitespace, multiline, and extremely long strings.
    :param lang: Language code under which the text is added.
    :param expected_result: Expected dictionary state after addition.
    """
    mls = MultiLangString()
    mls.add_entry(text, lang)
    assert mls.mls_dict == expected_result, f"Special case text '{text}' was not handled as expected."


@pytest.mark.parametrize(
    "flag, flag_value, text, lang, expected_result",
    [
        (MultiLangStringFlag.LOWERCASE_LANG, True, "Hello", "EN", {"en": {"Hello"}}),  # LOWERCASE_LANG effect
        (MultiLangStringFlag.STRIP_TEXT, True, "  Hello  ", "en", {"en": {"Hello"}}),  # STRIP_TEXT effect
    ],
)
def test_add_entry_with_flag_effects(flag, flag_value, text, lang, expected_result):
    """Tests the add_entry method with various flag effects.

    :param flag: The MultiLangStringFlag to test.
    :param flag_value: The value to set for the flag (True or False).
    :param text: The text to add to the MultiLangString.
    :param lang: The language code under which to add the text.
    :param expected_result: The expected mls_dict after adding the text with the flag effect.
    """
    Controller.set_flag(flag, flag_value)  # Set the flag to the specified value
    mls = MultiLangString()
    mls.add_entry(text, lang)
    assert mls.mls_dict == expected_result, f"Flag {flag.name} did not produce the expected effect."


@pytest.mark.parametrize(
    "initial_lang, initial_text, new_lang, new_text, expected_result",
    [
        # Case 1: Initial lowercase, new entry uppercase
        ("en", "Hello", "EN", "World", {"en": {"Hello", "World"}}),
        # Case 2: Initial uppercase, new entry lowercase
        ("EN", "Hello", "en", "World", {"en": {"Hello", "World"}}),
        # Case 3: Same case
        ("EN", "Hello", "EN", "World", {"en": {"Hello", "World"}}),
        ("en", "Hello", "en", "World", {"en": {"Hello", "World"}}),
    ],
)
def test_add_entry_case_insensitivity_on(initial_lang, initial_text, new_lang, new_text, expected_result):
    """Tests adding entries with case insensitivity in language codes.

    Ensures that languages are treated without case consideration but stored as they are first added.

    :param initial_lang: The language code of the initial entry.
    :param initial_text: The text of the initial entry.
    :param new_lang: The language code of the new entry.
    :param new_text: The text of the new entry.
    :param expected_result: The expected mls_dict state after additions.
    """
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, True)
    mls = MultiLangString()
    mls.add_entry(initial_text, initial_lang)  # Add initial entry
    mls.add_entry(new_text, new_lang)  # Add new entry in potentially different case
    assert mls.mls_dict == expected_result, "Entries were not stored correctly considering case-insensitivity."


@pytest.mark.parametrize(
    "initial_lang, initial_text, new_lang, new_text, expected_result",
    [
        # Case 1: Initial lowercase, new entry uppercase
        ("en", "Hello", "EN", "World", {"en": {"Hello", "World"}}),
        # Case 2: Initial uppercase, new entry lowercase
        ("EN", "Hello", "en", "World", {"EN": {"Hello", "World"}}),
        # Case 3: Same case
        ("EN", "Hello", "EN", "World", {"EN": {"Hello", "World"}}),
        ("en", "Hello", "en", "World", {"en": {"Hello", "World"}}),
    ],
)
def test_add_entry_case_insensitivity_off(initial_lang, initial_text, new_lang, new_text, expected_result):
    """Tests adding entries with case insensitivity in language codes.

    Ensures that languages are treated without case consideration but stored as they are first added.

    :param initial_lang: The language code of the initial entry.
    :param initial_text: The text of the initial entry.
    :param new_lang: The language code of the new entry.
    :param new_text: The text of the new entry.
    :param expected_result: The expected mls_dict state after additions.
    """
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, False)
    mls = MultiLangString()
    mls.add_entry(initial_text, initial_lang)  # Add initial entry
    mls.add_entry(new_text, new_lang)  # Add new entry in potentially different case
    assert mls.mls_dict == expected_result, "Entries were not stored correctly considering case-insensitivity."
