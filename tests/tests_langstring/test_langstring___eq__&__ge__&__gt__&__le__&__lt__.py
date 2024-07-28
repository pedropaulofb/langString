import pytest
from langstring import Controller
from langstring import LangString
from langstring import LangStringFlag

comparison_methods_to_test = ["__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__"]


class StringMethodComparisonTestCase:
    def __init__(self, input_string1, lang1, input_string2, lang2):
        self.input_string1 = input_string1
        self.lang1 = lang1
        self.input_string2 = input_string2
        self.lang2 = lang2
        self.expected_results = self.compute_expected_results()

    def compute_expected_results(self):
        results = {}
        # Check if input is not a string or LangString
        if not isinstance(self.input_string1, (str, LangString)) or not isinstance(
            self.input_string2, (str, LangString)
        ):
            return {method: NotImplemented for method in comparison_methods_to_test}

        lang_string1 = LangString(self.input_string1, self.lang1)
        lang_string2 = LangString(self.input_string2, self.lang2)

        # For __eq__ and __ne__, compare both text and language
        results["__eq__"] = (lang_string1.text == lang_string2.text) and (
            lang_string1.lang.casefold() == lang_string2.lang.casefold()
        )
        results["__ne__"] = (lang_string1.text != lang_string2.text) or (
            lang_string1.lang.casefold() != lang_string2.lang.casefold()
        )

        # For other methods, raise ValueError if languages do not match
        if lang_string1.lang.casefold() != lang_string2.lang.casefold():
            results.update({method: ValueError for method in ["__lt__", "__le__", "__gt__", "__ge__"]})
        else:
            results["__lt__"] = lang_string1.text < lang_string2.text
            results["__le__"] = lang_string1.text <= lang_string2.text
            results["__gt__"] = lang_string1.text > lang_string2.text
            results["__ge__"] = lang_string1.text >= lang_string2.text

        return results

    def perform_comparison(self, method):
        if self.expected_results[method] is NotImplemented:
            return NotImplemented
        lang_string1 = LangString(self.input_string1, self.lang1)
        lang_string2 = LangString(self.input_string2, self.lang2)
        return getattr(lang_string1, method)(lang_string2)


valid_comparison_test_cases = [
    # Comparisons with same language tags
    StringMethodComparisonTestCase("apple", "en", "banana", "en"),  # apple < banana
    StringMethodComparisonTestCase("apple", "en-uk", "banana", "en-uk"),  # apple < banana
    StringMethodComparisonTestCase("banana", "en", "apple", "en"),  # banana > apple
    StringMethodComparisonTestCase("apple", "en", "apple", "en"),  # apple == apple
    StringMethodComparisonTestCase("banana", "en", "banana", "en"),  # banana == banana
    StringMethodComparisonTestCase("apple", "en", "APPLE", "en"),  # Case sensitivity
    StringMethodComparisonTestCase("", "en", "apple", "en"),  # Empty string < apple
    StringMethodComparisonTestCase("apple", "en", "", "en"),  # apple > Empty string
    StringMethodComparisonTestCase("", "en", "", "en"),  # Empty string == Empty string
    StringMethodComparisonTestCase("apple", "", "apple", ""),
    # Unicode comparisons
    StringMethodComparisonTestCase("äpple", "en", "banana", "en"),  # Unicode characters
    StringMethodComparisonTestCase("😊", "en", "😊😊", "en"),  # Emoji comparison
    # Numeric string comparisons
    StringMethodComparisonTestCase("2", "en", "10", "en"),  # '2' < '10' as strings
    # Cyrillic, Japanese, Greek, etc., comparisons
    StringMethodComparisonTestCase("яблоко", "ru", "банан", "ru"),  # Cyrillic
    StringMethodComparisonTestCase("りんご", "ja", "バナナ", "ja"),  # Japanese
    StringMethodComparisonTestCase("μήλο", "el", "μπανάνα", "el"),  # Greek
    # Comparisons with different capitalizations of language tags
    StringMethodComparisonTestCase("apple", "EN", "banana", "en"),  # Capitalized language tag
    StringMethodComparisonTestCase("apple", "En", "banana", "eN"),  # Mixed case language tags
    StringMethodComparisonTestCase("apple", "EN", "apple", "en"),
    StringMethodComparisonTestCase("apple", "En", "apple", "eN"),
    # Extended charset
    StringMethodComparisonTestCase("hello!@#", "en", "hello123", "en"),
    StringMethodComparisonTestCase("12345", "en", "12345!", "en"),
    StringMethodComparisonTestCase("longstring" * 100, "en", "longstring" * 100 + "extra", "en"),
]


@pytest.mark.parametrize(
    "test_case, method", [(tc, m) for tc in valid_comparison_test_cases for m in comparison_methods_to_test]
)
@pytest.mark.parametrize("strict", [True, False])
def test_string_methods_valid_comparison(test_case, method, strict):
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    actual_result = test_case.perform_comparison(method)
    expected_result = test_case.expected_results[method]
    assert (
        actual_result == expected_result
    ), f"{method} failed for '{test_case.input_string1}@{test_case.lang1}' and '{test_case.input_string2}@{test_case.lang2}'"


