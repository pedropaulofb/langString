import pytest
from langstring import SetLangString


def calculate_expected_result_for_add_text(texts, new_text):
    result = texts.copy()
    result.add(new_text)
    return result


@pytest.mark.parametrize(
    "texts, lang, new_text, expected_exception",
    [
        # Adding valid text
        ({"hello"}, "en", "world", None),
        # Adding text to empty SetLangString
        (set(), "en", "hello", None),
        # Adding duplicate text
        ({"hello"}, "en", "hello", None),
        # Adding invalid text (empty string)
        ({"hello"}, "en", "", None),
        # Adding invalid text (empty string)
        ({"hello"}, "en", None, TypeError),
        # Adding non-string type (should raise TypeError in validation)
        ({"hello"}, "en", 123, TypeError),
    ],
)
def test_add_text(texts, lang, new_text, expected_exception):
    set_lang_string = SetLangString(texts=texts, lang=lang)

    if expected_exception:
        with pytest.raises(expected_exception):
            set_lang_string.add_text(new_text)
    else:
        expected_texts = calculate_expected_result_for_add_text(texts, new_text)
        set_lang_string.add_text(new_text)
        assert set_lang_string.texts == expected_texts, f"Failed to add '{new_text}' to {set_lang_string}"
