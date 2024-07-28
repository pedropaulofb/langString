import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang, expected_keys",
    [
        ("en", ["es"]),  # Deleting existing language
        ("eN", ["es"]),  # Deleting existing language
        ("EN", ["es"]),  # Deleting existing language
        ("es-ES", ["en"]),  # Deleting language with region
    ],
)
def test_multilangstring_delitem_valid(lang: str, expected_keys: list):
    """
    Test the __delitem__ method for valid language deletion scenarios.

    :param lang: The language code to be deleted from the MultiLangString instance.
    :param expected_keys: The expected remaining language codes in the instance after deletion.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}, "es-ES": {"Hola Mundo Español"}})
    del mls[lang]
    assert (
        all(key in mls.mls_dict for key in expected_keys) and lang not in mls.mls_dict
    ), f"After deleting '{lang}', expected remaining keys are {expected_keys}."


@pytest.mark.parametrize(
    "lang, match_msg",
    [
        ("fr", "fr"),  # Attempt to delete non-existent language
        (" en", " en"),  # Non-existent language with trailing space
        ("EN ", "EN "),  # Non-existent language with trailing space
        ("", ""),  # Attempt to delete an empty string language code
        ("Ελ", "Ελ"),  # Attempt to delete a language with Greek characters
        ("Привет", "Привет"),  # Attempt to delete a language with Cyrillic characters
        ("🚀", "🚀"),  # Attempt to delete a language with emoji
        ("special-char#", "special-char#"),  # Attempt to delete a language with special characters
    ],
)
def test_multilangstring_delitem_key_error(lang: str, match_msg: str):
    """
    Test the __delitem__ method for scenarios where deletion should raise KeyError.

    :param lang: The language code attempted to be deleted, expected to not exist in the instance.

    :raises KeyError: If the language code does not exist in the MultiLangString instance.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    with pytest.raises(KeyError, match=match_msg):
        del mls[lang]


@pytest.mark.parametrize(
    "lang",
    [
        123,  # Non-string input: integer
        [],  # Non-string input: list
        {},  # Non-string input: dictionary
    ],
)
def test_multilangstring_delitem_type_error(lang: str):
    """Test the delitem method for type validation, expecting TypeError for invalid input types.
    :param lang: The invalid language code input, not of type str, to be tested for deletion.
    :raises TypeError: If the input is not of type str.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        del mls[lang]


def test_multilangstring_delitem_none_value():
    """
    Test the __delitem__ method for invalid values like null and empty strings, expecting TypeError.
    :param lang: The invalid language code input to be tested for deletion.
    :raises TypeError: If the input is null or an empty string.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        del mls[None]


@pytest.mark.parametrize(
    "lang, expected_exception, match_msg",
    [
        ("  es  ", KeyError, "  es  "),  # Valid language with extra spaces around
        ("en-US", KeyError, "en-US"),  # Attempting a locale-specific deletion that doesn't exist
    ],
)
def test_multilangstring_delitem_edge_cases(lang: str, expected_exception: type, match_msg: str):
    """
    Test the __delitem__ method for edge cases including unusual but potentially valid inputs.
    :param lang: The language code being tested for deletion.
    :param expected_exception: The type of exception expected to be raised.
    :param match_msg: The expected message in the exception.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}, "es": {"Hola Mundo"}})
    with pytest.raises(expected_exception, match=match_msg):
        del mls[lang]


@pytest.mark.parametrize(
    "initial_contents, key_to_delete, expected_contents, expected_exception",
    [
        # Case 1: Empty string as key exists, and it is deleted.
        ({"": {"No language entry"}, "en": {"Hello"}}, "", {"en": {"Hello"}}, None),
        # Case 2: Attempt to delete using empty string when it does not exist, other languages present.
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "", {"en": {"Hello"}, "fr": {"Bonjour"}}, KeyError),
        # Case 3: MultiLangString contains only an empty string entry, which is then deleted.
        ({"": {"Only no language entry"}}, "", {}, None),
        # Case 4: MultiLangString is empty, attempt to delete using empty string.
        ({}, "", {}, KeyError),
        # Case 5: MultiLangString contains multiple languages, including empty string, all are deleted except one.
        (
            {"": {"No language entry"}, "en": {"Hello"}, "fr": {"Bonjour"}},
            "fr",
            {"": {"No language entry"}, "en": {"Hello"}},
            None,
        ),
        # Case 6: Delete a non-empty key when an empty string entry exists.
        ({"": {"No language entry"}, "en": {"Hello"}}, "en", {"": {"No language entry"}}, None),
    ],
)
def test_multilangstring_delitem_with_empty_string(
    initial_contents, key_to_delete, expected_contents, expected_exception
):
    """
    Test the `__delitem__` method of the MultiLangString class for handling the empty string as a key, across various scenarios.

    :param initial_contents: The initial contents to populate the MultiLangString instance.
    :param key_to_delete: The key (language code) to attempt to delete.
    :param expected_contents: The expected contents of the MultiLangString instance after deletion.
    :param expected_exception: The expected exception, if any; otherwise, None.
    """
    mls = MultiLangString(initial_contents)

    if expected_exception:
        with pytest.raises(expected_exception):
            del mls[key_to_delete]
    else:
        del mls[key_to_delete]
        assert mls.mls_dict == expected_contents, "MultiLangString contents after deletion did not match expected."


# Additional checks to ensure method's behavior aligns with expectations.
def test_multilangstring_delitem_side_effects():
    """
    Test to ensure that deleting an item does not have unintended side effects on MultiLangString's internal state.
    """
    initial_contents = {"": {"No language entry"}, "en": {"Hello"}}
    mls = MultiLangString(initial_contents)
    del mls["en"]  # Deleting an existing key

    assert "" in mls.mls_dict, "Deleting a specified language key unexpectedly affected other keys."
    assert "en" not in mls.mls_dict, "Specified language key was not successfully deleted."
