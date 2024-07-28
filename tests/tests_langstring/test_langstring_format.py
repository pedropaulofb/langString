import pytest
from langstring import LangString


class FormatTestCase:
    def __init__(self, input_string: str, args: tuple, kwargs: dict, lang: str):
        self.input_string = input_string
        self.args = args
        self.kwargs = kwargs
        self.lang = lang
        self.expected_output = input_string.format(*args, **kwargs)


format_test_cases = [
    FormatTestCase("Hello, {}", ("world",), {}, "en"),
    FormatTestCase("Value: {value}", (), {"value": 42}, "en"),
    FormatTestCase("{0} {1}", ("Hello", "world"), {}, "en"),
    FormatTestCase("Template string", ("hello", 123), {}, "en"),  # Non-string format argument
    FormatTestCase("Template string", (), {"value": [1, 2, 3]}, "en"),  # Non-primitive type in keyword argument
    FormatTestCase("Template string", ("hello",), {"value": {"key": "value"}}, "en"),  # Dictionary in keyword argument
    FormatTestCase("Template string", ("hello", complex(1, 2)), {}, "en"),  # Complex number as argument
    FormatTestCase("Template string", (), {"value": slice(0, 5)}, "en"),  # Slice object in keyword argument
    FormatTestCase("Template string", ("hello", {"not": "allowed"}), {}, "en"),  # Dictionary as argument
    FormatTestCase("Template string", ("hello",), {"value": lambda x: x}, "en"),  # Function in keyword argument
]


@pytest.mark.parametrize("test_case", format_test_cases)
def test_format(test_case: FormatTestCase):
    lang_string = LangString(test_case.input_string, test_case.lang)
    result = lang_string.format(*test_case.args, **test_case.kwargs)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    assert result.text == test_case.expected_output, "Format method failed"
    assert result.lang == test_case.lang, "Language tag should remain unchanged"
