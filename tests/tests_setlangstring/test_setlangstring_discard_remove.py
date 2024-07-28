import pytest
from langstring import LangString
from langstring import SetLangString


def calculate_expected_result_for_remove_discard(texts, lang, element, method):
    result = texts.copy()
    if isinstance(element, str):
        if method == "remove" and element not in result:
            raise KeyError(f"Element '{element}' not found in SetLangString")
        result.discard(element)
    elif isinstance(element, LangString) and element.lang.casefold() == lang.casefold():
        if method == "remove" and element.text not in result:
            raise KeyError(f"Element '{element.text}' not found in SetLangString")
        result.discard(element.text)
    return result


@pytest.mark.parametrize(
    "texts, lang, element, method, expected_exception",
    [
        # Valid string removal/discard
        ({"hello", "world"}, "en", "world", "remove", None),
        ({"hello", "world"}, "en", "world", "discard", None),
        # Valid LangString removal/discard
        ({"hello", "world"}, "en", LangString(text="world", lang="EN"), "remove", None),
        ({"hello", "world"}, "en", LangString(text="world", lang="EN"), "discard", None),
        # LangString with different language (should raise ValueError)
        ({"hello", "world"}, "en", LangString(text="monde", lang="fr"), "remove", ValueError),
        ({"hello", "world"}, "en", LangString(text="monde", lang="fr"), "discard", ValueError),
        # Invalid type (should raise TypeError)
        ({"hello", "world"}, "en", 123, "remove", TypeError),
        ({"hello", "world"}, "en", 123, "discard", TypeError),
        # Removing/discarding non-existent element (remove should raise KeyError)
        ({"hello", "world"}, "en", "universe", "remove", KeyError),
        ({"hello", "world"}, "en", "universe", "discard", None),
        # Case sensitivity checks
        ({"Hello", "World"}, "eN", "hello", "remove", KeyError),
        ({"Hello", "World"}, "eN", "hello", "discard", None),
        # Removing/discarding from an empty SetLangString
        (set(), "en", "world", "remove", KeyError),
        (set(), "en", "world", "discard", None),
        # LangString with uppercase language code
        ({"hello", "world"}, "eN", LangString(text="world", lang="EN"), "remove", None),
        ({"hello", "world"}, "eN", LangString(text="world", lang="EN"), "discard", None),
        # LangString with mixed case text
        ({"Hello", "World"}, "eN", LangString(text="World", lang="en"), "remove", None),
        ({"Hello", "World"}, "eN", LangString(text="World", lang="en"), "discard", None),
        # Special characters and numbers
        ({"hello1", "#world"}, "eN", "hello1", "remove", None),
        ({"hello1", "#world"}, "eN", "#world", "discard", None),
        # Unicode and emojis
        ({"👋", "🌍"}, "en", "👋", "remove", None),
        ({"👋", "🌍"}, "en", "🌍", "discard", None),
        # LangString with special characters and emojis
        ({"hello", "world"}, "en", LangString(text="🌍", lang="eN"), "remove", KeyError),
        ({"hello", "world"}, "en", LangString(text="🌍", lang="eN"), "discard", None),
        # LangString with numeric text
        ({"1", "2", "3"}, "en", LangString(text="2", lang="en"), "remove", None),
        ({"1", "2", "3"}, "en", LangString(text="4", lang="en"), "discard", None),
    ],
)
def test_remove_discard(texts, lang, element, method, expected_exception):
    set_lang_string = SetLangString(texts=texts, lang=lang)
    operation = getattr(set_lang_string, method)

    if expected_exception:
        with pytest.raises(expected_exception):
            operation(element)
    else:
        expected_texts = calculate_expected_result_for_remove_discard(texts, lang, element, method)
        operation(element)
        assert set_lang_string.texts == expected_texts, f"Failed to {method} '{element}' from {set_lang_string}"
