import pytest
from langstring import MultiLangString


def test_clean_empty_langs_with_no_empty_langs():
    """Ensure `clean_empty_langs` does not remove any languages when there are no empty languages."""
    mls = MultiLangString({"en": {"Hello", "World"}, "es": {"Hola"}})
    mls.remove_empty_langs()
    assert "en" in mls.mls_dict and "es" in mls.mls_dict, "Non-empty languages should not be removed"


def test_clean_empty_langs_with_empty_langs():
    """Test that `clean_empty_langs` removes only languages with empty text sets."""
    mls = MultiLangString({"en": {"Hello"}, "es": set(), "fr": set()})
    mls.remove_empty_langs()
    assert (
        "en" in mls.mls_dict and "es" not in mls.mls_dict and "fr" not in mls.mls_dict
    ), "Only empty languages should be removed"


def test_clean_empty_langs_with_all_empty_langs():
    """Check that `clean_empty_langs` clears the `mls_dict` completely when all languages are empty."""
    mls = MultiLangString({"en": set(), "es": set()})
    mls.remove_empty_langs()
    assert len(mls.mls_dict) == 0, "All languages should be removed when they are empty"


@pytest.mark.parametrize(
    "initial_mls_dict, expected_mls_dict",
    [
        ({"en": set(), "es": set()}, {}),
        ({"en": {"Hello"}, "es": set()}, {"en": {"Hello"}}),
        ({"en": {"Hello"}, "es": {"Holla"}}, {"en": {"Hello"}, "es": {"Holla"}}),
        ({"": {""}}, {"": {""}}),
        ({}, {}),
    ],
)
def test_clean_empty_langs_parametrized(initial_mls_dict, expected_mls_dict):
    """Parametrized test for `clean_empty_langs` to cover various initial and expected states."""
    mls = MultiLangString(initial_mls_dict)
    mls.remove_empty_langs()
    assert mls.mls_dict == expected_mls_dict, f"Expected {expected_mls_dict}, got {mls.mls_dict}"
