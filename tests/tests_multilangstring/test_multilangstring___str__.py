import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag


@pytest.mark.parametrize("print_with_lang, expected_output", [(True, "{}"), (False, "{}")])
def test_multi_lang_string_str_empty(print_with_lang: bool, expected_output: str):
    """Test __str__ method with an empty MultiLangString.

    :param print_with_lang: Flag to indicate if language tags should be included in the output.
    :param expected_output: Expected string representation of an empty MultiLangString.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, print_with_lang)
    mls = MultiLangString()
    assert str(mls) == expected_output, (
        f"Empty MultiLangString should return '{expected_output}' when "
        f"PRINT_WITH_LANG is {'enabled' if print_with_lang else 'disabled'}."
    )


def normalize_string(s: str) -> str:
    """Normalizes a string by sorting elements enclosed in braces `{}` if detected, and returns a comparable string."""
    import re

    def sort_braced_content(match):
        content = match.group(0).strip("{}")
        sorted_content = sorted(content.split(", "))
        return "{" + ", ".join(sorted_content) + "}"

    # This regex matches content within braces, including cases with nested braces.
    normalized = re.sub(r"\{[^{}]*\}", sort_braced_content, s)
    return normalized


@pytest.mark.parametrize(
    "texts, expected_with_lang, expected_without_lang",
    [
        ([("", "")], "{''}@", "{''}"),
        ([("Hello", "en")], "{'Hello'}@en", "{'Hello'}"),
        ([("Hola", "es"), ("Hello", "en")], "{'Hello'}@en, {'Hola'}@es", "{'Hello'}, {'Hola'}"),
        (
            [(" Привет", "ru"), (" Γειά", "gr")],
            "{' Γειά'}@gr, {' Привет'}@ru",
            "{' Γειά'}, {' Привет'}",
        ),  # Leading spaces in text, Cyrillic and Greek.
        (
            [("Hello ", "en"), ("Hola", "es ")],
            "{'Hello '}@en, {'Hola'}@es ",
            "{'Hello '}, {'Hola'}",
        ),  # Trailing spaces in text and language.
        (
            [("Καλημέρα", "GR"), ("Hello", "EN")],
            "{'Hello'}@EN, {'Καλημέρα'}@GR",
            "{'Hello'}, {'Καλημέρα'}",
        ),  # Mixed case languages.
        (
            [("Hello😊", "en"), ("😢", "emoji")],
            "{'😢'}@emoji, {'Hello😊'}@en",
            "{'😢'}, {'Hello😊'}",
        ),  # Emojis in text and as a language.
        (
            [("Hello\nWorld", "en"), ("Line\nBreak", "mult")],
            "{'Hello\nWorld'}@en, {'Line\nBreak'}@mult",
            "{'Hello\nWorld'}, {'Line\nBreak'}",
        ),  # Newline characters in text.
        (
            [("Speci@l Ch@racters", "en"), ("<XML>", "markup")],
            "{'Speci@l Ch@racters'}@en, {'<XML>'}@markup",
            "{'Speci@l Ch@racters'}, {'<XML>'}",
        ),  # Special characters.
        ([("Hello", "en"), ("hello", "en")], "{'Hello', 'hello'}@en", "{'Hello', 'hello'}"),
        (
            [("你好", "zh-Hant"), ("こんにちは", "ja")],
            "{'こんにちは'}@ja, {'你好'}@zh-Hant",
            "{'こんにちは'}, {'你好'}",
        ),
        ([("", "en")], "{''}@en", "{''}"),
        ([(" ", "en")], "{' '}@en", "{' '}"),
        ([("مرحبا", "ar"), ("שלום", "he")], "{'مرحبا'}@ar, {'שלום'}@he", "{'مرحبا'}, {'שלום'}"),
        ([("Line1\\nLine2", "en")], "{'Line1\\nLine2'}@en", "{'Line1\\nLine2'}"),
    ],
)
def test_multi_lang_string_str_various_texts(
    texts: list[tuple[str, str]], expected_with_lang: str, expected_without_lang: str
):
    mls = MultiLangString()
    for text, lang in texts:
        mls.add_entry(text, lang)

    # Test with language tags
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    assert normalize_string(str(mls)) == normalize_string(expected_with_lang), "Mismatch with language tags"

    # Test without language tags
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, False)
    assert normalize_string(str(mls)) == normalize_string(expected_without_lang), "Mismatch without language tags"


@pytest.mark.parametrize(
    "texts, expected_output",
    [
        ([("Hello", "en"), ("Hello", "en")], "{'Hello'}@en"),
        ([("Hello", "en"), ("Hello", "es")], "{'Hello'}@en, {'Hello'}@es"),
        ([("Hello" * 100, "en")], f"{{'{'Hello' * 100}'}}@en"),
    ],
)
def test_multi_lang_string_str_edge_and_unusual_cases(texts: list[tuple[str, str]], expected_output: str):
    """Test __str__ method for edge and unusual but valid cases.

    :param texts: List of text and language pairs to add to the MultiLangString.
    :param expected_output: Expected string representation.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    mls = MultiLangString()
    for text, lang in texts:
        mls.add_entry(text, lang)
    assert str(mls) == expected_output, "String representation does not match expected for edge or unusual cases."


def test_multi_lang_string_str_empty_set():
    """Test __str__ method for an empty set in MultiLangString with variations of the print_lang flag."""
    mls_empty_set = MultiLangString({"": set()})

    # Test with print_lang True
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    assert str(mls_empty_set) == "{}@", "Empty set with print_lang True should return '{}@'."

    # Test with print_lang False
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, False)
    assert str(mls_empty_set) == "{}", "Empty set with print_lang False should return '{}'."


def test_multi_lang_string_str_empty_string():
    """Test __str__ method for a set containing an empty string in MultiLangString with variations of the print_lang flag."""
    mls_empty_string = MultiLangString({"": {""}})

    # Test with print_lang True
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    assert (
        str(mls_empty_string) == "{''}@"
    ), "Set containing an empty string with print_lang True should return \"{''}@\"."

    # Test with print_lang False
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, False)
    assert (
        str(mls_empty_string) == "{''}"
    ), "Set containing an empty string with print_lang False should return \"{''}\"."
