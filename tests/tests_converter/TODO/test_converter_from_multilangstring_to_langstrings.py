import pytest

from langstring import Converter
from langstring import LangString
from langstring import MultiLangString


@pytest.mark.parametrize(
    "input_data, expected_output, langs",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, [LangString("Hello", "en"), LangString("Bonjour", "fr")], None),
        ({}, [], None),
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, [LangString("Bonjour", "fr")], ["fr"]),
        ({"en": {"Hello"}}, [], ["fr"]),
        ({"en": {" "}, "fr": {" Bonjour"}}, [LangString(" ", "en"), LangString(" Bonjour", "fr")], None),
        ({"en": {"Hello"}, "el": {"Γειά σου"}}, [LangString("Hello", "en"), LangString("Γειά σου", "el")], None),
        ({"en": {"Hello 😊"}, "ru": {"Привет"}}, [LangString("Hello 😊", "en"), LangString("Привет", "ru")], None),
        ({"en": {"<script>alert('xss')</script>"}}, [LangString("<script>alert('xss')</script>", "en")], None),
        ({"": {"Empty key test"}}, [LangString("Empty key test", "")], None),
        ({"en": {""}}, [LangString("", "en")], None),
    ],
)
def test_from_multilangstring_to_langstrings(input_data, expected_output, langs):
    mls = MultiLangString(mls_dict=input_data)
    result = Converter.from_multilangstring_to_langstrings(mls, languages=langs)

    assert isinstance(result, list), "Result should be a list."
    assert len(result) == len(expected_output), "Expected number of LangStrings does not match the result."
    for langstring in result:
        assert isinstance(langstring, LangString), "Each item in the result should be a LangString instance."
        expected_texts = [(ls.text, ls.lang) for ls in expected_output]
        assert (langstring.text, langstring.lang) in expected_texts, "Unexpected LangString in result."


@pytest.mark.parametrize(
    "invalid_input",
    [
        (123),
        ("string"),
        (None),
    ],
)
def test_from_multilangstring_to_langstrings_type_error(invalid_input):
    """Test the from_multilangstring_to_langstrings method raises TypeError for invalid input types."""
    with pytest.raises(TypeError, match="Argument .+ must be of type 'MultiLangString', but got"):
        Converter.from_multilangstring_to_langstrings(invalid_input)


@pytest.mark.parametrize(
    "languages_input, expected_exception",
    [
        (123, TypeError),  # Invalid type for languages parameter
        ("en", TypeError),  # Invalid type, expecting list, got str
        ([], ValueError),  # Empty list for languages parameter
        (["en", 123], TypeError),  # List with invalid type
        ([""], ValueError),  # List with empty string as language
    ],
)
def test_from_multilangstring_to_langstrings_invalid_languages_type(languages_input, expected_exception):
    """Test the from_multilangstring_to_langstrings method raises exceptions for invalid 'languages' parameter types."""
    mls = MultiLangString(mls_dict={"en": {"Hello"}})
    with pytest.raises(expected_exception, match="if specified, 'languages' must be a list of strings"):
        Converter.from_multilangstring_to_langstrings(mls, languages=languages_input)


@pytest.mark.parametrize(
    "input_data, languages, expected_len",
    [
        ({"en-GB": {"Hello, mate"}, "fr-FR": {"Bonjour, ami"}}, None, 2),  # Uncommon but valid language tags
        ({"en": {"Hello"}, "en": {"Hello again"}}, None, 1),  # Duplicate language in input, unusual but valid
        ({"en": {" Hello "}, "fr": {"Bonjour"}}, None, 2),  # Strings with spaces
        ({"EN": {"UPPERCASE"}, "fr": {"lowercase"}}, None, 2),  # Mixed case languages
        ({"en-US": {"Howdy, partner"}, "fr-CA": {"Salut, partenaire"}}, None, 2),  # Region-specific language tags
        ({"zh": {"你好"}}, None, 1),  # Non-Latin script
        ({"special-👾": {"Special char and emoji in lang"}}, None, 1),  # Special characters and emojis in language tag
    ],
)
def test_from_multilangstring_to_langstrings_edge_cases(input_data, languages, expected_len):
    """Test the from_multilangstring_to_langstrings method for edge cases and unusual but valid usage scenarios."""
    mls = MultiLangString(mls_dict=input_data)
    result = Converter.from_multilangstring_to_langstrings(mls, languages=languages)
    assert len(result) == expected_len, f"Expected length of result is {expected_len}, but got {len(result)}."


# Note: It's assumed that MultiLangString cannot be None, so a test for null input is not included.
