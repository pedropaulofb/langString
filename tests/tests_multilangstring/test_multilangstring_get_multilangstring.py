import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "langs, expected_keys",
    [
        (["en", "fr"], {"en", "fr"}),
        (["es"], {"es"}),
        (["en", "fr", "es"], {"en", "fr", "es"}),  # Valid multiple languages
        (["En", "FR", "Es"], {"FR", "Es", "En"}),  # Case insensitivity test
    ],
)
def test_get_multilangstring_success(langs, expected_keys):
    """Test get_multilangstring returns MultiLangString with only specified languages."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, pref_lang="en")
    result = mls.get_multilangstring(langs)
    assert isinstance(result, MultiLangString), "Result should be a MultiLangString instance"
    assert set(result.get_langs()) == expected_keys, f"Expected languages {expected_keys} not found in result"


@pytest.mark.parametrize(
    "langs",
    [
        ({"en": "Hello"}),
        ("en"),
        ([1, "en"]),
        (None),
        (["en", 1]),
    ],
)
def test_get_multilangstring_type_errors(langs):
    """Test get_multilangstring raises TypeError with invalid langs argument."""
    mls = MultiLangString({"en": {"Hello"}}, pref_lang="en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.get_multilangstring(langs)


@pytest.mark.parametrize(
    "langs, expected_empty",
    [
        ([], True),
        (["nonexistent"], True),  # Nonexistent language should return an empty MultiLangString
    ],
)
def test_get_multilangstring_with_empty_langs(langs, expected_empty):
    """Test get_multilangstring with an empty langs list returns an empty MultiLangString."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}}, pref_lang="en")
    result = mls.get_multilangstring(langs)
    assert (len(result.mls_dict) == 0) == expected_empty, "Expected an empty MultiLangString"


@pytest.mark.parametrize(
    "langs, expected_keys, description",
    [
        ([], set(), "empty langs list should return empty MultiLangString"),
        (["EN", "fr"], {"EN", "fr"}, "case insensitive check, 'EN' found because keys are case insensitive"),
        ([" en", "fr "], set(), "leading/trailing spaces in lang codes should be considered"),
        (["ελ", "рус"], {"ελ", "рус"}, "non-Latin characters in lang codes"),
        (["🙂", "#$%"], set(), "emojis and special characters in lang codes"),
        (["EN", "FR"], {"EN", "FR"}, "Should be case insensitive"),
        (["en", "fr", "ελ", "рус", "🙂"], {"en", "fr", "ελ", "рус"}, "Mixed valid and emoji lang codes"),
        (["", "  "], set(), "Only empty or space-only strings in lang codes"),  # Empty and space-only strings
    ],
)
def test_get_multilangstring_edge_cases(langs, expected_keys, description):
    """Test get_multilangstring handles edge cases appropriately."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "ελ": {"Γειά"}, "рус": {"Привет"}}, pref_lang="en")
    result = mls.get_multilangstring(langs)
    assert set(result.get_langs()) == expected_keys, f"{description}: Expected languages {expected_keys} not found"


@pytest.mark.parametrize(
    "langs, expected_exception",
    [
        (123, TypeError),
        ([False], TypeError),
    ],
)
def test_get_multilangstring_invalid_langs(langs, expected_exception):
    """Test get_multilangstring raises appropriate exceptions for invalid or nonexistent languages."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}}, pref_lang="en")
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.get_multilangstring(langs)


@pytest.mark.parametrize(
    "input_langs, expected_texts",
    [
        (["en"], {"Hello"}),
        (["fr", "en"], {"Bonjour", "Hello"}),
        (["ελ"], {"Γειά"}),  # Greek
        (["рус"], set()),  # Cyrillic
    ],
)
def test_get_multilangstring_correct_texts(input_langs, expected_texts):
    """Test get_multilangstring returns MultiLangString with correct texts for specified languages."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}, "ελ": {"Γειά"}}, pref_lang="en")
    result = mls.get_multilangstring(input_langs)
    all_texts = set()
    for lang in input_langs:
        all_texts.update(result.mls_dict.get(lang, set()))
    assert all_texts == expected_texts, "Expected texts do not match the returned MultiLangString texts"


@pytest.mark.parametrize(
    "langs, expected_result",
    [
        (["EN"], True),
        (["fr", "ES"], True),
        (["de"], False),  # Assuming 'de' (German) is not in the initial MultiLangString
        (["ελ", "рус", "🙂"], False),  # Greek, Cyrillic, and emoji
    ],
)
def test_get_multilangstring_lang_exists(langs, expected_result):
    """Test if get_multilangstring correctly identifies existence of specified languages, regardless of case."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, pref_lang="en")
    result = mls.get_multilangstring(langs)
    assert (
        set(result.get_langs()) == set([lang for lang in langs])
    ) == expected_result, "Existence of specified languages does not match expected result"


@pytest.mark.parametrize(
    "langs, expected_size",
    [
        (["en", "fr"], 2),
        (["es"], 1),
        (["en", "fr", "es"], 3),
        (["de"], 0),  # Assuming 'de' (German) is not in the initial MultiLangString
        (["ελ", "рус", "🙂"], 0),  # Greek, Cyrillic, and emoji should count only valid
    ],
)
def test_get_multilangstring_size(langs, expected_size):
    """Test get_multilangstring returns MultiLangString of expected size based on specified languages."""
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, pref_lang="en")
    result = mls.get_multilangstring(langs)
    assert (
        len(result.mls_dict) == expected_size
    ), "Size of the returned MultiLangString does not match the expected size"


@pytest.mark.parametrize(
    "langs, expected_contents",
    [
        (["en"], {"en": {"Hello"}}),
        (["fr", "en"], {"fr": {"Bonjour"}, "en": {"Hello"}}),
        (["es"], {"es": {"Hola"}}),
        (["ελ"], {"ελ": {"Γειά"}}),
        (["рус"], {"рус": {"Привет"}}),
    ],
)
def test_get_multilangstring_contents(langs, expected_contents):
    """
    Test get_multilangstring returns MultiLangString with correct languages and associated texts.

    :param langs: List of languages to filter the MultiLangString object.
    :param expected_contents: A dictionary with languages as keys and the expected set of texts as values.
    :return: None
    """
    mls = MultiLangString(
        {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}, "ελ": {"Γειά"}, "рус": {"Привет"}}, pref_lang="en"
    )
    result = mls.get_multilangstring(langs)
    assert all(
        lang in result.mls_dict and result.mls_dict[lang] == expected_contents[lang] for lang in langs
    ), "The contents of the returned MultiLangString do not match the expected contents"
