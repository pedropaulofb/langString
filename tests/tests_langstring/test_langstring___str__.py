import pytest
from langstring import Controller
from langstring import LangString
from langstring import LangStringFlag


class StrTestCase:
    def __init__(self, text: str, lang: str, print_with_quotes: bool, print_with_lang: bool, expected_output: str):
        self.text = text
        self.lang = lang
        self.print_with_quotes = print_with_quotes
        self.print_with_lang = print_with_lang
        self.expected_output = expected_output

    def setup(self):
        Controller.set_flag(LangStringFlag.PRINT_WITH_QUOTES, self.print_with_quotes)
        Controller.set_flag(LangStringFlag.PRINT_WITH_LANG, self.print_with_lang)


a1000 = "a" * 1000

str_test_cases = [
    # Default case (both flags True)
    StrTestCase("hello", "en", True, True, '"hello"@en'),
    StrTestCase("", "en", True, True, '""@en'),
    # Quotes only
    StrTestCase("hello", "en", True, False, '"hello"'),
    StrTestCase("こんにちは", "ja", True, False, '"こんにちは"'),
    # Language tag only
    StrTestCase("hello", "en", False, True, "hello@en"),
    StrTestCase("😊", "en", False, True, "😊@en"),
    # Neither
    StrTestCase("hello", "en", False, False, "hello"),
    StrTestCase("123", "en", False, False, "123"),
    # Other
    StrTestCase("Line 1\nLine 2", "en", True, True, '"Line 1\nLine 2"@en'),
    StrTestCase("   ", "en", True, True, '"   "@en'),
    StrTestCase(a1000, "en", True, True, f'"{a1000}"@en'),
    StrTestCase("Café Münster", "de", True, True, '"Café Münster"@de'),
    StrTestCase("", "", True, True, '""@'),
    StrTestCase("12345", "en", True, True, '"12345"@en'),
    StrTestCase("🙂😊", "en", True, True, '"🙂😊"@en'),
    StrTestCase("Text123!@#", "en", True, True, '"Text123!@#"@en'),
    StrTestCase("Line1\\nLine2", "en", True, True, '"Line1\\nLine2"@en'),
    StrTestCase("hello", a1000, True, True, f'"hello"@{a1000}'),  # Extremely long language tag
    StrTestCase("hello", "en-US", True, True, '"hello"@en-US'),  # Language tag with special characters
    StrTestCase("hello", "en", False, False, "hello"),  # Both flags False
    StrTestCase("hello", "en", True, False, '"hello"'),  # Only PRINT_WITH_QUOTES True
    StrTestCase("hello", "en", False, True, "hello@en"),  # Only PRINT_WITH_LANG True
]


@pytest.mark.parametrize("test_case", str_test_cases)
def test_str_method(test_case: StrTestCase):
    test_case.setup()
    lang_string = LangString(test_case.text, test_case.lang)
    assert (
        str(lang_string) == test_case.expected_output
    ), f"__str__ method failed for '{test_case.text}' with lang '{test_case.lang}'"
