import pytest

from langstring import MultiLangString


def test_discard_text_in_pref_lang_removes_existing_text():
    """
    Test that `discard_text_in_pref_lang` removes an existing text entry in the preferred language.
    """
    mls = MultiLangString({"en": {"Hello", "World"}}, "en")
    mls.discard_text_in_pref_lang("Hello")
    assert "Hello" not in mls.mls_dict["en"], "Text 'Hello' should be removed from the preferred language"


def test_discard_text_in_pref_lang_does_nothing_when_text_not_present():
    """
    Test that `discard_text_in_pref_lang` does nothing when the text is not present in the preferred language.
    """
    mls = MultiLangString({"en": {"Hello"}}, "en")
    mls.discard_text_in_pref_lang("World")  # "World" is not in the set
    assert "Hello" in mls.mls_dict["en"], "Text 'Hello' should remain in the preferred language"


@pytest.mark.parametrize(
    "initial_contents, text_to_discard, expected_result",
    [
        ({"en": {"Hello", "World"}}, "Hello", {"en": {"World"}}),
        ({"en": {"Hello"}}, "Hello", {"en": set()}),
        ({"en": {"Hello"}}, "World", {"en": {"Hello"}}),  # Text to discard is not present
        (
            {"fr": {"Bonjour"}, "en": {"Hello"}},
            "Hello",
            {"en": set(), "fr": {"Bonjour"}},
        ),  # Discard from non-default language
        ({"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}}, "World", {"en": {"Hello"}, "es": {"Hola", "Mundo"}}),
        ({"en": {"Hello"}}, "", {"en": {"Hello"}}),  # Discarding an empty string
        ({"en": set()}, "Hello", {"en": set()}),  # Discarding from an empty language set
    ],
)
def test_discard_text_in_pref_lang_various_scenarios_off(
    initial_contents: dict, text_to_discard: str, expected_result: dict
):
    """
    Test `discard_text_in_pref_lang` across various scenarios including non-default languages and absence of text.
    """
    mls = MultiLangString(initial_contents, "en")
    mls.discard_text_in_pref_lang(text_to_discard)
    assert (
        mls.mls_dict == expected_result
    ), f"After discarding '{text_to_discard}', expected {expected_result} but got {mls.mls_dict}"


@pytest.mark.parametrize(
    "initial_contents, text_to_discard, expected_result",
    [
        ({"en": {"Hello", "World"}}, "Hello", {"en": {"World"}}),
        ({"en": {"Hello"}}, "Hello", {}),
        ({"en": {"Hello"}}, "World", {"en": {"Hello"}}),  # Text to discard is not present
        ({"fr": {"Bonjour"}, "en": {"Hello"}}, "Hello", {"fr": {"Bonjour"}}),  # Discard from non-default language
        (
            {"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}},
            "Mundo",
            {"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}},
        ),
        ({"en": {"Hello"}}, "", {"en": {"Hello"}}),  # Discarding an empty string, with flag on
        ({"en": set()}, "Hello", {"en": set()}),  # Discarding from an empty language set, with CLEAN_EMPTY_LANG flag
    ],
)
def test_discard_text_in_pref_lang_various_scenarios_on(
    initial_contents: dict, text_to_discard: str, expected_result: dict
):
    """
    Test `discard_text_in_pref_lang` across various scenarios including non-default languages and absence of text.
    """
    mls = MultiLangString(initial_contents, "en")
    mls.discard_text_in_pref_lang(text_to_discard, True)
    assert (
        mls.mls_dict == expected_result
    ), f"After discarding '{text_to_discard}', expected {expected_result} but got {mls.mls_dict}"


def test_discard_text_in_pref_lang_with_empty_mls():
    """
    Test that `discard_text_in_pref_lang` handles an empty MultiLangString correctly.
    """
    mls = MultiLangString({}, "en")
    mls.discard_text_in_pref_lang("Hello")  # Attempting to discard from an empty MultiLangString
    assert mls.mls_dict == {}, "MultiLangString should remain empty after discarding text from an empty MultiLangString"


def test_discard_text_in_pref_lang_with_invalid_text_type():
    """
    Test that `discard_text_in_pref_lang` raises a TypeError when provided with an invalid text type.
    """
    mls = MultiLangString({"en": {"Hello"}}, "en")
    with pytest.raises(TypeError, match="Argument '.+' must be of type 'str', but got"):
        mls.discard_text_in_pref_lang(123)  # Invalid text type


@pytest.mark.parametrize(
    "text_to_discard",
    [
        None,
        123,
    ],
)
def test_discard_text_in_pref_lang_with_invalid_values(text_to_discard):
    """
    Test that `discard_text_in_pref_lang` raises a TypeError with a descriptive message for null and invalid value types.
    """
    mls = MultiLangString({"en": {"Hello"}}, "en")
    with pytest.raises(TypeError, match="Argument .+ must be of type 'str', but got"):
        mls.discard_text_in_pref_lang(text_to_discard)
