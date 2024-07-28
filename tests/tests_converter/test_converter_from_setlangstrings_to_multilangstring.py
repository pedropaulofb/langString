import pytest
from langstring import Converter
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "setlangstrings, expected_texts_per_lang",
    [
        # Test with a single SetLangString with single language
        ([SetLangString(texts={"Hello", "World"}, lang="en")], {"en": {"Hello", "World"}}),
        # Test with multiple SetLangString objects with distinct languages
        (
            [SetLangString(texts={"Hello", "World"}, lang="en"), SetLangString(texts={"Hola", "Mundo"}, lang="es")],
            {"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}},
        ),
        # Test with multiple SetLangString objects with overlapping languages and texts
        (
            [SetLangString(texts={"Hello"}, lang="en"), SetLangString(texts={"World", "Hello"}, lang="en")],
            {"en": {"Hello", "World"}},
        ),
        # Test with SetLangString objects with diverse character sets (emojis, special characters)
        (
            [
                SetLangString(texts={"😀", "😁"}, lang="emoji"),
                SetLangString(texts={"Special&*()[]Characters"}, lang="special"),
            ],
            {"emoji": {"😀", "😁"}, "special": {"Special&*()[]Characters"}},
        ),
        # Test with empty SetLangString objects
        ([SetLangString(texts=set(), lang="")], {"": set()}),
        # Test with SetLangString objects having spaces in language tags and texts
        (
            [
                SetLangString(texts={" Text with leading and trailing spaces "}, lang=" en "),
                SetLangString(texts={" Another text "}, lang=" en "),
            ],
            {" en ": {" Text with leading and trailing spaces ", " Another text "}},
        ),
        # Test with SetLangString objects using different cases in language tags
        (
            [SetLangString(texts={"Lowercase text"}, lang="en"), SetLangString(texts={"Uppercase text"}, lang="EN")],
            {"en": {"Lowercase text", "Uppercase text"}},
        ),
        (
            [SetLangString(texts={"    "}, lang="en"), SetLangString(texts={"Empty spaces"}, lang="EN")],
            {"en": {"    ", "Empty spaces"}},
        ),  # Testing leading/trailing spaces in texts
        (
            [SetLangString(texts={"Γειά σου κόσμε"}, lang="el"), SetLangString(texts={"Καλημέρα"}, lang="EL")],
            {"el": {"Γειά σου κόσμε", "Καλημέρα"}},
        ),  # Greek characters, mixed case
        (
            [SetLangString(texts={"Привет", "мир"}, lang="ru"), SetLangString(texts={"Доброе утро"}, lang="RU")],
            {"ru": {"Привет", "мир", "Доброе утро"}},
        ),  # Cyrillic characters, mixed case
        (
            [
                SetLangString(texts={"Hello"}, lang="en"),
                SetLangString(texts={"world"}, lang="EN"),
                SetLangString(texts={"HELLO"}, lang="En"),
            ],
            {"en": {"Hello", "world", "HELLO"}},
        ),  # Mixed case languages with same tag
        (
            [SetLangString(texts={"👋", "🌍"}, lang="emoji"), SetLangString(texts={"😊"}, lang="EMOJI")],
            {"emoji": {"👋", "🌍", "😊"}},
        ),  # Emojis in texts, mixed case
    ],
)
def test_from_setlangstrings_to_multilangstring_valid(setlangstrings, expected_texts_per_lang):
    """
    Test `from_setlangstrings_to_multilangstring` method with various valid SetLangString inputs.

    :param setlangstrings: A list of SetLangString instances to be converted.
    :param expected_texts_per_lang: A dictionary mapping language tags to sets of expected texts.
    """
    result = Converter.from_setlangstrings_to_multilangstring(setlangstrings)

    assert isinstance(result, MultiLangString), "The result should be a MultiLangString instance."
    for lang, expected_texts in expected_texts_per_lang.items():
        assert result.mls_dict.get(lang) == expected_texts, f"Expected texts for '{lang}' do not match in the result."


