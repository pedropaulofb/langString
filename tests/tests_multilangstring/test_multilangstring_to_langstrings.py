import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_langs, expected_length, specific_lang_check",
    [
        (["en", "fr"], 4, None),  # Basic case with multiple languages
        (["en"], 2, "en"),  # Single language filter, expecting two LangStrings for 'en'
        (None, 6, None),  # None as input to get all LangStrings
        ([], 0, None),  # Empty list as input, expecting no LangStrings
        (["xx"], 0, None),  # Empty list as input, expecting no LangStrings
        (["en", "fr", "el"], 4, None),  # Including a Greek language code
        (["ru"], 2, "ru"),  # Including a Cyrillic language code
        (["EN"], 2, "EN"),  # Upper case language code
        (["En"], 2, "En"),  # Mixed case language code
        (["🙂"], 0, None),  # Emoji as a language code, expecting no LangStrings
        ([""], 0, None),  # Empty string as a language code, expecting no LangStrings
        ([""], 0, []),
        (["en", "xx", ""], 2, "en"),
    ],
)
def test_to_langstrings_valid_cases(input_langs, expected_length, specific_lang_check):
    """
    Test the to_langstrings method with various valid inputs to ensure it returns the correct LangString instances.

    :param input_langs: The input 'langs' parameter to the method.
    :param expected_length: The expected number of LangString instances in the output list.
    :param specific_lang_check: A specific language to check in the output, if applicable.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}, "RU": {"Привет", "Мир"}})
    output = mls.to_langstrings(langs=input_langs)
    assert isinstance(output, list), "Output is not a list for valid input cases."
    assert len(output) == expected_length, f"Expected {expected_length} LangStrings, got {len(output)}."
    if specific_lang_check:
        assert all(
            lang.lang.casefold() == specific_lang_check.casefold() for lang in output
        ), f"Expected all LangStrings to be in {specific_lang_check}, found other languages."


@pytest.mark.parametrize(
    "input_langs, expected_exception",
    [
        ("en", TypeError),  # Non-list, non-None input
        ([123, "en"], TypeError),  # List with non-string element
        ({"en", "fr"}, TypeError),  # Set input, expecting list
        ([123, "fr"], TypeError),  # Numeric element in langs
        (["en", None], TypeError),  # None in langs
        (["en", 5.5], TypeError),  # Float in langs
        (["en", []], TypeError),  # Empty list in langs
        (["en", {}], TypeError),  # Empty dict in langs
    ],
)
def test_to_langstrings_invalid_cases(input_langs, expected_exception):
    """
    Test the to_langstrings method with invalid inputs to ensure it raises the correct exceptions.

    :param input_langs: The input 'langs' parameter to the method that is expected to trigger an exception.
    :param expected_exception: The exception type that is expected to be raised.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}})
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.to_langstrings(langs=input_langs)


@pytest.mark.parametrize(
    "input_langs, expected_length, expected_languages",
    [
        # Filtering with a single language, expecting 2 LangStrings for 'en'
        (["en"], 2, ["en", "en"]),
        # Including a test case for an empty list, which should yield no LangStrings
        ([], 0, []),
        # Including a language not in mls_dict to test filtering with no matches
        (["es"], 0, []),
        # Mixed case with one valid and one invalid language code, expecting LangStrings for valid language only
        (["en", "xx"], 2, ["en", "en"]),
        (["en ", "fr"], 2, ["fr", "fr"]),
        ([" en", "fr"], 2, ["fr", "fr"]),
    ],
)
def test_to_langstrings_valid_edge_cases(input_langs, expected_length, expected_languages):
    """
    Test the to_langstrings method for valid edge cases to ensure it returns the correct LangString instances
    and handles various input scenarios correctly.

    :param input_langs: The input 'langs' parameter to the method.
    :param expected_length: The expected number of LangString instances in the output list.
    :param expected_languages: The list of expected languages for each LangString in the output.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}})
    output = mls.to_langstrings(langs=input_langs)

    assert len(output) == expected_length, f"Expected {expected_length} LangStrings, got {len(output)}."
    if expected_length > 0:
        output_languages = [lang.lang for lang in output]
        assert (
            output_languages == expected_languages
        ), f"Expected languages {expected_languages}, got {output_languages}."
    else:
        assert output == [], "Expected an empty list for no matching languages."


import pytest


# Tests for valid cases including handling of non-existing languages
@pytest.mark.parametrize(
    "input_langs, expected_length, expected_languages",
    [
        # Basic case with multiple languages
        (["en", "fr"], 4, ["en", "en", "fr", "fr"]),
        # Single language filter, expecting two LangStrings for 'en'
        (["en"], 2, ["en", "en"]),
        # None as input to get all LangStrings
        (None, 4, ["en", "en", "fr", "fr"]),
        # Empty list as input, expecting no LangStrings
        ([], 0, []),
        # Space in language code treated as invalid, expecting no output for that language
        (["en ", "fr"], 2, ["fr", "fr"]),
        ([" en", "fr"], 2, ["fr", "fr"]),
        (["en", "fr "], 2, ["en", "en"]),
        (["en", " fr"], 2, ["en", "en"]),
        # Non-existent language codes, expecting no output for those languages
        (["xx", "yy"], 0, []),
        # Mixed valid and invalid language codes
        (["en", "xx"], 2, ["en", "en"]),
    ],
)
def test_to_langstrings_valid_cases2(input_langs, expected_length, expected_languages):
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}})
    output = mls.to_langstrings(langs=input_langs)
    assert len(output) == expected_length, "Incorrect number of LangStrings returned."
    if expected_length > 0:
        output_languages = [ls.lang for ls in output]
        assert output_languages == expected_languages, "Incorrect languages returned."


# Tests for invalid types
@pytest.mark.parametrize(
    "input_langs, expected_exception",
    [
        ("en", TypeError),  # String instead of list
        (123, TypeError),  # Integer instead of list
        ({"en", "fr"}, TypeError),  # Set instead of list
        (["en", "fr", 123], TypeError),
        ([123], TypeError),
        ([None], TypeError),
    ],
)
def test_to_langstrings_invalid_types(input_langs, expected_exception):
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}})
    with pytest.raises(expected_exception):
        mls.to_langstrings(langs=input_langs)


@pytest.mark.parametrize(
    "input_langs, expected_length, expected_languages",
    [
        # New test case: Case with an empty string language code existing in the mls_dict
        ([""], 2, ["", ""]),  # Expecting LangStrings with empty lang
        # New test case: Mixed case with valid, invalid, and empty string language codes
        (["en", "xx", ""], 4, ["en", "en", "", ""]),  # Including empty string lang code
    ],
)
def test_to_langstrings_valid_cases_with_empty_lang(input_langs, expected_length, expected_languages):
    # Enhanced MultiLangString dictionary to include empty string language code
    mls = MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}, "": {"Empty1", "Empty2"}})
    output = mls.to_langstrings(langs=input_langs)
    assert (
        len(output) == expected_length
    ), f"Incorrect number of LangStrings returned. Expected {expected_length}, got {len(output)}."
    if expected_length > 0:
        output_languages = [ls.lang for ls in output]
        assert (
            output_languages == expected_languages
        ), f"Incorrect languages returned. Expected {expected_languages}, got {output_languages}."
