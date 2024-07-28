import pytest
from langstring import Converter
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, expected_texts, expected_lang_tag",
    [
        ({"Hello", "World"}, "en", {"Hello", "World"}, "en"),
        (set(), "en", set(), "en"),  # Adjusted for an empty set with a language tag
        ({"Bonjour"}, "fr", {"Bonjour"}, "fr"),
        ({"Hola", "Mundo"}, "es", {"Hola", "Mundo"}, "es"),
    ],
)
def test_from_setlangstring_to_string_valid(texts, lang, expected_texts, expected_lang_tag):
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_string(set_lang_string)

    # Extract texts and language tag from the result
    result_texts_str, _, result_lang_tag = result.rpartition("@")
    result_texts = eval(result_texts_str) if result_texts_str != "{}" else set()

    # Assertions
    assert result_texts == expected_texts, f"Expected texts {expected_texts} but got {result_texts}."
    assert result_lang_tag == expected_lang_tag, f"Expected language tag {expected_lang_tag} but got {result_lang_tag}."


def test_from_setlangstring_to_string_invalid_type():
    """
    Test conversion of SetLangString to a string with invalid input type, expecting a TypeError.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstring_to_string("not a SetLangString")


# Test for valid cases including special characters, case sensitivity, and special combinations
@pytest.mark.parametrize(
    "texts, lang, expected_output",
    [
        ({"Hello", "World"}, "en", {"Hello", "World"}),  # Basic case
        ({"Bonjour"}, "fr", {"Bonjour"}),  # Single text
        ({"Hola", "Mundo"}, "es", {"Hola", "Mundo"}),  # Multiple texts
        ({"Hello, World", "Greetings: Earth"}, "en", {"Hello, World", "Greetings: Earth"}),  # Special characters
        ({"Apple", "apple"}, "en", {"Apple", "apple"}),  # Case sensitivity
        (
            {"Hello, World!", "😀🌍🔥", "こんにちは, 世界"},
            "multi",
            {"Hello, World!", "😀🌍🔥", "こんにちは, 世界"},
        ),  # Special combinations
    ],
)
def test_from_setlangstring_to_string_various_cases(texts, lang, expected_output):
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_string(set_lang_string)
    # Assuming result is a string representation of a set, evaluate to get the actual set
    result_texts = eval(result.split("@")[0])
    assert set(result_texts) == expected_output, f"Expected {expected_output} but got {result_texts}"


@pytest.mark.parametrize(
    "texts, lang, expected_exception",
    [
        ({}, "en", TypeError),  # None texts
        ({"Hello", None}, "en", TypeError),  # None value in set
        ("Hello", "en", TypeError),  # Invalid type for texts
        ({}, "en", TypeError),  # Empty dictionary instead of set
    ],
)
def test_from_setlangstring_to_string_none_values(texts, lang, expected_exception):
    with pytest.raises(expected_exception):
        SetLangString(texts=texts, lang=lang)


# Test for valid cases including special characters, case sensitivity, and special combinations
@pytest.mark.parametrize(
    "texts, lang, expected_output",
    [
        ({"Hello", "World"}, "en", {"Hello", "World"}),  # Basic case
        ({"Bonjour"}, "fr", {"Bonjour"}),  # Single text
        ({"Hola", "Mundo"}, "es", {"Hola", "Mundo"}),  # Multiple texts
        ({"Hello, World", "Greetings: Earth"}, "en", {"Hello, World", "Greetings: Earth"}),  # Special characters
        ({"Apple", "apple"}, "en", {"Apple", "apple"}),  # Case sensitivity
        (
            {"Hello, World!", "😀🌍🔥", "こんにちは, 世界"},
            "multi",
            {"Hello, World!", "😀🌍🔥", "こんにちは, 世界"},
        ),  # Special combinations
    ],
)
def test_from_setlangstring_to_string_various_cases(texts, lang, expected_output):
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_string(set_lang_string)
    # Assuming result is a string representation of a set, evaluate to get the actual set
    result_texts = eval(result.split("@")[0])
    assert set(result_texts) == expected_output, f"Expected {expected_output} but got {result_texts}"