@pytest.mark.parametrize(
    "input, error_type",
    [
        # Test with a non-list input
        (123, TypeError),
        # Test with a list containing non-SetLangString objects
        ([123], TypeError),
        # Test with None as input
        (None, TypeError),
    ],
)
def test_from_setlangstrings_to_multilangstring_invalid(input, error_type):
    """
    Test `from_setlangstrings_to_multilangstring` method with invalid inputs to ensure proper error handling.

    :param input: The input to be tested, expected to raise an error.
    :param error_type: The type of error expected to be raised.
    """
    with pytest.raises(error_type, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstrings_to_multilangstring(input)


@pytest.mark.parametrize(
    "setlangstrings, expected_texts_per_lang",
    [
        # Test with an empty list as input
        ([], {}),
        # Test with a list containing an empty SetLangString object
        ([SetLangString(texts=set(), lang="")], {"": set()}),
        # Test with a list containing multiple empty SetLangString objects with different languages
        (
            [
                SetLangString(texts=set(), lang=""),
                SetLangString(texts=set(), lang="en"),
                SetLangString(texts=set(), lang="es"),
            ],
            {"": set(), "en": set(), "es": set()},
        ),
    ],
)
def test_from_setlangstrings_to_multilangstring_special_cases(setlangstrings, expected_texts_per_lang):
    """
    Test `from_setlangstrings_to_multilangstring` method with special cases including an empty list and
    lists containing empty SetLangString objects.

    :param setlangstrings: A list of SetLangString instances to be converted, which may be empty or contain empty SetLangString objects.
    :param expected_texts_per_lang: A dictionary mapping language tags to sets of expected texts, which are expected to be empty in these cases.
    """
    result = Converter.from_setlangstrings_to_multilangstring(setlangstrings)

    assert isinstance(result, MultiLangString), "The result should be a MultiLangString instance."
    assert (
        result.mls_dict == expected_texts_per_lang
    ), "The result's language-text mapping does not match the expected empty mappings."


@pytest.mark.parametrize(
    "setlangstrings, expected_texts, lang_tag",
    [
        # Single language in lowercase, uppercase, and mixed case
        (
            [
                SetLangString(texts={"Hello"}, lang="en"),
                SetLangString(texts={"World"}, lang="EN"),
                SetLangString(texts={"Good morning"}, lang="En"),
                SetLangString(texts={"Good night"}, lang="eN"),
            ],
            {"Hello", "World", "Good morning", "Good night"},
            "en",
        ),
        # Another language with lowercase, uppercase, and mixed case
        (
            [
                SetLangString(texts={"Hola"}, lang="es"),
                SetLangString(texts={"Mundo"}, lang="ES"),
                SetLangString(texts={"Buenos días"}, lang="Es"),
                SetLangString(texts={"Buenas noches"}, lang="eS"),
            ],
            {"Hola", "Mundo", "Buenos días", "Buenas noches"},
            "es",
        ),
        (
            [SetLangString(texts={"Case"}, lang="pt"), SetLangString(texts={"Sensitive"}, lang="PT")],
            {"Case", "Sensitive"},
            "pt",
        ),  # Mixed case, but should result in lowercase 'pt'
        (
            [SetLangString(texts={"Only", "Lowercase"}, lang="de")],
            {"Only", "Lowercase"},
            "de",
        ),  # Single case, should retain 'de'
        (
            [SetLangString(texts={"ONLY", "UPPERCASE"}, lang="DE")],
            {"ONLY", "UPPERCASE"},
            "DE",
        ),  # Single uppercase case, should retain 'DE'
        (
            [
                SetLangString(texts={"Case"}, lang="fr"),
                SetLangString(texts={"folding"}, lang="FR"),
                SetLangString(texts={"Test"}, lang="Fr"),
            ],
            {"Case", "folding", "Test"},
            "fr",
        ),  # French language, mixed case
        (
            [
                SetLangString(texts={"uno", "dos"}, lang="es"),
                SetLangString(texts={"tres"}, lang="ES"),
            ],
            {"uno", "dos", "tres"},
            "es",
        ),  # Spanish language, mixed case
    ],
)
def test_from_setlangstrings_to_multilangstring_case_insensitivity_single_language(
    setlangstrings, expected_texts, lang_tag
):
    """
    Test `from_setlangstrings_to_multilangstring` with SetLangString objects for a single language tag in various casings,
    ensuring all texts are aggregated under the same language tag, treating the tag case-insensitively.

    :param setlangstrings: A list of SetLangString instances to be converted.
    :param expected_texts: A set of expected texts aggregated under the same language tag.
    :param lang_tag: The expected language tag after aggregation.
    """
    result = Converter.from_setlangstrings_to_multilangstring(setlangstrings)

    assert isinstance(result, MultiLangString), "The result should be a MultiLangString instance."
    assert len(result.mls_dict) == 1, f"Expected a single language tag, got {len(result.mls_dict)}"
    # Determine the correct key based on the expected behavior
    correct_key = lang_tag if len(set([sls.lang.casefold() for sls in setlangstrings])) == 1 else lang_tag.casefold()
    assert all(
        text in result.mls_dict[correct_key] for text in expected_texts
    ), f"Not all expected texts found under the aggregated language tag '{correct_key}'."


@pytest.mark.parametrize(
    "setlangstrings, expected_texts_per_lang",
    [
        # Testing with multiple languages and different casings
        (
            [
                SetLangString(texts={"Bonjour"}, lang="fr"),
                SetLangString(texts={"Monde"}, lang="FR"),
                SetLangString(texts={"Bonsoir"}, lang="Fr"),
                SetLangString(texts={"Bonne nuit"}, lang="fR"),
                SetLangString(texts={"Hello again"}, lang="EN"),
                SetLangString(texts={"Good evening"}, lang="eN"),
            ],
            {"fr": {"Bonjour", "Monde", "Bonsoir", "Bonne nuit"}, "en": {"Hello again", "Good evening"}},
        ),
        (
            [
                SetLangString(texts={"Mixed"}, lang="it"),
                SetLangString(texts={"Cases"}, lang="IT"),
                SetLangString(texts={"Bonjour"}, lang="fr"),
                SetLangString(texts={"Monde"}, lang="FR"),
            ],
            {"it": {"Mixed", "Cases"}, "fr": {"Bonjour", "Monde"}},
        ),  # Mixed IT/it and consistent FR/fr
        (
            [
                SetLangString(texts={"Hello"}, lang="en"),
                SetLangString(texts={"World"}, lang="EN"),
                SetLangString(texts={"Hallo"}, lang="nl"),
                SetLangString(texts={"Wereld"}, lang="NL"),
                SetLangString(texts={"Hola"}, lang="es"),
            ],
            {"en": {"Hello", "World"}, "nl": {"Hallo", "Wereld"}, "es": {"Hola"}},
        ),  # Mixed EN/en, consistent NL/nl, single es
    ],
)
def test_from_setlangstrings_to_multilangstring_case_insensitivity_multiple_languages(
    setlangstrings, expected_texts_per_lang
):
    """
    Test `from_setlangstrings_to_multilangstring` with SetLangString objects for multiple languages, each in various casings,
    ensuring texts for each language are correctly aggregated under case-insensitive language tags.

    :param setlangstrings: A list of SetLangString instances to be converted.
    :param expected_texts_per_lang: A dictionary mapping each language tag to its expected set of texts.
    """
    result = Converter.from_setlangstrings_to_multilangstring(setlangstrings)

    assert isinstance(result, MultiLangString), "The result should be a MultiLangString instance."
    for lang, expected_texts in expected_texts_per_lang.items():
        assert all(
            text in result.mls_dict[lang.lower()] for text in expected_texts
        ), f"Not all expected texts for {lang} found under the aggregated language tag."


@pytest.mark.parametrize(
    "setlangstrings, expected_output",
    [
        # Test to ensure language tags are preserved in uppercase if all are uppercase
        (
            [SetLangString(texts={"UPPERCASE", "ONLY"}, lang="DE")],
            [SetLangString(texts={"UPPERCASE", "ONLY"}, lang="DE")],
        ),
        # Test to ensure language tags are converted to lowercase if there's a variation in case
        (
            [
                SetLangString(texts={"MixedCase", "Test"}, lang="De"),
                SetLangString(texts={"ANOTHER", "TEST"}, lang="DE"),
            ],
            [SetLangString(texts={"MixedCase", "Test", "ANOTHER", "TEST"}, lang="de")],
        ),
        (
            [
                SetLangString(texts={"MixedCase", "Test"}, lang="De"),
                SetLangString(texts={"ANOTHER", "TEST"}, lang="De"),
            ],
            [SetLangString(texts={"MixedCase", "Test", "ANOTHER", "TEST"}, lang="De")],
        ),
        # Test to ensure language tags are preserved in lowercase if all are lowercase
        (
            [SetLangString(texts={"lowercase", "test"}, lang="de")],
            [SetLangString(texts={"lowercase", "test"}, lang="de")],
        ),
        # Test to ensure original casing is used when no duplicates exist
        (
            [SetLangString(texts={"unique"}, lang="EN"), SetLangString(texts={"distinct"}, lang="FR")],
            [SetLangString(texts={"unique"}, lang="EN"), SetLangString(texts={"distinct"}, lang="FR")],
        ),
        # Test to ensure casefolding occurs when there are multiple instances with varying cases
        (
            [SetLangString(texts={"first"}, lang="es"), SetLangString(texts={"second"}, lang="ES")],
            [SetLangString(texts={"first", "second"}, lang="es")],
        ),
    ],
)
def test_merge_setlangstrings_language_tag_casing(setlangstrings, expected_output):
    """
    Test `merge_setlangstrings` to verify it correctly handles language tag casing according to specified rules.

    :param setlangstrings: List of SetLangString instances to be merged.
    :param expected_output: Expected list of merged SetLangString instances, with appropriate language tag casing.
    """
    result = SetLangString.merge_setlangstrings(setlangstrings)
    assert len(result) == len(
        expected_output
    ), "The number of merged SetLangStrings does not match the expected output."
    for merged, expected in zip(result, expected_output):
        assert (
            merged.texts == expected.texts
        ), f"Expected texts {expected.texts} but got {merged.texts} for lang {expected.lang}."
        assert merged.lang == expected.lang, f"Expected language tag '{expected.lang}' but got '{merged.lang}'."
