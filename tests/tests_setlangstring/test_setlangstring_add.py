import pytest
from langstring import LangString
from langstring import SetLangString


def calculate_expected_result_for_add(texts, lang, new_element):
    result = texts.copy()
    if isinstance(new_element, str):
        result.add(new_element)
    elif isinstance(new_element, LangString):
        if new_element.lang.casefold() == lang.casefold():
            result.add(new_element.text)
    return result


@pytest.mark.parametrize(
    "texts, lang, new_element, expected_exception",
    [
        # Adding valid string
        ({"hello"}, "en", "world", None),
        # Adding valid LangString
        ({"hello"}, "en", LangString(text="world", lang="en"), None),
        # Adding LangString with different language
        ({"hello"}, "en", LangString(text="monde", lang="fr"), ValueError),
        # Adding invalid type (should raise TypeError)
        ({"hello"}, "en", 123, TypeError),
    ],
)
def test_add(texts, lang, new_element, expected_exception):
    set_lang_string = SetLangString(texts=texts, lang=lang)

    if expected_exception:
        with pytest.raises(expected_exception):
            set_lang_string.add(new_element)
    else:
        expected_texts = calculate_expected_result_for_add(texts, lang, new_element)
        set_lang_string.add(new_element)
        assert set_lang_string.texts == expected_texts, f"Failed to add '{new_element}' to {set_lang_string}"
