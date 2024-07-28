import copy

import pytest
from langstring import LangString

methods_to_test = ["rstrip", "lstrip", "strip"]


class StringMethodSingleArgTestCase:
    def __init__(self, input_string, method_arg):
        self.input_string = input_string
        self.method_arg = method_arg

    def get_expected_output(self, method_name):
        method = getattr(self.input_string, method_name)
        return method(self.method_arg)

    def get_expected_default_output(self, method_name):
        method = getattr(self.input_string, method_name)
        return method()


# Test cases for methods with a single argument
test_cases = [
    # Testing with different types of whitespace
    StringMethodSingleArgTestCase("   hello   ", None),
    StringMethodSingleArgTestCase("\nhello\n", None),
    StringMethodSingleArgTestCase("\thello\t", None),
    StringMethodSingleArgTestCase("   ", None),  # Only whitespace
    StringMethodSingleArgTestCase("", None),  # Empty string
    # Testing with specific characters
    StringMethodSingleArgTestCase("xxhelloxx", "x"),
    StringMethodSingleArgTestCase("yyhello", "y"),
    StringMethodSingleArgTestCase("hellozz", "z"),
    StringMethodSingleArgTestCase("abcde", "a"),  # Character only at the start
    StringMethodSingleArgTestCase("edcba", "a"),  # Character only at the end
    StringMethodSingleArgTestCase("abcba", "a"),  # Character at both ends
    # Testing with multiple characters to strip
    StringMethodSingleArgTestCase("abchelloabc", "abc"),
    StringMethodSingleArgTestCase("xyzhelloxyz", "xyz"),
    # Testing with no matching characters to strip
    StringMethodSingleArgTestCase("hello", "x"),
    StringMethodSingleArgTestCase("world", "abc"),
    # Testing with special characters
    StringMethodSingleArgTestCase("!hello!", "!"),
    StringMethodSingleArgTestCase("#$hello$#", "#$"),
    # Testing with unicode characters
    StringMethodSingleArgTestCase("😊hello😊", "😊"),
    StringMethodSingleArgTestCase("こんにちはhelloこんにちは", "こんにちは"),
    # Edge cases
    StringMethodSingleArgTestCase("a" * 10000, "a"),  # Very long string
    StringMethodSingleArgTestCase("🌍🌎🌏" * 1000, "🌍"),  # Repeated complex unicode
    StringMethodSingleArgTestCase("hello😊world😊hello", "😊world"),  # Mixed unicode and regular characters
]


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in test_cases for m in methods_to_test])
def test_string_methods_single_arg(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_output = test_case.get_expected_output(method)
    result = getattr(lang_string, method)(test_case.method_arg)
    assert result.text == expected_output, f"{method}({test_case.method_arg}) failed for '{test_case.input_string}'"
    assert lang_string_before == lang_string, "The original LangString cannot be modified by the called method."


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in test_cases for m in methods_to_test])
def test_string_methods_default_arg(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_output = test_case.get_expected_default_output(method)
    result = getattr(lang_string, method)()
    assert result.text == expected_output, f"{method} (default arg) failed for '{test_case.input_string}'"
    assert lang_string_before == lang_string, "The original LangString cannot be modified by the called method."


# Test cases for invalid argument types
invalid_arg_test_cases = [
    123,  # Integer
    12.34,  # Float
    [],  # List
    {},  # Dictionary
    True,  # Boolean
]


@pytest.mark.parametrize("invalid_arg", invalid_arg_test_cases)
@pytest.mark.parametrize("method", methods_to_test)
def test_string_methods_single_invalid_arg(invalid_arg, method):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError, match=".* must be None or str"):
        getattr(lang_string, method)(invalid_arg)
