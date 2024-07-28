import copy

import pytest
from langstring import LangString

methods_to_test = [
    "isalnum",
    "isalpha",
    "isascii",
    "isdecimal",
    "isdigit",
    "isidentifier",
    "islower",
    "isnumeric",
    "isprintable",
    "isspace",
    "istitle",
    "isupper",
]


class StringTestCase:
    def __init__(self, string):
        self.string = string
        self.expected_results = self._generate_expected_results()

    def _generate_expected_results(self):
        results = {
            "isalnum": self.string.isalnum(),
            "isalpha": self.string.isalpha(),
            "isascii": self.string.isascii(),
            "isdecimal": self.string.isdecimal(),
            "isdigit": self.string.isdigit(),
            "isidentifier": self.string.isidentifier(),
            "islower": self.string.islower(),
            "isnumeric": self.string.isnumeric(),
            "isprintable": self.string.isprintable(),
            "isspace": self.string.isspace(),
            "istitle": self.string.istitle(),
            "isupper": self.string.isupper(),
        }
        return results


test_cases = [
    StringTestCase("Hello123"),
    StringTestCase("Hello 123"),
    StringTestCase("123"),
    StringTestCase("こんにちは"),
    StringTestCase(""),
    StringTestCase("123abc"),
    StringTestCase("123.45"),
    StringTestCase("   "),
    StringTestCase("HelloWorld"),
    StringTestCase("HELLO"),
    StringTestCase("hello"),
    StringTestCase(" hello"),
    StringTestCase("hello "),
    StringTestCase("Hello World"),
    StringTestCase("1234567890"),
    StringTestCase("こんにちは123"),
    StringTestCase("😊😊😊"),
    StringTestCase("123\n"),
    StringTestCase("Title Case"),
    StringTestCase("123ABC"),
    StringTestCase("abc_def"),
    StringTestCase("1234567890abcdefABCDEF"),
    StringTestCase("Γειά σου Κόσμε"),
    StringTestCase("1234_5678"),
    StringTestCase("1234567890\n"),
    StringTestCase("1234567890\t"),
    StringTestCase("1234567890\r"),
    StringTestCase("1234567890\f"),
    StringTestCase("1234567890\v"),
    StringTestCase("1234567890 "),
    StringTestCase(" 1234567890"),
    StringTestCase("1234567890a"),
    StringTestCase("a1234567890"),
    StringTestCase("1234567890a "),
    StringTestCase(" 1234567890a"),
    StringTestCase("1234567890a\n"),
    StringTestCase("1234567890a\t"),
    StringTestCase("1234567890a\r"),
    StringTestCase("1234567890a\f"),
    StringTestCase("1234567890a\v"),
    StringTestCase("1234567890a "),
    StringTestCase("HelloWorld123"),
    StringTestCase("AbCdEfG123"),
    StringTestCase("hello@world.com"),
    StringTestCase("pass!word123"),
    StringTestCase("123#abc!"),
    StringTestCase("Привет"),
    StringTestCase("مرحبا"),
    StringTestCase("नमस्ते"),
    StringTestCase("中文测试"),
    StringTestCase("\nNewLine"),
    StringTestCase("\tTabbed"),
    StringTestCase("FirstLine\\nSecondLine"),
    StringTestCase("a"),
    StringTestCase("Z"),
    StringTestCase("1"),
    StringTestCase("9"),
    StringTestCase("@"),
    StringTestCase("#"),
    StringTestCase("     "),
    StringTestCase(" 1234 "),
    StringTestCase("Line1\nLine2"),
    StringTestCase("Column1\tColumn2"),
    StringTestCase("👍👎"),
    StringTestCase("a̐éö̲"),
    StringTestCase("12345!@#$%"),
]


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in test_cases for m in methods_to_test])
def test_string_methods(test_case, method):
    lang_string = LangString(test_case.string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_result = getattr(test_case.string, method)()
    actual_result = getattr(lang_string, method)()
    assert actual_result == expected_result, f"Failed for method '{method}' with input '{test_case.string}'"
    assert lang_string_before == lang_string, "The original LangString cannot be modified by the called method."


# Invalid arguments to test with
invalid_args = [123, 12.34, [], {}, None, True, False]


@pytest.mark.parametrize("method, invalid_arg", [(m, ia) for m in methods_to_test for ia in invalid_args])
def test_methods_invalid(method, invalid_arg):
    with pytest.raises(TypeError, match="takes 1 positional argument but 2 were given"):
        getattr(LangString("hello world", "en"), method)(invalid_arg)  # Pass invalid argument
