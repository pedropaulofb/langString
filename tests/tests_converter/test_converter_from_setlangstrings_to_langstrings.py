import pytest
from langstring import Converter
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, expected_output",
    [
        ({"Hello", "Hi"}, "en", ['"Hello"@en', '"Hi"@en']),
        ({"Bonjour"}, "fr", ['"Bonjour"@fr']),
        ({"😊", "👍"}, "emoji", ['"😊"@emoji', '"👍"@emoji']),
        ({"    "}, "en", ['"    "@en']),  # Text with spaces
        (set(), "en", []),  # Empty SetLangString
        ({"123", "456"}, "num", ['"123"@num', '"456"@num']),  # Numeric-like strings
        ({"ENGLISH", "english"}, "en", ['"ENGLISH"@en', '"english"@en']),  # Case variation in texts
        ({"Español", "Français"}, "multi", ['"Español"@multi', '"Français"@multi']),  # Multiple languages in texts
        ({" "}, "whitespace", ['" "@whitespace']),  # Single space text
        ({"", "    "}, "empty_or_spaces", ['""@empty_or_spaces', '"    "@empty_or_spaces']),  # Empty and spaces
        ({"Καλημέρα", "Привет"}, "intl", ['"Καλημέρα"@intl', '"Привет"@intl']),  # Greek and Cyrillic
        ({"#python", "$$$"}, "special_chars", ['"$$$"@special_chars', '"#python"@special_chars']),  # Special characters
        ({"Hello World"}, "mixed_case", ['"Hello World"@mixed_case']),  # Mixed case
        (
            {" leading space", "trailing space "},
            "spaces",
            ['" leading space"@spaces', '"trailing space "@spaces'],
        ),  # Spaces
    ],
)
def test_from_setlangstrings_to_langstrings_varied_texts(texts: set[str], lang: str, expected_output: list[str]):
    """Test conversion from SetLangString to LangStrings with varied texts and languages.
    :param texts: A set of text strings.
    :param lang: The language code.
    :param expected_output: A list of the actual string representations of the expected LangString outputs.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstrings_to_langstrings([set_lang_string])

    sorted_result = sorted([str(langstring) for langstring in result])
    sorted_expected_output = sorted(expected_output)

    assert (
        sorted_result == sorted_expected_output
    ), f"Converted LangStrings mismatch expected output. Got {sorted_result}"


@pytest.mark.parametrize(
    "invalid_input",
    [
        123,
        "string",
        None,
    ],
)
def test_from_setlangstrings_to_langstrings_invalid_type(invalid_input):
    """Test from_setlangstrings_to_langstrings raises TypeError for invalid input types.

    :param invalid_input: An input expected to raise TypeError.
    :param match_error: The error message expected to match the TypeError.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstrings_to_langstrings(invalid_input)


# Testing invalid types within SetLangString texts
@pytest.mark.parametrize(
    "texts, lang",
    [
        ([123, 456], "num"),  # List instead of set, containing numbers
        ({"Hello", 123}, "mixed"),  # Set containing both string and number
    ],
)
def test_from_setlangstrings_to_langstrings_invalid_text_types(texts, lang):
    """Test handling of invalid text types within SetLangString."""
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        set_lang_string = SetLangString(texts=texts, lang=lang)
        Converter.from_setlangstrings_to_langstrings([set_lang_string])


def test_from_setlangstrings_to_langstrings_preserves_input():
    """Ensure the original SetLangString is not modified during conversion."""
    original_texts = {"Hello", "Hi"}
    lang = "en"
    set_lang_string = SetLangString(texts=original_texts, lang=lang)
    Converter.from_setlangstrings_to_langstrings([set_lang_string])
    assert set_lang_string.texts == original_texts and set_lang_string.lang == lang, "Input SetLangString was modified."


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"select * from users;"}, "sql"),  # SQL injection-like text
        ({"<script>alert('XSS')</script>"}, "html"),  # XSS-like text
        ({"def", "class", "import"}, "python_keywords"),  # Python reserved keywords
    ],
)
def test_from_setlangstrings_to_langstrings_unusual_usage(texts, lang):
    """Test conversion with unusual but valid texts.
    :param texts: A set of unusual text strings.
    :param lang: The language code.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstrings_to_langstrings([set_lang_string])
    assert len(result) == len(texts), "Conversion did not handle unusual texts correctly."
