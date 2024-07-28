import pytest
from langstring import Controller
from langstring import SetLangString
from langstring import SetLangStringFlag


class SetLangStringOperationTestCase:
    def __init__(self, texts1, lang1, texts2, lang2):
        self.texts1 = texts1
        self.lang1 = lang1
        self.texts2 = texts2
        self.lang2 = lang2
        self.set1 = SetLangString(texts=texts1, lang=lang1)
        self.set2 = SetLangString(texts=texts2, lang=lang2)
        self.expected_results = {
            "__and__": texts1 & texts2,
            "__or__": texts1 | texts2,
            "__sub__": texts1 - texts2,
            "__xor__": texts1 ^ texts2,
            "__iand__": texts1 & texts2,
            "__ior__": texts1 | texts2,
            "__isub__": texts1 - texts2,
            "__ixor__": texts1 ^ texts2,
            "symmetric_difference": texts1.symmetric_difference(texts2),
        }

    def run_test(self, method_name):
        # Create a copy of set1 for in-place operations
        set1_copy = SetLangString(texts=self.texts1, lang=self.lang1)
        method = getattr(set1_copy, method_name)
        return method(self.set2)


operation_test_cases_same_lang = [
    # (texts1, lang1, texts2, lang2)
    # Identical sets and languages
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    # Different sets, same language
    SetLangStringOperationTestCase({"a", "b"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"b", "c"}, "en"),
    # Subset and superset
    SetLangStringOperationTestCase({"a"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"a"}, "en"),
    # Disjoint sets
    SetLangStringOperationTestCase({"a", "b"}, "en", {"c", "d"}, "en"),
    # Empty sets
    SetLangStringOperationTestCase(set(), "en", {"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", set(), "en"),
    SetLangStringOperationTestCase(set(), "en", set(), "en"),
    # Different languages, same texts
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    # Different languages, different texts
    SetLangStringOperationTestCase({"a", "b"}, "en", {"c", "d"}, "en"),
    SetLangStringOperationTestCase({"x", "y"}, "en", {"z"}, "en"),
    # Overlapping sets, different languages
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", {"b", "c", "d"}, "en"),
    SetLangStringOperationTestCase({"m", "n"}, "en", {"n", "o"}, "en"),
    # Single element sets
    SetLangStringOperationTestCase({"a"}, "en", {"a"}, "en"),
    SetLangStringOperationTestCase({"a"}, "en", {"b"}, "en"),
    SetLangStringOperationTestCase({"a"}, "EN", {"a"}, "en"),
    # Complex sets
    SetLangStringOperationTestCase({"apple", "banana", "cherry"}, "en", {"banana", "date", "fig"}, "en"),
    SetLangStringOperationTestCase({"1", "2", "3"}, "en", {"4", "5", "6"}, "en"),
    SetLangStringOperationTestCase({"alpha", "beta"}, "en", {"beta", "gamma"}, "en"),
    # Cyrillic alphabet
    SetLangStringOperationTestCase({"привет", "мир"}, "en", {"мир", "земля"}, "en"),
    SetLangStringOperationTestCase({"привет"}, "EN", {"hello"}, "en"),
    # Japanese characters
    SetLangStringOperationTestCase({"こんにちは", "世界"}, "en", {"世界", "地球"}, "en"),
    SetLangStringOperationTestCase({"こんにちは"}, "EN", {"hello"}, "en"),
    # Mixed alphabets
    SetLangStringOperationTestCase({"hello", "привет"}, "en", {"привет", "мир"}, "en"),
    SetLangStringOperationTestCase({"hello", "こんにちは"}, "en", {"こんにちは", "世界"}, "en"),
    # Upper, lower, and mixed case
    SetLangStringOperationTestCase({"HELLO", "WORLD"}, "en", {"hello", "world"}, "en"),
    SetLangStringOperationTestCase({"Hello", "World"}, "en", {"HELLO", "WORLD"}, "en"),
    # Emojis
    SetLangStringOperationTestCase({"😊", "😂"}, "en", {"😂", "🤣"}, "En"),
    SetLangStringOperationTestCase({"😊"}, "en", {"😂"}, "en"),
    # Mixed content (alphabets, cases, emojis)
    SetLangStringOperationTestCase({"hello", "WORLD", "😊"}, "en", {"WORLD", "мир", "🤣"}, "en"),
    SetLangStringOperationTestCase({"こんにちは", "WORLD", "😂"}, "en", {"WORLD", "hello", "😊"}, "en"),
    # Numeric and special characters
    SetLangStringOperationTestCase({"123", "456"}, "en", {"456", "789"}, "En"),
    SetLangStringOperationTestCase({"!@#", "$%^"}, "en", {"$%^", "&*("}, "En"),
    # Mixed numeric, alphabets, and special characters
    SetLangStringOperationTestCase({"abc", "123", "!@#"}, "en", {"123", "def", "$%^"}, "en"),
    # Empty sets
    SetLangStringOperationTestCase(set(), "en", set(), "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", set(), "En"),
    SetLangStringOperationTestCase(set(), "en", {"hello", "world"}, "En"),
    # Sets with only empty strings
    SetLangStringOperationTestCase({"", ""}, "en", {"", ""}, "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", {"", ""}, "En"),
    SetLangStringOperationTestCase({"", ""}, "eN", {"hello", "world"}, "En"),
    # Sets with only spaces
    SetLangStringOperationTestCase({" ", "  "}, "en", {" ", "  "}, "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", {" ", "  "}, "en"),
    SetLangStringOperationTestCase({" ", "  "}, "en", {"hello", "world"}, "en"),
    # Words with spaces in different positions
    SetLangStringOperationTestCase({" hello", "world "}, "en", {"hello ", " world"}, "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", {" hello", "world "}, "en"),
    SetLangStringOperationTestCase({" hello", "world "}, "en", {"hello", "world"}, "en"),
    # Mixed scenarios
    SetLangStringOperationTestCase({"", " "}, "eN", {"hello", "world"}, "en"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", {"", " "}, "en"),
    SetLangStringOperationTestCase({" hello ", " world "}, "en", {"", " "}, "en"),
    SetLangStringOperationTestCase({"", " "}, "eN", {" hello ", " world "}, "en"),
    SetLangStringOperationTestCase(set(), "eN", {" hello ", " world "}, "en"),
    SetLangStringOperationTestCase({" hello ", " world "}, "en", set(), "en"),
]


@pytest.mark.parametrize("test_case", operation_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name",
    ["__and__", "__or__", "__sub__", "__xor__", "__iand__", "__ior__", "__isub__", "__ixor__", "symmetric_difference"],
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_operation_methods(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    got_strict = Controller.get_flag(SetLangStringFlag.METHODS_MATCH_TYPES)
    result = test_case.run_test(method_name)
    expected = test_case.expected_results[method_name]

    # Compare the contents of the SetLangString object with the expected set
    if isinstance(result, SetLangString):
        assert (
            set(result.texts) == expected
        ), f"Failed {method_name} for {test_case.set1} and {test_case.set2} with strict={got_strict}"
    else:
        assert (
            result == expected
        ), f"Failed {method_name} for {test_case.set1} and {test_case.set2} with strict={got_strict}"


@pytest.mark.parametrize("test_case", operation_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name",
    ["__and__", "__or__", "__sub__", "__xor__", "__iand__", "__ior__", "__isub__", "__ixor__", "symmetric_difference"],
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_comparison_methods_with_different_lang(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    # Modify lang2 to be different from lang1
    test_case.set2.lang = "different_lang"

    # Run the test and expect a ValueError
    with pytest.raises(ValueError):
        test_case.run_test(method_name)


@pytest.mark.parametrize("test_case", operation_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name",
    ["__and__", "__or__", "__sub__", "__xor__", "__iand__", "__ior__", "__isub__", "__ixor__", "symmetric_difference"],
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_comparison_methods_with_set(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    # Use texts1 and lang1 to build a SetLangString
    set_lang_string = SetLangString(texts=test_case.texts1, lang=test_case.lang1)

    # Use texts2 as a regular set
    regular_set = test_case.texts2

    # Run the test
    if strict is True:
        # Expect a TypeError when strict is True
        with pytest.raises(TypeError):
            getattr(set_lang_string, method_name)(regular_set)
    else:
        # Expect the test to pass when strict is None or False
        result = getattr(set_lang_string, method_name)(regular_set)
        expected = test_case.expected_results[method_name]
        assert result.texts == expected, f"Failed {method_name} comparison for {set_lang_string} and {regular_set}"
