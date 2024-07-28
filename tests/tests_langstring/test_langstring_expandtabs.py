import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "input_string, tabsize, expected_output",
    [
        ("hello\tworld", 0, "helloworld"),
        ("hello\tworld", 8, "hello   world"),
        ("hello\tworld", 4, "hello   world"),
        ("hello\t\tworld", 0, "helloworld"),
        ("hello\t\tworld", 4, "hello       world"),
        ("hello\n\tworld", 8, "hello\n        world"),
        ("", 8, ""),
        ("\t", 4, "    "),
        ("helloworld", 8, "helloworld"),
        ("hello_world", 8, "hello_world"),
        ("hello world", 8, "hello world"),
        ("hello\tworld", -1, "helloworld"),
        ("hello\tworld", -100, "helloworld"),
    ],
)
def test_expandtabs_basic(input_string: str, tabsize: int, expected_output: str):
    """
    Test the basic functionality of expandtabs method.

    :param input_string: The input string containing tab characters.
    :param tabsize: The size of the tab stops.
    :param expected_output: The expected output after expanding tabs.
    """
    lang_string = LangString(input_string, "en")
    result = lang_string.expandtabs(tabsize)
    assert result.text == expected_output, f"expandtabs({tabsize}) failed for '{input_string}'"


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("hello\tworld", "hello   world"),
        ("hello\t\tworld", "hello           world"),
        ("hello\n\tworld", "hello\n        world"),
        ("", ""),
        ("\t", "        "),
        ("helloworld", "helloworld"),
        ("hello-world", "hello-world"),
        ("hello world", "hello world"),
    ],
)
def test_expandtabs_default(input_string: str, expected_output: str):
    """
    Test the basic functionality of expandtabs method.

    :param input_string: The input string containing tab characters.
    :param tabsize: The size of the tab stops.
    :param expected_output: The expected output after expanding tabs.
    """
    lang_string = LangString(input_string, "en")
    result = lang_string.expandtabs()
    assert result.text == expected_output, f"expandtabs(default) failed for '{input_string}'"


@pytest.mark.parametrize(
    "input_string, invalid_tabsize",
    [
        ("hello\tworld", "four"),
        ("hello\tworld", None),
        ("hello\tworld", 3.5),
        ("hello\tworld", []),
        ("hello\tworld", {}),
    ],
)
def test_expandtabs_invalid_tabsize_type(input_string: str, invalid_tabsize):
    """
    Test expandtabs with invalid tabsize types.

    :param input_string: The input string to test.
    :param invalid_tabsize: Invalid tabsize value to test.
    :raises TypeError: If tabsize is not an integer.
    """
    lang_string = LangString(input_string, "en")
    with pytest.raises(TypeError, match=".+ object cannot be interpreted as an integer"):
        lang_string.expandtabs(invalid_tabsize)


@pytest.mark.parametrize(
    "input_string, tabsize, lang",
    [
        ("hello\tworld", 8, "en"),
        ("hola\tmundo", 4, "es"),
        ("bonjour\tmonde", 8, "fr"),
    ],
)
def test_expandtabs_preserve_lang(input_string: str, tabsize: int, lang: str):
    """
    Test expandtabs while preserving the language tag.

    :param input_string: The input string to test.
    :param tabsize: The size of the tab stops.
    :param lang: The language tag of the input string.
    """
    lang_string = LangString(input_string, lang)
    result = lang_string.expandtabs(tabsize)
    assert result.lang == lang, f"Language tag changed after expandtabs({tabsize}) for '{input_string}'"


@pytest.mark.parametrize(
    "input_string, tabsize, expected_output",
    [
        ("\t\t\t", 8, "                        "),  # Only tabs
        ("\n\t\n\t", 8, "\n        \n        "),  # Newlines with tabs
        ("hello\tworld", 1, "hello world"),  # Small tab size
        ("hello\tworld", 100, "hello" + " " * 95 + "world"),  # Large tab size
        ("hello\tworld", -1, "helloworld"),  # Negative tab size
    ],
)
def test_expandtabs_edge_cases(input_string: str, tabsize: int, expected_output: str):
    """
    Test expandtabs with edge cases and unusual but valid usage.

    :param input_string: The input string to test.
    :param tabsize: The size of the tab stops.
    :param expected_output: The expected output after expanding tabs.
    """
    lang_string = LangString(input_string, "en")
    result = lang_string.expandtabs(tabsize)
    assert result.text == expected_output, f"expandtabs({tabsize}) failed for '{input_string}'"
