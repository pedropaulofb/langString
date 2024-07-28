import pytest
from langstring import SetLangString


class SetLangStringTestCase:
    def __init__(self, texts, lang):
        self.texts = texts
        self.lang = lang

    def run_test(self, method_name):
        set_lang_string = SetLangString(texts=self.texts, lang=self.lang)
        method = getattr(set_lang_string, method_name)
        return method()


# Define test cases
test_cases = [
    SetLangStringTestCase({"a", "b", "c"}, "en"),  # Basic set
    SetLangStringTestCase({"x", "y", "z"}, "en"),  # Different basic set
    SetLangStringTestCase({"1", "2", "3"}, "en"),  # Numeric strings
    SetLangStringTestCase({"apple", "banana", "cherry"}, "en"),  # Longer strings
    SetLangStringTestCase({"hello", "world"}, "en"),  # Common words
    SetLangStringTestCase({"😊", "😂", "😜"}, "en"),  # Emojis
    SetLangStringTestCase({"🍏", "🍎"}, "en"),  # Emojis (fruits)
    SetLangStringTestCase({"HELLO", "WORLD"}, "en"),  # Uppercase strings
    SetLangStringTestCase({" ", "  "}, "en"),  # Strings with spaces
    SetLangStringTestCase(set(), "en"),  # Empty set
    SetLangStringTestCase({"a", "a", "b"}, "en"),  # Set with duplicates
    SetLangStringTestCase({"", " "}, "en"),  # Empty string and space
    SetLangStringTestCase({"hello", "HELLO"}, "en"),  # Case sensitivity
    SetLangStringTestCase({"123", "456", "789"}, "en"),  # Only numeric strings
    SetLangStringTestCase({"@", "#", "$"}, "en"),  # Special characters
    SetLangStringTestCase({"alpha", "beta", "gamma"}, "en"),  # Greek letters
    SetLangStringTestCase({"привет", "мир"}, "ru"),  # Cyrillic characters
    SetLangStringTestCase({"こんにちは", "世界"}, "jp"),  # Japanese characters
    SetLangStringTestCase({"one", "two", "three", "four"}, "en"),  # Larger set
    SetLangStringTestCase({"single"}, "en"),  # Single element
    SetLangStringTestCase({"hello", "привет", "こんにちは"}, "en"),
    SetLangStringTestCase({"abc", "123", "xyz789"}, "en"),
    SetLangStringTestCase({"This is a very long string", "Another long string"}, "en"),
    SetLangStringTestCase({"Line1\nLine2", "Tab\tSeparated"}, "en"),
    SetLangStringTestCase({"string", "string "}, "en"),  # Note the space in the second string
    SetLangStringTestCase({"√", "π", "Ω"}, "en"),
    SetLangStringTestCase(set(str(i) for i in range(1000)), "en"),
]


@pytest.mark.parametrize("test_case", test_cases)
@pytest.mark.parametrize("method_name", ["__hash__", "__len__"])
def test_setlangstring_methods(test_case, method_name):
    result = test_case.run_test(method_name)
    if method_name == "__hash__":
        assert isinstance(result, int), f"Failed {method_name} for texts={test_case.texts}"
    elif method_name == "__len__":
        assert result == len(test_case.texts), f"Failed {method_name} for texts={test_case.texts}"
