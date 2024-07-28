import pytest
from langstring import LangString
from langstring import SetLangString
from langstring.converter import Converter


@pytest.mark.parametrize(
    "langstrings, expected_texts, expected_lang",
    [
        # Homogeneous language LangStrings
        ([LangString(text="Hello", lang="en"), LangString(text="World", lang="en")], {"Hello", "World"}, "en"),
        # Duplicate texts and the same language
        ([LangString(text="Duplicate", lang="en"), LangString(text="Duplicate", lang="en")], {"Duplicate"}, "en"),
        # The same text in different cases
        ([LangString(text="hello", lang="en"), LangString(text="Hello", lang="en")], {"hello", "Hello"}, "en"),
    ],
)
def test_from_langstrings_to_setlangstring_valid(langstrings, expected_texts, expected_lang):
    result = Converter.from_langstrings_to_setlangstring(langstrings)
    assert result.texts == expected_texts
    assert result.lang == expected_lang


def test_from_langstrings_to_setlangstring_empty_list():
    z = Converter.from_langstrings_to_setlangstring([])
    assert z == SetLangString()


@pytest.mark.parametrize(
    "langstrings",
    [
        # Mixed languages
        ([LangString(text="Hello", lang="en"), LangString(text="Bonjour", lang="fr")]),
    ],
)
def test_from_langstrings_to_setlangstring_mixed_languages(langstrings):
    with pytest.raises(ValueError):
        Converter.from_langstrings_to_setlangstring(langstrings)


@pytest.mark.parametrize(
    "langstrings, expected_texts, expected_lang",
    [
        # Single LangString
        ([LangString(text="Single", lang="en")], {"Single"}, "en"),
        # Special characters
        (
            [LangString(text="@Special&*()_", lang="en"), LangString(text="#$%^", lang="en")],
            {"@Special&*()_", "#$%^"},
            "en",
        ),
        # Leading/trailing whitespace
        (
            [LangString(text="  Leading", lang="en"), LangString(text="Trailing  ", lang="en")],
            {"  Leading", "Trailing  "},
            "en",
        ),
    ],
)
def test_from_langstrings_to_setlangstring_special_cases(langstrings, expected_texts, expected_lang):
    result = Converter.from_langstrings_to_setlangstring(langstrings)
    assert result.texts == expected_texts
    assert result.lang == expected_lang


# Ensure TypeError is raised for completely invalid input types
@pytest.mark.parametrize(
    "invalid_input",
    [
        "Not a list",
        123,
        None,
        [123, "string"],
    ],
)
def test_from_langstrings_to_setlangstring_invalid_input_type(invalid_input):
    with pytest.raises(TypeError):
        Converter.from_langstrings_to_setlangstring(invalid_input)
