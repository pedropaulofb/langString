import pytest
from langstring import Controller
from langstring import Converter
from langstring import LangString
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        # Single MultiLangString with one language
        ([MultiLangString(mls_dict={"en": {"Hello"}})], [LangString("Hello", "en")]),
        # Multiple MultiLangStrings with different languages
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})],
            [LangString("Hello", "en"), LangString("Bonjour", "fr")],
        ),
        # Multiple MultiLangStrings with overlapping languages
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"en": {"World"}})],
            [LangString("Hello", "en"), LangString("World", "en")],
        ),
        # Multiple MultiLangStrings with empty dictionary
        ([MultiLangString(), MultiLangString()], []),
    ],
)
def test_from_multilangstrings_to_langstrings(input_list, expected_output):
    """Test conversion from list of MultiLangString to list of LangString objects."""
    result = Converter.from_multilangstrings_to_langstrings(input_list)
    assert len(result) == len(expected_output), "Number of LangStrings does not match expected"
    for langstring in expected_output:
        assert langstring in result, f"LangString {langstring} not found in result"


@pytest.mark.parametrize(
    "input_list, filter_langs, expected_output",
    [
        # Filtering with a single language
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})],
            ["en"],
            [LangString("Hello", "en")],
        ),
        # Filtering with multiple languages
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})],
            ["en", "fr"],
            [LangString("Hello", "en"), LangString("Bonjour", "fr")],
        ),
        # Filtering with no matching languages
        ([MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})], ["es"], []),
        # Filtering with overlapping languages
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"en": {"World"}})],
            ["en"],
            [LangString("Hello", "en"), LangString("World", "en")],
        ),
    ],
)
def test_from_multilangstrings_to_langstrings_with_language_filter(input_list, filter_langs, expected_output):
    """Test conversion from list of MultiLangString to list of LangString objects with language filtering."""
    result = Converter.from_multilangstrings_to_langstrings(input_list, languages=filter_langs)
    assert len(result) == len(expected_output), "Number of LangStrings after filtering does not match expected"
    for langstring in expected_output:
        assert langstring in result, f"Filtered LangString {langstring} not found in result"


def test_from_multilangstrings_to_langstrings_empty():
    """Test conversion from an empty list of MultiLangString."""
    result = Converter.from_multilangstrings_to_langstrings([])
    assert result == [], "Result is not an empty list for an empty input list"


@pytest.mark.parametrize(
    "invalid_input",
    [
        (123),
        ("not a MultiLangString list"),
        ([LangString("Hello", "en")]),
        (None),  # None as input
        ([{"en": "Hello"}]),  # Incorrectly formed dict inside list
        ([LangString("Hello", "en")]),  # LangString instance inside list
    ],
)
def test_from_multilangstrings_to_langstrings_invalid_input_type(invalid_input):
    """Test conversion with invalid input types."""
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstrings_to_langstrings(invalid_input)


@pytest.mark.parametrize(
    "invalid_language_filter",
    [
        123,
        "not a list",
        {"lang": "en"},
        True,
        5.5,
        [123],
        [None],
    ],
)
def test_from_multilangstrings_to_langstrings_invalid_language_filter(invalid_language_filter):
    """Test conversion with various invalid language filter types."""
    mls = MultiLangString(mls_dict={"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstrings_to_langstrings([mls], languages=invalid_language_filter)


def test_from_multilangstrings_to_langstrings_default_behavior():
    """Test default behavior without language filter."""
    mls_list = [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})]
    result = Converter.from_multilangstrings_to_langstrings(mls_list)
    assert len(result) == 2, "Expected default behavior to include all languages"


@pytest.mark.parametrize("languages", [None, []])
def test_from_multilangstrings_to_langstrings_null_languages(languages):
    """Test behavior with null and empty language filters."""
    mls_list = [MultiLangString(mls_dict={"en": {"Hello"}})]
    result = Converter.from_multilangstrings_to_langstrings(mls_list, languages=languages)
    if languages is None:
        assert len(result) == 1, "Passing None as languages should include all languages"
    else:
        assert len(result) == 0, "Passing empty list as languages should not include any languages"


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([MultiLangString(mls_dict={"": {""}})], [LangString("", "")]),  # Edge case: empty text and language
        (
            [MultiLangString(mls_dict={"en-GB": {"Colour"}}), MultiLangString(mls_dict={"en-US": {"Color"}})],
            [LangString("Colour", "en-GB"), LangString("Color", "en-US")],
        ),
    ],
)
def test_from_multilangstrings_to_langstrings_edge_cases(input_list, expected_output):
    """Test edge cases."""
    result = Converter.from_multilangstrings_to_langstrings(input_list)
    assert len(result) == len(expected_output), "Edge cases not handled correctly"
    for langstring in expected_output:
        assert langstring in result, f"LangString {langstring} not found in result"


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([MultiLangString(mls_dict={"": {""}})], [LangString("", "")]),
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"fr": {"Bonjour"}})],
            [LangString("Hello", "en"), LangString("Bonjour", "fr")],
        ),
        (
            [
                MultiLangString(mls_dict={"en": {"Hello"}}, pref_lang="en"),
                MultiLangString(mls_dict={"fr": {"Bonjour"}}),
            ],
            [LangString("Hello", "en"), LangString("Bonjour", "fr")],
        ),
        (
            [MultiLangString(mls_dict={"en": {"Hello"}}), MultiLangString(mls_dict={"en": {"World"}})],
            [LangString("Hello", "en"), LangString("World", "en")],
        ),
    ],
)
def test_from_multilangstrings_to_langstrings_unusual_usage(input_list, expected_output):
    """Test conversion from list of MultiLangString to list of LangString objects with unusual but valid usage."""
    result = Converter.from_multilangstrings_to_langstrings(input_list)
    assert len(result) == len(expected_output), "Number of LangStrings does not match expected"
    for langstring in expected_output:
        assert langstring in result, f"LangString {langstring} not found in result"


def test_from_multilangstrings_to_langstrings_operation_on_itself():
    """Test operation on itself."""
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "fr": {"Bonjour"}})
    input_list = [mls, mls]
    result = Converter.from_multilangstrings_to_langstrings(input_list)
    assert len(result) == 2, "Number of LangStrings should match the unique entries in the MultiLangString"
    assert LangString("Hello", "en") in result
    assert LangString("Bonjour", "fr") in result


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([MultiLangString(mls_dict={"en": {"Hello"}})], [LangString("Hello", "en")]),
        ([MultiLangString(mls_dict={"en": {"Hello"}}, pref_lang="fr")], [LangString("Hello", "en")]),
        (
            [
                MultiLangString(mls_dict={"en": {"Hello"}}, pref_lang="fr"),
                MultiLangString(mls_dict={"fr": {"Bonjour"}}),
            ],
            [LangString("Hello", "en"), LangString("Bonjour", "fr")],
        ),
    ],
)
def test_from_multilangstrings_to_langstrings_with_flags(input_list, expected_output):
    """Test conversion from list of MultiLangString to list of LangString objects with control flags."""
    # Set the flag to control the output
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, True)
    result = Converter.from_multilangstrings_to_langstrings(input_list)
    assert len(result) == len(expected_output), "Number of LangStrings does not match expected"
    for langstring in expected_output:
        assert langstring in result, f"LangString {langstring} not found in result"
    # Reset the flag to its default state
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
