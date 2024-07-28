import pytest
from langstring import Converter
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.fixture
def multilangstrings_with_varied_contents() -> list[MultiLangString]:
    """Fixture to provide MultiLangString instances with varied contents for testing."""
    return [
        MultiLangString(mls_dict={"en": {"Hello"}, "fr": {"Bonjour"}}),
        MultiLangString(mls_dict={"es": {"Hola", "¿Qué tal?"}, "de": {"Guten Tag", "Hallo"}}),
        MultiLangString(mls_dict={"ru": {"Привет"}}),
        MultiLangString(mls_dict={"whitespace": {"   "}, "emoji-lang": {"😀"}}),
    ]


@pytest.mark.parametrize(
    "input_mls, expected_number_of_setlangstrings, expected_languages",
    [
        ([], 0, []),
        (
            [
                MultiLangString(mls_dict={"en": {"Hello", "World"}}),
                MultiLangString(mls_dict={"en": {"Goodbye"}, "fr": {"Au revoir"}}),
            ],
            2,
            ["en", "fr"],
        ),
        (
            [
                MultiLangString(mls_dict={"en": {"One", "Two"}}),
                MultiLangString(mls_dict={"en": {"Three"}, "es": {"Tres"}}),
                MultiLangString(mls_dict={"de": {"Eins", "Zwei", "Drei"}}),
            ],
            3,
            ["en", "es", "de"],
        ),
        (
            [
                MultiLangString(mls_dict={"EN ": {"Space after"}}),
                MultiLangString(mls_dict={" en": {"Space before"}, "EN": {"UpperCase"}}),
            ],
            3,
            ["EN ", " en", "EN"],
        ),
        (
            [
                MultiLangString(mls_dict={"en": set()}),  # Empty set of texts for a language
            ],
            1,
            ["en"],
        ),
    ],
)
def test_from_multilangstrings_to_setlangstrings_basic_behavior(
    input_mls, expected_number_of_setlangstrings, expected_languages
):
    """
    Test that from_multilangstrings_to_setlangstrings combines MultiLangString instances into the correct number of SetLangString instances.

    :param input_mls: List of MultiLangString instances to be combined.
    :param expected_number_of_setlangstrings: Expected number of unique SetLangString instances created.
    :param expected_languages: Expected languages represented in the output SetLangString instances.
    """
    result = Converter.from_multilangstrings_to_setlangstrings(input_mls)
    assert len(result) == expected_number_of_setlangstrings, "Incorrect number of SetLangString instances created."
    for sls in result:
        assert isinstance(sls, SetLangString), "Each item in the result should be an instance of SetLangString."
        assert sls.lang in expected_languages, f"Unexpected language {sls.lang} found in the result."


@pytest.mark.parametrize(
    "input_mls",
    [
        [123],
        ["string"],
        [None],
        (
            [MultiLangString(mls_dict={"en": {"Valid"}}), "invalid"],
            "Expected all elements to be MultiLangString instances.",
        ),
    ],
)
def test_from_multilangstrings_to_setlangstrings_invalid_types(input_mls):
    """
    Test that from_multilangstrings_to_setlangstrings raises TypeError for invalid input types,
    ensuring all elements of the input list must be instances of MultiLangString.

    :param input_mls: Invalid input to test the method's type validation.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstrings_to_setlangstrings(input_mls)


def test_from_multilangstrings_to_setlangstrings_empty_strings_and_special_chars(multilangstrings_with_varied_contents):
    """
    Test handling of empty strings and special characters within MultiLangString instances.

    This test ensures that empty strings and texts with special characters are correctly handled and transferred to SetLangString instances.
    """
    # Adding a MultiLangString with empty strings and special characters
    multilangstrings_with_varied_contents.append(MultiLangString(mls_dict={"empty": {""}, "special": {"@#&*()"}}))
    result = Converter.from_multilangstrings_to_setlangstrings(multilangstrings_with_varied_contents)
    empty_sls = next((sls for sls in result if sls.lang == "empty"), None)
    special_sls = next((sls for sls in result if sls.lang == "special"), None)
    assert empty_sls is not None and "" in empty_sls.texts, "Empty strings should be correctly handled."
    assert special_sls is not None and "@#&*()" in special_sls.texts, "Special characters should be correctly handled."


@pytest.mark.parametrize(
    "input_mls, expected_lang_tag",
    [
        ([MultiLangString(mls_dict={"xx-long-lang-code": {"Unique"}})], "xx-long-lang-code"),
        ([MultiLangString(mls_dict={"MixedCASE": {"Text"}})], "MixedCASE"),
        ([MultiLangString(mls_dict={" spacedLang ": {"Text with spaces"}})], " spacedLang "),
        ([MultiLangString(mls_dict={"ru": {"Привет, как дела?"}})], "ru"),
        ([MultiLangString(mls_dict={"emoji-text": {"😀😃😄"}})], "emoji-text"),
    ],
)
def test_from_multilangstrings_to_setlangstrings_unusual_valid_usage(input_mls, expected_lang_tag):
    """Test handling of unusual but valid language codes."""
    result = Converter.from_multilangstrings_to_setlangstrings(input_mls)
    assert len(result) == 1, "Should handle unusual but valid language codes correctly."
    assert result[0].lang == expected_lang_tag, f"Expected language tag '{expected_lang_tag}' was not preserved."


@pytest.mark.parametrize(
    "input_mls, expected_texts",
    [
        (
            [MultiLangString(mls_dict={"en": {"A very long text string that goes on and on"}})],
            {"A very long text string that goes on and on"},
        ),
        # Duplicate MultiLangString instances
        ([MultiLangString(mls_dict={"en": {"Repeat"}}), MultiLangString(mls_dict={"en": {"Repeat"}})], {"Repeat"}),
    ],
)
def test_from_multilangstrings_to_setlangstrings_edge_cases_and_duplicates(input_mls, expected_texts):
    """Test edge cases including long texts and handling of duplicate MultiLangString instances."""
    result = Converter.from_multilangstrings_to_setlangstrings(input_mls)
    assert len(result) == 1, "Duplicate or long text cases should still result in one SetLangString per language."
    assert expected_texts.issubset(result[0].texts), "All expected texts should be present in the result."
