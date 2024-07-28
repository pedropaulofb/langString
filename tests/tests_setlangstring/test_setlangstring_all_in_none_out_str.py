import re

import pytest
from langstring import Controller
from langstring import SetLangString
from langstring import SetLangStringFlag


class SetLangStringOperationTestCase:
    def __init__(self, texts, lang):
        self.texts = texts
        self.lang = lang

    def run_test(self, method_name):
        set_lang_string = SetLangString(texts=self.texts, lang=self.lang)
        method = getattr(set_lang_string, method_name)
        if method_name == "pop" and not self.texts:
            with pytest.raises(KeyError, match="pop from an empty set"):
                return method()
            return "KeyError"
        else:
            return method()


# Define test cases
operation_test_cases = [
    SetLangStringOperationTestCase({"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"x", "y", "z"}, "en"),
    SetLangStringOperationTestCase({"1", "2", "3"}, "en"),
    SetLangStringOperationTestCase({"apple", "banana", "cherry"}, "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en"),
    SetLangStringOperationTestCase({"😊", "😂", "😜"}, "en"),
    SetLangStringOperationTestCase({"🍏", "🍎"}, "en"),
    SetLangStringOperationTestCase({"HELLO", "WORLD"}, "en"),
    SetLangStringOperationTestCase({" ", "  "}, "en"),
    SetLangStringOperationTestCase(set(), "en"),  # Empty set
    # Basic cases with different sizes
    SetLangStringOperationTestCase({"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"x", "y"}, "en"),
    SetLangStringOperationTestCase({"1"}, "en"),
    SetLangStringOperationTestCase(set(), "en"),  # Empty set
    # Cases with mixed character types
    SetLangStringOperationTestCase({"1", "a", "@"}, "en"),
    SetLangStringOperationTestCase({"#", "$", "%", "&"}, "en"),
    # Cases with special characters and emojis
    SetLangStringOperationTestCase({"😊", "😂", "😜"}, "en"),
    SetLangStringOperationTestCase({"🍏", "🍎", "🍐"}, "en"),
    SetLangStringOperationTestCase({"!", "@", "#"}, "en"),
    # Cases with numeric strings
    SetLangStringOperationTestCase({"123", "456", "789"}, "en"),
    SetLangStringOperationTestCase({"100", "200", "300"}, "en"),
    # Cases with spaces and empty strings
    SetLangStringOperationTestCase({" ", "  ", "   "}, "en"),
    SetLangStringOperationTestCase({"", " ", "  "}, "en"),
    # Cases with mixed alphabets
    SetLangStringOperationTestCase({"apple", "banana", "cherry"}, "en"),
    SetLangStringOperationTestCase({"cat", "dog", "bird"}, "en"),
    # Cases with upper and lower case
    SetLangStringOperationTestCase({"Hello", "World"}, "en"),
    SetLangStringOperationTestCase({"APPLE", "BANANA", "CHERRY"}, "en"),
    # Cases with non-English alphabets
    SetLangStringOperationTestCase({"привет", "мир"}, "ru"),
    SetLangStringOperationTestCase({"こんにちは", "世界"}, "jp"),
    # Complex mixed content cases
    SetLangStringOperationTestCase({"hello", "world", "😊"}, "en"),
    SetLangStringOperationTestCase({"123", "abc", "😜"}, "en"),
    SetLangStringOperationTestCase({"Hello", "123", "🍏"}, "en"),
    SetLangStringOperationTestCase({"hello", "привет", "こんにちは"}, "en"),
    SetLangStringOperationTestCase(
        {"This is a very long string to test the handling of large elements within the SetLangString class"}, "en"
    ),
    SetLangStringOperationTestCase({"string", "String", "strIng"}, "en"),
    SetLangStringOperationTestCase({"√", "π", "Ω"}, "en"),
    SetLangStringOperationTestCase({"Line1\nLine2", "Tab\tSeparated"}, "en"),
]


@pytest.mark.parametrize("test_case", operation_test_cases)
@pytest.mark.parametrize("method_name", ["pop", "__repr__", "__str__"])
def test_setlangstring_operation_methods(test_case, method_name):
    result = test_case.run_test(method_name)
    if method_name == "pop":
        if test_case.texts:
            assert result in test_case.texts, f"Failed {method_name} for texts={test_case.texts}"
        else:
            assert result == "KeyError", "Expected KeyError for popping from an empty set"
    else:
        assert isinstance(result, str), f"Failed {method_name} for texts={test_case.texts}"


str_test_cases = [
    {"texts": set(), "lang": "en", "expected_without_lang": "{}", "expected_with_lang": "{}@en"},
    {
        "texts": {"a", "b", "c"},
        "lang": "en",
        "expected_without_lang": "{'a', 'b', 'c'}",
        "expected_with_lang": "{'a', 'b', 'c'}@en",
    },
    {"texts": {" "}, "lang": "en", "expected_without_lang": "{' '}", "expected_with_lang": "{' '}@en"},
    # Cyrillic
    {
        "texts": {"привет", "мир"},
        "lang": "ru",
        "expected_without_lang": "{'привет', 'мир'}",
        "expected_with_lang": "{'привет', 'мир'}@ru",
    },
    # Greek
    {
        "texts": {"γειά", "σου"},
        "lang": "el",
        "expected_without_lang": "{'γειά', 'σου'}",
        "expected_with_lang": "{'γειά', 'σου'}@el",
    },
    # Emojis
    {
        "texts": {"😊", "😂", "👍"},
        "lang": "en",
        "expected_without_lang": "{'😊', '😂', '👍'}",
        "expected_with_lang": "{'😊', '😂', '👍'}@en",
    },
    # Upper case
    {
        "texts": {"HELLO", "WORLD"},
        "lang": "en",
        "expected_without_lang": "{'HELLO', 'WORLD'}",
        "expected_with_lang": "{'HELLO', 'WORLD'}@en",
    },
    # Mixed case
    {
        "texts": {"Python", "pYTHON"},
        "lang": "en",
        "expected_without_lang": "{'Python', 'pYTHON'}",
        "expected_with_lang": "{'Python', 'pYTHON'}@en",
    },
    # Spaces before and after
    {
        "texts": {" hello ", " world "},
        "lang": "en",
        "expected_without_lang": "{' hello ', ' world '}",
        "expected_with_lang": "{' hello ', ' world '}@en",
    },
    # Mixed content
    {
        "texts": {"123", "abc", "😜", "Привет"},
        "lang": "en",
        "expected_without_lang": "{'123', 'abc', '😜', 'Привет'}",
        "expected_with_lang": "{'123', 'abc', '😜', 'Привет'}@en",
    },
    # Single character
    {
        "texts": {"a"},
        "lang": "en",
        "expected_without_lang": "{'a'}",
        "expected_with_lang": "{'a'}@en",
    },
    # Numerics and symbols
    {
        "texts": {"1", "2", "$", "%"},
        "lang": "en",
        "expected_without_lang": "{'1', '2', '$', '%'}",
        "expected_with_lang": "{'1', '2', '$', '%'}@en",
    },
    # Empty string in a set
    {
        "texts": {""},
        "lang": "en",
        "expected_without_lang": "{''}",  # Adjust based on actual handling of empty strings
        "expected_with_lang": "{''}@en",  # Adjust based on actual handling of empty strings
    },
    # Mixed empty and non-empty strings
    {
        "texts": {"", "non-empty"},
        "lang": "en",
        "expected_without_lang": "{'', 'non-empty'}",
        "expected_with_lang": "{'', 'non-empty'}@en",
    },
    # Empty set
    {
        "texts": set(),
        "lang": "en",
        "expected_without_lang": "{}",
        "expected_with_lang": "{}@en",
    },
    # Set with only spaces (considering valid as it's not auto-trimmed)
    {
        "texts": {" ", "  "},
        "lang": "en",
        "expected_without_lang": "{' ', '  '}",
        "expected_with_lang": "{' ', '  '}@en",
    },
    # Set with mixed empty strings and spaces
    {
        "texts": {"", " ", "  "},
        "lang": "en",
        "expected_without_lang": "{'', ' ', '  '}",
        "expected_with_lang": "{'', ' ', '  '}@en",
    },
    # Set with newline characters
    {
        "texts": {"\n", "\n\n"},
        "lang": "en",
        "expected_without_lang": "{'\\n', '\\n\\n'}",
        "expected_with_lang": "{'\\n', '\\n\\n'}@en",
    },
    # Set with tab characters
    {
        "texts": {"\t", "\t\t"},
        "lang": "en",
        "expected_without_lang": "{'\\t', '\\t\\t'}",
        "expected_with_lang": "{'\\t', '\\t\\t'}@en",
    },
    # Multiple empty strings (effectively a single empty string due to set behavior)
    {
        "texts": {"", "", ""},
        "lang": "en",
        "expected_without_lang": "{''}",  # As sets deduplicate, only one empty string is valid
        "expected_with_lang": "{''}@en",  # Adjust based on actual handling
    },
]


def escape_special_characters(text: str) -> str:
    return text.replace("\n", "\\n").replace("\t", "\\t")


@pytest.mark.parametrize("case", str_test_cases)
def test_setlangstring_str_method(case):
    set_lang_string = SetLangString(texts=case["texts"], lang=case["lang"])

    # Disable PRINT_WITH_LANG for the first part of the test
    Controller.set_flag(SetLangStringFlag.PRINT_WITH_LANG, False)
    result_without_lang = str(set_lang_string)

    # Escaping special characters in the expected result for comparison
    escaped_expected_without_lang = escape_special_characters(case["expected_without_lang"])

    # Directly compare sets to ensure elements match, regardless of order
    expected_set = set(escaped_expected_without_lang.strip("{}").split(", "))
    result_set = set(escape_special_characters(result_without_lang).strip("{}").split(", "))

    assert result_set == expected_set, f"Mismatch in set elements without language tag: {result_set} != {expected_set}"

    # Enable PRINT_WITH_LANG for the second part of the test
    Controller.set_flag(SetLangStringFlag.PRINT_WITH_LANG, True)
    result_with_lang = str(set_lang_string)

    # Escaping special characters in the expected result for comparison
    escaped_expected_with_lang = escape_special_characters(case["expected_with_lang"])

    # Extract set and language tag portions from the result
    match = re.match(r"^(.*)@(\w+)$", result_with_lang, re.DOTALL)
    if not match:
        assert False, f"Result does not match expected format: {result_with_lang}"

    result_texts, result_lang = match.groups()
    expected_texts, expected_lang = re.match(r"^(.*)@(\w+)$", escaped_expected_with_lang).groups()

    result_set_with_lang = set(escape_special_characters(result_texts).strip("{}").split(", "))
    expected_set_with_lang = set(expected_texts.strip("{}").split(", "))

    assert (
        result_set_with_lang == expected_set_with_lang
    ), f"Mismatch in set elements with language tag: {result_set_with_lang} != {expected_set_with_lang}"
    assert result_lang == expected_lang, f"Mismatch in language tag: {result_lang} != {expected_lang}"


def escape_special_characters(text: str) -> str:
    return text.replace("\n", "\\n").replace("\t", "\\t")


def parse_set_string(set_string: str) -> set:
    """Helper function to parse set string into a Python set."""
    return set(escape_special_characters(set_string.strip("{}")).split(", "))


@pytest.mark.parametrize(
    "texts, lang, expected_without_quotes, expected_with_lang",
    [
        ({"a", "b", "c"}, "en", "{a, b, c}", "{a, b, c}@en"),
        ({" "}, "en", "{ }", "{ }@en"),
        ({"😊", "😂", "👍"}, "en", "{😊, 😂, 👍}", "{😊, 😂, 👍}@en"),
        ({"привет", "мир"}, "ru", "{привет, мир}", "{привет, мир}@ru"),
        ({"HELLO", "WORLD"}, "en", "{HELLO, WORLD}", "{HELLO, WORLD}@en"),
        (set(), "en", "{}", "{}@en"),
        ({"", " "}, "en", "{,  }", "{,  }@en"),
        ({"\n", "\t"}, "en", "{\\n, \\t}", "{\\n, \\t}@en"),
        ({"123", "abc", "😜", "Привет"}, "en", "{123, abc, 😜, Привет}", "{123, abc, 😜, Привет}@en"),
    ],
)
def test_setlangstring_str_various_cases(texts, lang, expected_without_quotes, expected_with_lang):
    # Ensure the PRINT_WITH_QUOTES flag is set to False
    Controller.set_flag(SetLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(SetLangStringFlag.PRINT_WITH_LANG, False)

    set_lang_string = SetLangString(texts=texts, lang=lang)
    result_without_quotes = str(set_lang_string)
    assert parse_set_string(result_without_quotes) == parse_set_string(
        expected_without_quotes
    ), f"Expected: {expected_without_quotes}, but got: {result_without_quotes}"

    # Enable PRINT_WITH_LANG and check
    Controller.set_flag(SetLangStringFlag.PRINT_WITH_LANG, True)
    result_with_lang = str(set_lang_string)
    result_texts, result_lang = result_with_lang.rsplit("@", 1) if "@" in result_with_lang else (result_with_lang, "")
    expected_texts, expected_lang = (
        expected_with_lang.rsplit("@", 1) if "@" in expected_with_lang else (expected_with_lang, "")
    )

    assert parse_set_string(result_texts) == parse_set_string(
        expected_texts
    ), f"Expected: {expected_with_lang}, but got: {result_with_lang}"
    assert result_lang == expected_lang, f"Expected language: {expected_lang}, but got: {result_lang}"

    # Reset the flags to avoid side effects on other tests
    Controller.reset_flag(SetLangStringFlag.PRINT_WITH_QUOTES)
    Controller.reset_flag(SetLangStringFlag.PRINT_WITH_LANG)