invalid_comparison_test_cases = [
    # Invalid comparisons with non-LangString objects
    StringMethodComparisonTestCase("apple", "en", 123, "en"),  # Non-LangString comparison
    StringMethodComparisonTestCase("apple", "en", None, "en"),  # Non-LangString comparison
    # Comparisons with non-LangString objects
    StringMethodComparisonTestCase("apple", "en", 123, None),
    StringMethodComparisonTestCase("apple", "en", True, None),
    StringMethodComparisonTestCase("apple", "en", None, None),
    StringMethodComparisonTestCase("apple", "en", ["apple"], None),
    StringMethodComparisonTestCase("apple", "en", {"apple": 1}, None),
]


@pytest.mark.parametrize(
    "test_case, method", [(tc, m) for tc in invalid_comparison_test_cases for m in comparison_methods_to_test]
)
@pytest.mark.parametrize("strict", [True, False])
def test_string_methods_invalid_comparison(test_case, method, strict):
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    actual_result = test_case.perform_comparison(method)
    assert actual_result is NotImplemented, f"{method} did not return NotImplemented for invalid comparison"


incompatible_language_test_cases = [
    StringMethodComparisonTestCase("apple", " en", "apple", "en"),
    StringMethodComparisonTestCase("apple", "en", "apple", "en "),
    StringMethodComparisonTestCase("apple", "en", "apple", "e n"),
    StringMethodComparisonTestCase("apple", "en", "apple", "fr"),
    StringMethodComparisonTestCase("banana", "en", "banana", "de"),
    StringMethodComparisonTestCase("orange", "en", "orange", "es"),
    StringMethodComparisonTestCase("grape", "en", "grape", "it"),
    StringMethodComparisonTestCase("apple", "en", "яблоко", "ru"),
    StringMethodComparisonTestCase("りんご", "ja", "apple", "en"),
    StringMethodComparisonTestCase("사과", "ko", "apple", "en"),
    StringMethodComparisonTestCase("manzana", "es", "apple", "en"),
    # Test with more complex language tags
    StringMethodComparisonTestCase("apple", "en-US", "apple", "en-GB"),
    StringMethodComparisonTestCase("apple", "en-AU", "apple", "en-CA"),
]


@pytest.mark.parametrize(
    "test_case, method", [(tc, m) for tc in incompatible_language_test_cases for m in comparison_methods_to_test]
)
@pytest.mark.parametrize("strict", [True, False])
def test_string_methods_incompatible_language_comparison(test_case, method, strict):
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_string1 = LangString(test_case.input_string1, test_case.lang1)
    lang_string2 = LangString(test_case.input_string2, test_case.lang2)

    if method in ["__eq__", "__ne__"]:
        expected_result = test_case.compute_expected_results()[method]
        actual_result = getattr(lang_string1, method)(lang_string2)
        assert actual_result == expected_result
    else:
        with pytest.raises(ValueError, match="Incompatible languages"):
            getattr(lang_string1, method)(lang_string2)


not_impl_test_cases = [
    ["apple", "en", 123],  # int
    ["apple", "en", 123.45],  # float
    ["apple", "en", True],  # bool
    ["apple", "en", ["apple"]],  # list
    ["apple", "en", {"apple": 1}],  # dict
]


@pytest.mark.parametrize("test_case", not_impl_test_cases)
@pytest.mark.parametrize("method", ["__eq__", "__ne__", "__ge__", "__gt__", "__le__", "__lt__"])
def test_not_implemented_comparisons(test_case, method):
    """Test the comparison methods of the LangString class with non-string and non-LangString objects.

    :param test_case: A test case for the __eq__ and __ne__ methods.
    :type test_case: list
    :param method: The method to test (__eq__ or __ne__).
    :type method: str
    """
    ls = LangString(
        test_case[0], test_case[1]
    )  # Create LangString from pos 0 and 1 from lists inside not_impl_test_cases
    other = test_case[2]  # Get the object to compare from pos 2 from lists inside not_impl_test_cases
    actual_result = getattr(ls, method)(other)  # Perform comparison between ls and other
    assert actual_result is NotImplemented, f"{method} did not return NotImplemented for invalid comparison"


cases_ls_string = [
    ["apple", "en", "apple"],
    ["apple", "en", "apple "],
    ["apple", "en", " apple"],
    ["apple", "en", "Apple"],
    ["apple", "en", "APPLE"],
]


@pytest.mark.parametrize("test_case", cases_ls_string)
@pytest.mark.parametrize("method", ["__eq__", "__ne__", "__ge__", "__gt__", "__le__", "__lt__"])
def test_langstring_string_comparisons(test_case, method):
    """Test the comparison methods of the LangString class with non-string and non-LangString objects.

    :param test_case: A test case for the __eq__ and __ne__ methods.
    :type test_case: list
    :param method: The method to test (__eq__ or __ne__).
    :type method: str
    """
    ls = LangString(
        test_case[0], test_case[1]
    )  # Create LangString from pos 0 and 1 from lists inside not_impl_test_cases
    other = test_case[2]  # Get the object to compare from pos 2 from lists inside not_impl_test_cases
    actual_result = getattr(ls, method)(other)  # Perform comparison between ls and other
    assert actual_result in [True, False], f"{method} did return NotImplemented for invalid comparison"
