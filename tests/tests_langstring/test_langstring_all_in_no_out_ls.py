import copy

import pytest
from langstring import LangString

methods_to_test = ["capitalize", "casefold", "lower", "title", "swapcase", "upper"]


class StringMethodTestCase:
    def __init__(self, input_string):
        self.input_string = input_string
        self.expected_results = self._generate_expected_results()

    def _generate_expected_results(self):
        return {
            "capitalize": self.input_string.capitalize(),
            "casefold": self.input_string.casefold(),
            "lower": self.input_string.lower(),
            "title": self.input_string.title(),
            "swapcase": self.input_string.swapcase(),
            "upper": self.input_string.upper(),
        }


# Valid test cases
valid_test_cases = [
    StringMethodTestCase("hello world"),
    StringMethodTestCase("HELLO WORLD"),
    StringMethodTestCase("Python Programming"),
    StringMethodTestCase("123abc"),
    StringMethodTestCase(""),
    StringMethodTestCase("こんにちは"),
    StringMethodTestCase("HELLO world 123"),
    StringMethodTestCase("12345!@#$%"),
    StringMethodTestCase("Mixed CASE text"),
    StringMethodTestCase("1234"),
    StringMethodTestCase("!@#$%^&*()"),
    StringMethodTestCase("Text with spaces"),
    StringMethodTestCase(" Text with leading space"),
    StringMethodTestCase("     Text with leading spaces"),
    StringMethodTestCase("Text with trailing space "),
    StringMethodTestCase("Text with trailing spaces     "),
    StringMethodTestCase("Text   with  multiple spaces"),
    StringMethodTestCase("Text_with_underscores"),
    StringMethodTestCase("1234text"),
    StringMethodTestCase("text1234"),
    StringMethodTestCase("1234_text"),
    StringMethodTestCase("text_1234"),
    StringMethodTestCase("text\nnew line"),
    StringMethodTestCase("text\ttab"),
    StringMethodTestCase("text\rreturn"),
    StringMethodTestCase("text\fformfeed"),
    StringMethodTestCase("text\vvertical tab"),
    StringMethodTestCase("text with\nmultiple\nlines"),
    StringMethodTestCase("text with\tmultiple\ttabs"),
    StringMethodTestCase("SingleWord"),
    StringMethodTestCase("a"),
    StringMethodTestCase("A"),
    StringMethodTestCase("1"),
    StringMethodTestCase("😊😊😊"),
    StringMethodTestCase("中文字符"),
    StringMethodTestCase("русский текст"),
    StringMethodTestCase("texto en español"),
    StringMethodTestCase("texte en français"),
    StringMethodTestCase("النص بالعربية"),
    StringMethodTestCase("हिंदी में पाठ"),
    StringMethodTestCase("1234😊"),
    StringMethodTestCase("😊1234"),
    StringMethodTestCase("1234😊abc"),
    StringMethodTestCase("abc😊1234"),
    StringMethodTestCase("1234😊abc😊"),
    StringMethodTestCase("abc😊1234😊"),
    StringMethodTestCase("1234😊abc😊1234"),
    StringMethodTestCase("abc😊1234😊abc"),
]


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in valid_test_cases for m in methods_to_test])
def test_string_methods_valid(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_result = LangString(test_case.expected_results[method], "en")
    actual_result = getattr(lang_string, method)()  # Convert LangString object to string
    assert actual_result == expected_result, f"Failed for method '{method}' with input '{test_case.input_string}'"
    assert lang_string_before == lang_string, "The original LangString cannot be modified by the called method."


# Invalid arguments to test with
invalid_args = ["str", "", 123, 12.34, [], {}, None, True, False]


@pytest.mark.parametrize("method, invalid_arg", [(m, ia) for m in methods_to_test for ia in invalid_args])
def test_string_methods_invalid(method, invalid_arg):
    with pytest.raises(TypeError, match="takes 1 positional argument but 2 were given"):
        getattr(LangString("hello world", "en"), method)(invalid_arg)  # Pass invalid argument
