import pytest
from langstring import LangString
from langstring import SetLangString


def calculate_expected_result_for_discard(texts, langstring):
    result = texts.copy()
    result.discard(langstring.text)
    return result


def calculate_expected_result_for_remove(texts, langstring):
    result = texts.copy()
    if langstring.text in result:
        result.remove(langstring.text)
    return result


@pytest.mark.parametrize(
    "texts, lang, langstring_text, langstring_lang, method_name",
    [
        # Discard/Remove existing LangString
        ({"hello", "world"}, "En", "world", "en", "discard_langstring"),
        ({"hello", "world"}, "EN", "world", "EN", "remove_langstring"),
        # Discard/Remove non-existing LangString
        ({"hello"}, "EN", "world", "en", "discard_langstring"),
        ({"hello"}, "en", "world", "eN", "remove_langstring"),
        # Discard/Remove from empty SetLangString
        (set(), "en", "world", "eN", "discard_langstring"),
        (set(), "en", "world", "en", "remove_langstring"),
    ],
)
def test_discard_remove_langstring(texts, lang, langstring_text, langstring_lang, method_name):
    set_lang_string = SetLangString(texts=texts, lang=lang)
    langstring = LangString(text=langstring_text, lang=langstring_lang)

    if method_name == "discard_langstring":
        expected_texts = calculate_expected_result_for_discard(texts, langstring)
        set_lang_string.discard_langstring(langstring)
    else:
        if langstring.text not in texts:
            with pytest.raises(KeyError):
                set_lang_string.remove_langstring(langstring)
            return
        expected_texts = calculate_expected_result_for_remove(texts, langstring)
        set_lang_string.remove_langstring(langstring)

    assert set_lang_string.texts == expected_texts, f"Failed {method_name} for {set_lang_string} with {langstring}"
