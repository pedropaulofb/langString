import pytest
from langstring import LangString


class TranslateTestCase:
    def __init__(self, input_string: str, table: dict[int, str], lang: str):
        self.input_string = input_string
        self.table = table
        self.lang = lang
        self.expected_output = input_string.translate(table)


# Example translation tables
table1 = str.maketrans({"h": "H", "e": "3", "l": "1", "o": "0"})
table2 = str.maketrans({"😊": "🙂", "🌍": "🌎"})
table3 = str.maketrans("", "", "aeiou")  # Removing vowels

translate_test_cases = [
    TranslateTestCase("hello", table1, "en"),
    TranslateTestCase("😊🌍", table2, "en"),
    TranslateTestCase("hello world", table3, "en"),
    TranslateTestCase("こんにちは", str.maketrans({"に": "ニ", "ち": "チ"}), "ja"),
    TranslateTestCase("", table1, "en"),  # Empty string
    TranslateTestCase("no change", {}, "en"),  # Empty translation table
    # Additional valid cases...
    TranslateTestCase("12345", str.maketrans({"1": "one", "2": "two"}), "en"),
    TranslateTestCase("spaces", str.maketrans({" ": "-"}), "en"),
    TranslateTestCase("UPPER", str.maketrans({"U": "u", "P": "p"}), "en"),
    # Edge cases
    TranslateTestCase("a" * 10000, str.maketrans({"a": "A"}), "en"),  # Very long string
    # Unusual but valid cases
    TranslateTestCase("    ", str.maketrans({" ": "*"}), "en"),  # Strings with only whitespace
    TranslateTestCase("123", str.maketrans({"1": "one", "2": None}), "en"),  # Removing and replacing characters
    TranslateTestCase("hello", table1, "en"),
    TranslateTestCase("😊🌍", table2, "en"),
    TranslateTestCase("hello world", table3, "en"),
    TranslateTestCase("こんにちは", str.maketrans({"に": "ニ", "ち": "チ"}), "ja"),
    TranslateTestCase("", table1, "en"),  # Empty string
    TranslateTestCase("no change", {}, "en"),  # Empty translation table
    # Additional valid cases based on errors...
    TranslateTestCase("hello", {"a": 123}, "en"),  # Non-string replacement
    TranslateTestCase("hello", "string", "en"),  # String instead of dict
    TranslateTestCase("hello", [1, 2, 3], "en"),  # List instead of dict
    # More valid cases...
    TranslateTestCase("12345", str.maketrans({"1": "one", "2": "two"}), "en"),
    TranslateTestCase("spaces", str.maketrans({" ": "-"}), "en"),
    TranslateTestCase("UPPER", str.maketrans({"U": "u", "P": "p"}), "en"),
    # Edge cases
    TranslateTestCase("a" * 10000, str.maketrans({"a": "A"}), "en"),  # Very long string
    # Unusual but valid cases
    TranslateTestCase("    ", str.maketrans({" ": "*"}), "en"),  # Strings with only whitespace
    TranslateTestCase("123", str.maketrans({"1": "one", "2": None}), "en"),  # Removing and replacing characters
    TranslateTestCase("hello", {"a": 123}, "en"),  # Non-integer replacement
    TranslateTestCase("hello", "string", "en"),  # String instead of dict
    TranslateTestCase("hello", [1, 2, 3], "en"),  # List instead of dict
    TranslateTestCase("hello", {"hello": "world"}, "en"),  # Dict with string keys
    TranslateTestCase("hello", {"1": 2, "3": 4}, "en"),  # Dict with mixed keys
    TranslateTestCase("hello", {1: "a", 2: "b", "3": "c"}, "en"),  # Mixed key types
    TranslateTestCase("hello", {1.5: "a", 2.5: "b"}, "en"),  # Float keys
    TranslateTestCase("hello", {True: "a", False: "b"}, "en"),  # Boolean keys
    TranslateTestCase("hello", {None: "a"}, "en"),  # None key
    TranslateTestCase("hello", (1, 2, 3), "en"),  # Tuple
    TranslateTestCase("hello", {"a": complex(1, 2)}, "en"),  # Complex number as replacement
    TranslateTestCase("hello", {"a": (1, 2, 3)}, "en"),  # Tuple as replacement
    TranslateTestCase("hello", {"a": [1, 2, 3]}, "en"),  # List as replacement
    TranslateTestCase("hello", {"a": slice(0, 5)}, "en"),  # Slice object as replacement
]


@pytest.mark.parametrize("test_case", translate_test_cases)
def test_translate(test_case: TranslateTestCase) -> None:
    lang_string = LangString(test_case.input_string, test_case.lang)
    result = lang_string.translate(test_case.table)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    assert result.text == test_case.expected_output, f"translate(table) failed for '{test_case.input_string}'"
    assert result.lang == test_case.lang, "Language tag should remain unchanged"


invalid_table_test_cases = [
    123,  # Integer
    None,  # NoneType
    complex(1, 2),  # Complex number
    slice(0, 5),  # Slice object
]


@pytest.mark.parametrize("invalid_table", invalid_table_test_cases)
def test_translate_invalid_table(invalid_table: dict[int, str]) -> None:
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError):
        lang_string.translate(invalid_table)
