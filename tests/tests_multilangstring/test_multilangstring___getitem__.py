import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "lang, expected_set",
    [
        ("en", {"Hello World"}),  # Existing language
        ("EN", {"Hello World"}),  # Existing language
        ("es", {"Hola Mundo"}),  # Another existing language
        ("Es", {"Hola Mundo"}),  # Another existing language
    ],
)
def test_getitem_valid(lang: str, expected_set: set):
    """
    Test retrieval of valid language entries.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    assert mls[lang] == expected_set, f"Retrieving '{lang}' should return {expected_set}"


@pytest.mark.parametrize(
    "lang",
    [
        ("fr"),  # Non-existent language
        ("de"),  # Another non-existent language
        ("en "),
        ("en "),
        (" en "),
        ("ελ"),
        ("рус"),
        ("emoji"),
    ],
)
def test_getitem_key_error(lang: str):
    """
    Test that accessing non-existent language raises KeyError.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    with pytest.raises(KeyError, match=f".*{lang}.*"):
        _ = mls[lang]


@pytest.mark.parametrize(
    "lang",
    [
        (123),  # Integer
        (None),  # NoneType
        (["en"]),  # List
        ({}),  # Dictionary
        (set()),  # Empty set
    ],
)
def test_getitem_type_error(lang):
    """
    Test that providing an invalid type for language raises TypeError.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    with pytest.raises(TypeError):
        _ = mls[lang]


@pytest.mark.parametrize(
    "initial_contents, key_to_get, expected_result, expected_exception",
    [
        # Case 1: Retrieving an existing entry where the key is an empty string.
        ({"": {"An entry without language"}}, "", {"An entry without language"}, None),
        # Case 2: Attempting to retrieve using an empty string when no such entry exists.
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "", None, KeyError),
        # Case 3: MultiLangString contains only an empty string entry; it is retrieved.
        ({"": {"Only no language entry"}}, "", {"Only no language entry"}, None),
        # Case 4: MultiLangString is entirely empty, attempt to retrieve using an empty string.
        ({}, "", None, KeyError),
        # Case 5: MultiLangString contains multiple languages, including an empty string; the empty string entry is retrieved.
        ({"": {"No language entry"}, "en": {"Hello"}, "fr": {"Bonjour"}}, "", {"No language entry"}, None),
        # Case 6: Retrieving a non-empty key when an empty string entry exists.
        ({"": {"No language entry"}, "en": {"Hello"}}, "en", {"Hello"}, None),
    ],
)
def test_multilangstring_getitem_with_empty_string(initial_contents, key_to_get, expected_result, expected_exception):
    """
    Test the `__getitem__` method of the MultiLangString class for handling the empty string as a key across various scenarios.

    :param initial_contents: The initial contents to populate the MultiLangString instance.
    :param key_to_get: The key (language code) to attempt to retrieve, focusing on the empty string.
    :param expected_result: The expected result (set of texts) for the given key, or None if an exception is expected.
    :param expected_exception: The expected exception, if any; otherwise, None.
    """
    mls = MultiLangString(initial_contents)

    if expected_exception:
        with pytest.raises(expected_exception):
            _ = mls[key_to_get]
    else:
        result = mls[key_to_get]
        assert isinstance(result, set), "Expected result to be a set."
        assert result == expected_result, f"Expected texts for key '{key_to_get}' did not match."


@pytest.mark.parametrize(
    "key",
    [
        "en",  # Non-empty, existing language
        "fr",  # Non-empty, non-existing language
        " ",  # Space as key
        "Ελ",  # Greek characters as key, non-existing
        "Ру",  # Cyrillic characters as key, non-existing
        "en😀",  # Emoji in the key, non-existing
    ],
)
def test_multilangstring_getitem_various_non_empty_keys(key):
    """
    Additional test to ensure `__getitem__` method behaves correctly for various non-empty keys, including handling of non-existent keys.

    :param key: The key (language code) to attempt to retrieve.
    """
    initial_contents = {"en": {"Hello"}, "": {"No language entry"}}
    mls = MultiLangString(initial_contents)

    if key in initial_contents:
        result = mls[key]
        assert isinstance(result, set), "Expected result to be a set for non-empty keys."
        assert result == initial_contents[key], f"Retrieved texts for key '{key}' did not match expected."
    else:
        with pytest.raises(KeyError):
            _ = mls[key]
