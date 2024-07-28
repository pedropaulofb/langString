import pytest
from langstring import SetLangString


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"hello", "world"}, "en"),
        ({"a", "b", "c"}, "en"),
        ({"1", "2", "3"}, "en"),
        ({"😊", "😂", "😜"}, "en"),
        (set(), "en"),  # Empty set
        ({"apple", "banana", "cherry"}, "en"),
        ({" ", "  ", "   "}, "en"),  # Spaces
    ],
)
def test_setlangstring_iter(texts, lang):
    """
    Test the __iter__ method of SetLangString.

    :param texts: A set of texts for the SetLangString.
    :param lang: The language of the SetLangString.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    iterated_texts = set(iter(set_lang_string))

    assert iterated_texts == texts, f"Iteration failed for SetLangString with texts {texts} and lang '{lang}'"
