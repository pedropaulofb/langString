import pytest
from langstring import LangString
from langstring import SetLangString


def calculate_expected_result(texts, langstring):
    """
    Calculate the expected result of adding a LangString to a set of texts.

    :param texts: The initial set of texts.
    :param langstring: The LangString to add.
    :return: The expected set of texts after addition.
    """
    expected_texts = texts.copy()
    if langstring.lang.casefold() == langstring.lang.casefold():
        expected_texts.add(langstring.text)
    return expected_texts


@pytest.mark.parametrize(
    "texts, lang, langstring_text, langstring_lang, expected_exception",
    [
        # Adding compatible LangString
        ({"hello"}, "en", "world", "en", None),
        # Adding LangString with different language
        ({"hello"}, "en", "world", "fr", ValueError),
        # Adding LangString with empty text
        ({"hello"}, "en", "", "en", None),
        # Adding LangString to empty SetLangString
        (set(), "en", "world", "en", None),
        # Adding LangString with uppercase language code
        ({"hello"}, "EN", "world", "EN", None),
    ],
)
def test_add_langstring(texts, lang, langstring_text, langstring_lang, expected_exception):
    """
    Test the add_langstring method.

    :param texts: Initial texts in the SetLangString.
    :param lang: Language of the SetLangString.
    :param langstring_text: Text of the LangString to add.
    :param langstring_lang: Language of the LangString to add.
    :param expected_exception: Expected exception, if any.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    langstring = LangString(text=langstring_text, lang=langstring_lang)
    expected_texts = calculate_expected_result(texts, langstring)

    if expected_exception:
        with pytest.raises(expected_exception):
            set_lang_string.add_langstring(langstring)
    else:
        set_lang_string.add_langstring(langstring)
        assert (
            set_lang_string.texts == expected_texts
        ), f"Texts mismatch: expected {expected_texts}, got {set_lang_string.texts}"
