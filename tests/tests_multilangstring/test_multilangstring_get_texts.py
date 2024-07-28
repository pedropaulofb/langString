import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "input_dict, expected_result",
    [
        ({"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}}, ["Bonjour", "Hello", "Monde", "World"]),
        ({"en": {"", " "}, "fr": {" ", ""}}, ["", "", " ", " "]),
        ({"en": {"Hello"}, "es": {"Hola", "Mundo"}, "ru": {"Привет"}}, ["Hello", "Hola", "Mundo", "Привет"]),
        ({"jp": {"こんにちは", "世界"}, "kr": {"안녕하세요", "세계"}}, ["こんにちは", "世界", "세계", "안녕하세요"]),
        ({"emoji": {"😊", "😂", "👍"}, "symbols": {"@", "#"}}, ["#", "@", "👍", "😂", "😊"]),
        (
            {"mixed": {"text with spaces", " textwithleadingandtrailing ", "123"}},
            [" textwithleadingandtrailing ", "123", "text with spaces"],
        ),
        ({}, []),
        (
            {"upper": {"THIS", "IS", "UPPERCASE"}, "lower": {"this", "is", "lowercase"}},
            ["IS", "THIS", "UPPERCASE", "is", "lowercase", "this"],
        ),
        (
            {"spaces": {" leading", "trailing ", " inside spaces "}, "empty": {"", "  "}},
            ["", "  ", " inside spaces ", " leading", "trailing "],
        ),
        ({"numbers": {"1", "2", "3"}, "special": {"!", "@", "#"}}, ["!", "#", "1", "2", "3", "@"]),
        ({"non-ascii": {"æøå", "éèê"}, "cyrillic": {"д", "ж", "ё"}}, ["æøå", "éèê", "д", "ж", "ё"]),
        ({"mixed": {"Text1", "TEXT2", "text3", "123"}}, ["123", "TEXT2", "Text1", "text3"]),
    ],
)
def test_get_texts_varied_inputs(input_dict: dict, expected_result: list[str]) -> None:
    """Test get_texts method with a variety of input scenarios including different languages, characters, and symbols.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and sets of texts.
    :param expected_result: Expected sorted list of texts returned by get_texts.
    :return: None
    """
    mls = MultiLangString(input_dict)
    assert mls.get_texts() == expected_result, f"Expected sorted texts {expected_result}, but got {mls.get_texts()}"


@pytest.mark.parametrize(
    "input_dict, expected_result",
    [
        ({"en": set()}, []),
        ({"en": {" "}, "fr": {"   "}}, [" ", "   "]),
        ({"en": {"Hello\nWorld"}, "fr": {"Bonjour\nMonde"}}, ["Bonjour\nMonde", "Hello\nWorld"]),
    ],
)
def test_get_texts_with_special_cases(input_dict: dict, expected_result: list[str]) -> None:
    """Test get_texts with special cases including empty sets, spaces, and newlines.

    :param input_dict: A dictionary to initialize MultiLangString with language keys and text sets including special cases.
    :param expected_result: Expected sorted list of texts returned by get_texts, including handling of special characters.
    """
    mls = MultiLangString(input_dict)
    assert mls.get_texts() == expected_result, "get_texts should correctly handle special characters and empty sets"
