import pytest
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang, texts, clean_empty, expected_result",
    [
        # Default case
        ("en", {"hello", "world"}, False, True),
        # Null case - Assuming a test for attempting to remove a null SetLangString
        # Invalid type for texts - Not applicable as SetLangString constrains texts to sets
        # Valid and invalid values
        ("en", {"valid_text"}, True, False),
        ("xx", {"nonexistent_language"}, False, True),  # Invalid language code, assuming it's treated as non-existent
        # Edge cases
        ("en", {"edge_case_text"}, True, False),
        # Unusual, but valid usage
        ("en", {"unusual_text1", "unusual_text2"}, False, True),
    ],
)
def test_remove_setlangstring(lang, texts, clean_empty, expected_result):
    """Test removing SetLangString from MultiLangString under various conditions.

    :param lang: Language code for the SetLangString.
    :param texts: A set of texts in the specified language.
    :param clean_empty: Whether to clean up the language entry if it becomes empty.
    :param expected_result: Expected result after removal operation.
    """
    mls = MultiLangString({lang: texts})
    sls = SetLangString(texts=texts, lang=lang)
    mls.remove_setlangstring(sls, clean_empty=clean_empty)
    assert (lang in mls.mls_dict) is expected_result, "The remove_setlangstring method didn't perform as expected."


@pytest.mark.parametrize(
    "initial_contents, lang_to_remove, clean_empty, expected_contents",
    [
        # Attempting to remove a SetLangString from an empty MultiLangString
        ({}, "en", False, {}),
        # Removing a SetLangString when its language is not present in MultiLangString
        ({"fr": {"bonjour"}}, "en", False, {"fr": {"bonjour"}}),
        # clean_empty True, language present and becomes empty after removal
        ({"en": {"hello"}}, "en", True, {}),
        # clean_empty False, language present and becomes empty after removal
        ({"en": {"hello"}}, "en", False, {"en": set()}),
        # Language present with multiple texts, only one text matches for removal
        ({"en": {"hello", "world"}}, "en", False, {"en": set()}),
        ({"en": {"hello", "world"}}, "en", True, {}),
        # SetLangString with multiple texts removing multiple entries
        ({"en": {"hello", "world", "test"}}, "en", False, {"en": set()}),
        ({"en": {"hello", "world", "test"}}, "en", True, {}),
    ],
)
def test_remove_setlangstring_valid_cases(initial_contents, lang_to_remove, clean_empty, expected_contents):
    """Test the remove_setlangstring method for various valid scenarios including edge cases.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param lang_to_remove: Language of the SetLangString to remove.
    :param clean_empty: Flag to clean up the language entry if it becomes empty.
    :param expected_contents: Expected contents of the MultiLangString after removal.
    """
    mls = MultiLangString(initial_contents)
    sls = SetLangString(texts=initial_contents.get(lang_to_remove, set()), lang=lang_to_remove)
    mls.remove_setlangstring(sls, clean_empty=clean_empty)
    assert (
        mls.mls_dict == expected_contents
    ), "The MultiLangString contents after removal did not match the expected result."


@pytest.mark.parametrize(
    "initial_contents, invalid_input, clean_empty, expected_exception",
    [
        # Attempting to remove with an invalid type for SetLangString
        ({"en": {"hello"}}, 123, False, TypeError),
    ],
)
def test_remove_setlangstring_invalid_cases(initial_contents, invalid_input, clean_empty, expected_exception):
    """Test the remove_setlangstring method for various invalid scenarios to ensure proper error handling.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param invalid_input: Invalid input attempting to remove.
    :param clean_empty: Flag to clean up the language entry if it becomes empty.
    :param expected_exception: Expected exception type if an error is expected.
    :param expected_message: Expected message in the exception if an error is expected.
    """
    mls = MultiLangString(initial_contents)
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_setlangstring(invalid_input, clean_empty=clean_empty)


@pytest.mark.parametrize(
    "start_dict",
    [{"en": {"test"}}, {"en": set()}],
)
def test_remove_empty(start_dict):
    mls = MultiLangString(start_dict, "en")
    sls = SetLangString(texts=set(), lang="en")
    mls.remove_setlangstring(sls)
    assert mls.mls_dict == start_dict
