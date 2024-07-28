import pytest
from langstring import Converter
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.fixture
def mls_with_multiple_languages():
    return MultiLangString(mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}, "es": {"Hola", "Mundo"}})


@pytest.mark.parametrize("invalid_input", [None, 123, "string", [], {}, LangString(), True])
def test_from_multilangstring_to_setlangstrings_invalid_type(invalid_input):
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstring_to_setlangstrings(invalid_input)


def test_from_multilangstring_to_setlangstrings_empty_multilangstring():
    mls = MultiLangString()
    result = Converter.from_multilangstring_to_setlangstrings(mls)
    assert isinstance(result, list), "Result should be a list"
    assert not result, "Result list should be empty for an empty MultiLangString"


@pytest.mark.parametrize(
    "mls_dict, expected_langs_texts",
    [
        ({"en": {"Hello", "World"}}, [("en", {"Hello", "World"})]),
        (
            {"fr": {"Bonjour", "Monde"}, "es": {"Hola", "Mundo"}},
            [("fr", {"Bonjour", "Monde"}), ("es", {"Hola", "Mundo"})],
        ),
        ({"de": set(), "it": {"Ciao"}}, [("de", set()), ("it", {"Ciao"})]),  # Testing empty language set
        ({}, []),  # Testing completely empty MultiLangString
        # Testing with multiple texts in the same language
        (
            {"en": {"Hello", "Good morning"}, "fr": {"Bonjour", "Bonsoir"}},
            [("en", {"Hello", "Good morning"}), ("fr", {"Bonjour", "Bonsoir"})],
        ),
        ({"en": {" ", "  "}}, [("en", {" ", "  "})]),  # Spaces as valid texts
        (
            {"ru": {"Привет", "Мир"}, "el": {"Γειά", "Κόσμος"}},  # Cyrillic and Greek characters
            [("ru", {"Привет", "Мир"}), ("el", {"Γειά", "Κόσμος"})],
        ),
        ({"emoji": {"😊", "😂"}}, [("emoji", {"😊", "😂"})]),  # Emojis as valid texts
        (
            {"mixed": {"Hello", "HELLO", "hello"}},  # Different cases considered distinct
            [("mixed", {"Hello", "HELLO", "hello"})],
        ),
        (
            {"special": {"Hello@world", "Hi#there"}},  # Special characters in texts
            [("special", {"Hello@world", "Hi#there"})],
        ),
    ],
)
def test_from_multilangstring_to_setlangstrings_basic_conversion(mls_dict, expected_langs_texts):
    mls = MultiLangString(mls_dict=mls_dict)
    result = Converter.from_multilangstring_to_setlangstrings(mls)
    assert len(result) == len(expected_langs_texts), "Number of SetLangString objects does not match expected count"
    for lang, texts in expected_langs_texts:
        found_sls = next((sls for sls in result if sls.lang == lang and sls.texts == texts), None)
        assert found_sls is not None, f"SetLangString for language {lang} with texts {texts} not found"


@pytest.mark.parametrize(
    "languages, expected_len",
    [
        (["en"], 1),
        (["en", "fr"], 2),
        (["de"], 0),
        ([], 0),
        (["ru", "el"], 0),  # Cyrillic and Greek languages not present
        (["emoji"], 0),  # Emoji language not present
        (["mixed"], 0),  # Mixed case language not present
        (["special"], 0),  # Special characters in language not present
    ],
)
def test_from_multilangstring_to_setlangstrings_with_languages_param(
    mls_with_multiple_languages, languages, expected_len
):
    result = Converter.from_multilangstring_to_setlangstrings(mls_with_multiple_languages, languages=languages)
    assert len(result) == expected_len, f"Expected {expected_len} SetLangString objects for languages {languages}"


@pytest.mark.parametrize(
    "lang, texts",
    [
        ("en", {"Hello", "World"}),
        ("fr", {"Bonjour", "Monde"}),  # Adding cases with spaces, special characters, different charset, and emojis
        ("spaced", {" Hello ", "World "}),  # Spaces before and after
        ("special", {"Hello@world", "<Hi#there>"}),  # Special characters
        ("greek", {"Γειά", "Κόσμος"}),  # Greek characters
        ("emoji", {"😊", "😂"}),  # Emojis
    ],
)
def test_from_multilangstring_to_setlangstrings_content_conversion(lang, texts):
    mls = MultiLangString(mls_dict={lang: texts})
    result = Converter.from_multilangstring_to_setlangstrings(mls)
    assert len(result) == 1, "Should return a single SetLangString object for one language"
    sls = result[0]
    assert sls.lang == lang and sls.texts == texts, "SetLangString content should match input MultiLangString"


@pytest.mark.parametrize(
    "mls_dict, expected_result",
    [
        # Single language with different casings should be merged into one.
        ({"en": {"Hello"}, "EN": {"Hi"}}, [("en", {"Hello", "Hi"})]),
        # Multiple casings for multiple languages, all should be merged by language.
        (
            {"En": {"Hello"}, "en": {"World"}, "EN": {"Hi"}, "fr": {"Bonjour"}, "FR": {"Salut"}},
            [("en", {"Hello", "World", "Hi"}), ("fr", {"Bonjour", "Salut"})],
        ),
        # No merging needed, single case per language.
        ({"de": {"Hallo"}, "it": {"Ciao"}}, [("de", {"Hallo"}), ("it", {"Ciao"})]),
        (
            {" en ": {"Hello"}, " EN ": {"Hi"}, " eN ": {"Hey"}},  # Spaces around language codes
            [(" en ", {"Hello", "Hi", "Hey"})],
        ),
        (
            {"special@": {"One", "Two"}, "SPECIAL@": {"Three"}},  # Special characters in language codes
            [("special@", {"One", "Two", "Three"})],
        ),
        (
            {"😊": {"Smile", "Joy"}, "😂": {"Laugh"}},  # Emojis as language codes
            [("😊", {"Smile", "Joy"}), ("😂", {"Laugh"})],
        ),
    ],
)
def test_from_multilangstring_to_setlangstrings_case_sensitivity(mls_dict, expected_result):
    mls = MultiLangString(mls_dict=mls_dict)
    result = Converter.from_multilangstring_to_setlangstrings(mls)

    # Ensure the number of SetLangStrings matches the expected number of unique languages, considering case insensitivity.
    assert len(result) == len(
        expected_result
    ), f"Expected {len(expected_result)} SetLangString objects, got {len(result)}"

    # Verify that each expected language and its texts are correctly represented in the result.
    for expected_lang, expected_texts in expected_result:
        sls = next((r for r in result if r.lang.lower() == expected_lang.lower()), None)
        assert sls is not None, f"Expected language '{expected_lang}' not found in result"
        assert sls.texts == set(
            expected_texts
        ), f"Mismatch in texts for language '{expected_lang}': expected {set(expected_texts)}, got {sls.texts}"


@pytest.mark.parametrize("invalid_languages", [123, "string", {}, LangString("Hello")])
def test_from_multilangstring_to_setlangstrings_invalid_languages_type(mls_with_multiple_languages, invalid_languages):
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstring_to_setlangstrings(mls_with_multiple_languages, languages=invalid_languages)
