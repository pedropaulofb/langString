import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.fixture
def sample_mls():
    """Fixture to provide a MultiLangString instance with predefined languages and texts."""
    return MultiLangString(
        mls_dict={"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}, "es": {"Hola", "Mundo"}, "": {"NoLangText"}}
    )


@pytest.mark.parametrize(
    "lang_to_remove",
    [
        "es",
        "fr",
        "en",
        "En",
        "EN",
        "",
    ],
)
def test_remove_existing_language(sample_mls: MultiLangString, lang_to_remove: str):
    """Test removing languages that exist in the MultiLangString with different cases.

    :param sample_mls: A MultiLangString instance for testing.
    :param lang_to_remove: The language code to be removed from the MultiLangString.
    """

    sample_mls.remove_lang(lang_to_remove)
    assert lang_to_remove.lower() not in [
        key.lower() for key in sample_mls.mls_dict
    ], f"Failed to remove existing language '{lang_to_remove}'."


@pytest.mark.parametrize(
    "lang_to_remove",
    [
        "de",  # Non-existing language
        " en",  # Leading space
        "en ",  # Trailing space
        " en ",  # Leading and trailing spaces
        "ru",  # Non-existing language
        "it",  # Non-existing language
        "DA",  # Non-existing language
        "   ",  # Spaces only
        "ελ",  # Greek, non-existing
        "рус",  # Cyrillic, non-existing
        "🚀",  # Emoji, non-existing
        "<script>",  # Injection attack vector, non-existing
        "\n",  # Newline character, non-existing
        "\t",  # Tab character, non-existing
    ],
)
def test_remove_nonexistent_language(sample_mls: MultiLangString, lang_to_remove: str):
    """Test attempting to remove languages that do not exist in the MultiLangString.

    :param sample_mls: A MultiLangString instance for testing.
    :param lang_to_remove: The language code attempted to be removed from the MultiLangString.
    """
    original_dict = sample_mls.mls_dict.copy()
    with pytest.raises(ValueError, match=f"Lang '{lang_to_remove}' not found in the MultiLangString."):
        sample_mls.remove_lang(lang_to_remove)
    assert (
        sample_mls.mls_dict == original_dict
    ), "MultiLangString contents changed after attempting to remove a non-existent language."


@pytest.mark.parametrize("invalid_lang", [None, 123, [], {}])
def test_remove_lang_with_invalid_type(sample_mls: MultiLangString, invalid_lang):
    """Test attempting to remove a language using an invalid type for `lang`.

    :param sample_mls: A MultiLangString instance for testing.
    :param invalid_lang: An invalid language identifier to test type validation.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        sample_mls.remove_lang(invalid_lang)


def test_remove_lang_with_empty_string_affects_target_language(sample_mls: MultiLangString):
    """Test removing a language represented by an empty string affects only the targeted language.

    :param sample_mls: A MultiLangString instance for testing.
    """
    sample_mls.remove_lang("")
    assert "" not in sample_mls.mls_dict, "Failed to remove language represented by an empty string."
