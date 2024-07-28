import pytest
from langstring import SetLangString


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"a", "b", "c"}, "en"),
        ({"hello", "world"}, "en"),
        ({"1", "2", "3"}, "en"),
        ({"😊", "😂", "😜"}, "en"),
        (set(), "en"),  # Testing clear on an already empty set
        ({" ", "  "}, "en"),
        ({"long string", "another long string"}, "en"),
        ({"mixed", "123", "😊"}, "en"),
    ],
)
def test_clear_method(texts: set, lang: str) -> None:
    """
    Test the clear method of SetLangString.

    :param texts: A set of strings to initialize the SetLangString object.
    :param lang: The language code for the SetLangString object.
    :return: None. Asserts if the clear method works as expected.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    set_lang_string.clear()
    assert len(set_lang_string.texts) == 0, f"Clear method failed. Expected empty set, got {set_lang_string.texts}"


def test_clear_method_on_empty_set() -> None:
    """
    Test the clear method on an already empty SetLangString.

    :return: None. Asserts if the clear method works as expected on an empty set.
    """
    set_lang_string = SetLangString(texts=set(), lang="en")
    set_lang_string.clear()
    assert len(set_lang_string.texts) == 0, "Clear method failed on an empty set. Expected empty set, got non-empty set"


def test_clear_method_language_unchanged() -> None:
    """
    Test that the clear method does not change the language attribute of SetLangString.

    :return: None. Asserts if the language attribute remains unchanged after clear method.
    """
    lang = "en"
    set_lang_string = SetLangString(texts={"a", "b", "c"}, lang=lang)
    set_lang_string.clear()
    assert set_lang_string.lang == lang, "Clear method changed the language attribute."
