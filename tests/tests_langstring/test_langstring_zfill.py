import pytest
from langstring import LangString


class ZFillTestCase:
    def __init__(self, input_string, width):
        self.input_string = input_string
        self.width = width
        self.expected_output = input_string.zfill(width)


zfill_test_cases = [
    ZFillTestCase("123", 5),
    ZFillTestCase("hello", 10),
    ZFillTestCase("world", 3),  # Width less than string length
    ZFillTestCase("", 5),  # Empty string
    ZFillTestCase("こんにちは", 10),  # Unicode characters
    ZFillTestCase("😊😊😊", 5),  # Emojis
    ZFillTestCase("123", 0),  # Zero width
    ZFillTestCase("-123", 5),  # Negative number
    ZFillTestCase("123", -5),  # Negative width
    ZFillTestCase("123", True),
    ZFillTestCase("-123", True),
    ZFillTestCase("hello", True),
    ZFillTestCase("123", False),
    ZFillTestCase("-123", False),
    ZFillTestCase("hello", False),
    ZFillTestCase("+123", 6),  # String with leading plus sign
    ZFillTestCase("-123", 6),  # String with leading minus sign
    ZFillTestCase("000123", 6),  # String already filled with zeros
    ZFillTestCase("123", 3),  # Width equal to string length
    ZFillTestCase("123", 100),  # Very large width
]


@pytest.mark.parametrize("test_case", zfill_test_cases)
def test_zfill(test_case: ZFillTestCase) -> None:
    """
    Test the zfill method of LangString.
    """
    lang_string = LangString(test_case.input_string, "en")
    result = lang_string.zfill(test_case.width)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    assert result.text == test_case.expected_output, f"zfill({test_case.width}) failed for '{test_case.input_string}'"
    assert result.lang == "en", "Language tag should remain unchanged"


# Test cases for invalid argument types
invalid_width_test_cases = [
    "string",  # String
    1.5,  # Float
    [],  # List
    {},  # Dictionary
    None,  # NoneType
]


@pytest.mark.parametrize("invalid_width", invalid_width_test_cases)
def test_zfill_invalid_width(invalid_width):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError):
        lang_string.zfill(invalid_width)
