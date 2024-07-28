import pytest
from langstring import SetLangString


class SetLangStringEqualityTestCase:
    def __init__(self, texts1, lang1, texts2, lang2):
        self.set1 = SetLangString(texts=texts1, lang=lang1)
        self.set2 = SetLangString(texts=texts2, lang=lang2)
        self.expected_eq = self.calculate_expected_eq(texts1, lang1, texts2, lang2)
        self.expected_ne = not self.expected_eq

    @staticmethod
    def calculate_expected_eq(texts1, lang1, texts2, lang2):
        return texts1 == texts2 and lang1.casefold() == lang2.casefold()


equality_test_cases = [
    SetLangStringEqualityTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringEqualityTestCase({"a", "b"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringEqualityTestCase({"a", "b", "c"}, "en", {"b", "c"}, "en"),
    SetLangStringEqualityTestCase({"a"}, "en", {"a"}, "EN"),
    SetLangStringEqualityTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "fr"),
    SetLangStringEqualityTestCase(set(), "en", set(), "en"),
    # Identical sets and languages
    SetLangStringEqualityTestCase({"hello", "world"}, "en", {"hello", "world"}, "en"),
    # Different sets, same language
    SetLangStringEqualityTestCase({"hello"}, "en", {"world"}, "en"),
    # Same sets, different languages
    SetLangStringEqualityTestCase({"hello", "world"}, "en", {"hello", "world"}, "fr"),
    # Different sets and languages
    SetLangStringEqualityTestCase({"hello"}, "en", {"world"}, "fr"),
    # Case sensitivity in languages
    SetLangStringEqualityTestCase({"hello"}, "EN", {"hello"}, "en"),
    # Empty set compared with non-empty set
    SetLangStringEqualityTestCase(set(), "en", {"hello"}, "en"),
    # Both sets empty, same language
    SetLangStringEqualityTestCase(set(), "en", set(), "en"),
    # Both sets empty, different languages
    SetLangStringEqualityTestCase(set(), "en", set(), "fr"),
    # Sets with special characters
    SetLangStringEqualityTestCase({"!", "@"}, "en", {"!", "@"}, "en"),
    # Sets with numbers
    SetLangStringEqualityTestCase({"1", "2"}, "en", {"1", "2"}, "en"),
    # Sets with emojis
    SetLangStringEqualityTestCase({"😊", "😂"}, "en", {"😊", "😂"}, "en"),
    # Mixed content sets
    SetLangStringEqualityTestCase({"hello", "1", "😊"}, "en", {"hello", "1", "😊"}, "en"),
    # Sets with spaces
    SetLangStringEqualityTestCase({" hello ", "world"}, "en", {" hello ", "world"}, "en"),
    # Sets with mixed case texts
    SetLangStringEqualityTestCase({"Hello", "World"}, "en", {"hello", "world"}, "en"),
    # Complex sets with multiple elements
    SetLangStringEqualityTestCase({"apple", "banana", "cherry"}, "en", {"apple", "banana", "cherry"}, "en"),
]


@pytest.mark.parametrize("test_case", equality_test_cases)
def test_setlangstring_eq_ne(test_case):
    """
    Test the equality and inequality methods of SetLangString.

    :param test_case: A test case instance containing two SetLangString objects and expected results.
    :return: None. Asserts if the equality and inequality checks pass.
    """
    assert (
        test_case.set1 == test_case.set2
    ) == test_case.expected_eq, f"Equality test failed for {test_case.set1} and {test_case.set2}"
    assert (
        test_case.set1 != test_case.set2
    ) == test_case.expected_ne, f"Inequality test failed for {test_case.set1} and {test_case.set2}"


# Define a dummy class to test comparison with a user-defined object type
class DummyClass:
    pass


# Define the parameterized test cases
@pytest.mark.parametrize(
    "different_type_object",
    [
        "a string",
        42,
        3.14,
        True,
        None,
        [1, 2, 3],
        {"key": "value"},
        DummyClass(),
        (1, 2, 3),
    ],
)
def test_setlangstring_eq_returns_not_implemented(different_type_object):
    """
    Test that SetLangString.__eq__ method returns NotImplemented when compared with objects of different types.
    """
    set_lang_string = SetLangString(texts={"hello", "world"}, lang="en")
    # Directly call the __eq__ method
    result = set_lang_string.__eq__(different_type_object)
    assert (
        result is NotImplemented
    ), f"__eq__ did not return NotImplemented when comparing with {type(different_type_object).__name__}."
