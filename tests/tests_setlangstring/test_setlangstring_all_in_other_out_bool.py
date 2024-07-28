import pytest
from langstring import Controller
from langstring import SetLangString
from langstring import SetLangStringFlag


class SetLangStringComparisonTestCase:
    def __init__(self, texts1, lang1, texts2, lang2):
        self.texts1 = texts1
        self.lang1 = lang1
        self.texts2 = texts2
        self.lang2 = lang2
        self.set1 = SetLangString(texts=texts1, lang=lang1)
        self.set2 = SetLangString(texts=texts2, lang=lang2)
        self.expected_results = {
            "__ge__": texts1 >= texts2,
            "__gt__": texts1 > texts2,
            "__le__": texts1 <= texts2,
            "__lt__": texts1 < texts2,
            "isdisjoint": texts1.isdisjoint(texts2),
            "issubset": texts1.issubset(texts2),
            "issuperset": texts1.issuperset(texts2),
        }

    def run_test(self, method_name):
        method = getattr(self.set1, method_name)
        return method(self.set2)


comparison_test_cases_same_lang = [
    # (texts1, lang1, texts2, lang2)
    # Identical sets and languages
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    # Different sets, same language
    SetLangStringComparisonTestCase({"a", "b"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"b", "c"}, "en"),
    # Subset and superset
    SetLangStringComparisonTestCase({"a"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"a"}, "en"),
    # Disjoint sets
    SetLangStringComparisonTestCase({"a", "b"}, "en", {"c", "d"}, "en"),
    # Empty sets
    SetLangStringComparisonTestCase(set(), "en", {"a", "b", "c"}, "en"),
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", set(), "en"),
    SetLangStringComparisonTestCase(set(), "en", set(), "en"),
    # Different languages, same texts
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    # Different languages, different texts
    SetLangStringComparisonTestCase({"a", "b"}, "en", {"c", "d"}, "en"),
    SetLangStringComparisonTestCase({"x", "y"}, "en", {"z"}, "en"),
    # Overlapping sets, different languages
    SetLangStringComparisonTestCase({"a", "b", "c"}, "en", {"b", "c", "d"}, "en"),
    SetLangStringComparisonTestCase({"m", "n"}, "en", {"n", "o"}, "en"),
    # Single element sets
    SetLangStringComparisonTestCase({"a"}, "en", {"a"}, "en"),
    SetLangStringComparisonTestCase({"a"}, "en", {"b"}, "en"),
    SetLangStringComparisonTestCase({"a"}, "EN", {"a"}, "en"),
    # Complex sets
    SetLangStringComparisonTestCase({"apple", "banana", "cherry"}, "en", {"banana", "date", "fig"}, "en"),
    SetLangStringComparisonTestCase({"1", "2", "3"}, "en", {"4", "5", "6"}, "en"),
    SetLangStringComparisonTestCase({"alpha", "beta"}, "en", {"beta", "gamma"}, "en"),
    # Cyrillic alphabet
    SetLangStringComparisonTestCase({"привет", "мир"}, "en", {"мир", "земля"}, "en"),
    SetLangStringComparisonTestCase({"привет"}, "EN", {"hello"}, "en"),
    # Japanese characters
    SetLangStringComparisonTestCase({"こんにちは", "世界"}, "en", {"世界", "地球"}, "en"),
    SetLangStringComparisonTestCase({"こんにちは"}, "EN", {"hello"}, "en"),
    # Mixed alphabets
    SetLangStringComparisonTestCase({"hello", "привет"}, "en", {"привет", "мир"}, "en"),
    SetLangStringComparisonTestCase({"hello", "こんにちは"}, "en", {"こんにちは", "世界"}, "en"),
    # Upper, lower, and mixed case
    SetLangStringComparisonTestCase({"HELLO", "WORLD"}, "en", {"hello", "world"}, "en"),
    SetLangStringComparisonTestCase({"Hello", "World"}, "en", {"HELLO", "WORLD"}, "en"),
    # Emojis
    SetLangStringComparisonTestCase({"😊", "😂"}, "en", {"😂", "🤣"}, "En"),
    SetLangStringComparisonTestCase({"😊"}, "en", {"😂"}, "en"),
    # Mixed content (alphabets, cases, emojis)
    SetLangStringComparisonTestCase({"hello", "WORLD", "😊"}, "en", {"WORLD", "мир", "🤣"}, "en"),
    SetLangStringComparisonTestCase({"こんにちは", "WORLD", "😂"}, "en", {"WORLD", "hello", "😊"}, "en"),
    # Numeric and special characters
    SetLangStringComparisonTestCase({"123", "456"}, "en", {"456", "789"}, "En"),
    SetLangStringComparisonTestCase({"!@#", "$%^"}, "en", {"$%^", "&*("}, "En"),
    # Mixed numeric, alphabets, and special characters
    SetLangStringComparisonTestCase({"abc", "123", "!@#"}, "en", {"123", "def", "$%^"}, "en"),
    # Empty sets
    SetLangStringComparisonTestCase(set(), "en", set(), "en"),
    SetLangStringComparisonTestCase({"hello", "world"}, "en", set(), "En"),
    SetLangStringComparisonTestCase(set(), "en", {"hello", "world"}, "En"),
    # Sets with only empty strings
    SetLangStringComparisonTestCase({"", ""}, "en", {"", ""}, "en"),
    SetLangStringComparisonTestCase({"hello", "world"}, "en", {"", ""}, "En"),
    SetLangStringComparisonTestCase({"", ""}, "eN", {"hello", "world"}, "En"),
    # Sets with only spaces
    SetLangStringComparisonTestCase({" ", "  "}, "en", {" ", "  "}, "en"),
    SetLangStringComparisonTestCase({"hello", "world"}, "en", {" ", "  "}, "en"),
    SetLangStringComparisonTestCase({" ", "  "}, "en", {"hello", "world"}, "en"),
    # Words with spaces in different positions
    SetLangStringComparisonTestCase({" hello", "world "}, "en", {"hello ", " world"}, "en"),
    SetLangStringComparisonTestCase({"hello", "world"}, "en", {" hello", "world "}, "en"),
    SetLangStringComparisonTestCase({" hello", "world "}, "en", {"hello", "world"}, "en"),
    # Mixed scenarios
    SetLangStringComparisonTestCase({"", " "}, "eN", {"hello", "world"}, "en"),
    SetLangStringComparisonTestCase({"hello", "world"}, "en", {"", " "}, "en"),
    SetLangStringComparisonTestCase({" hello ", " world "}, "en", {"", " "}, "en"),
    SetLangStringComparisonTestCase({"", " "}, "eN", {" hello ", " world "}, "en"),
    SetLangStringComparisonTestCase(set(), "eN", {" hello ", " world "}, "en"),
    SetLangStringComparisonTestCase({" hello ", " world "}, "en", set(), "en"),
]


@pytest.mark.parametrize("test_case", comparison_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name", ["__ge__", "__gt__", "__le__", "__lt__", "isdisjoint", "issubset", "issuperset"]
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_comparison_methods(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    # Adjust the method call based on the strict value
    result = test_case.run_test(method_name)

    assert (
        result == test_case.expected_results[method_name]
    ), f"Failed {method_name} comparison for {test_case.set1} and {test_case.set2} with strict={strict}"


@pytest.mark.parametrize("test_case", comparison_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name", ["__ge__", "__gt__", "__le__", "__lt__", "isdisjoint", "issubset", "issuperset"]
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_comparison_methods_with_different_lang(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    # Modify lang2 to be different from lang1
    test_case.set2.lang = "different_lang"

    # Run the test and expect a ValueError
    with pytest.raises(ValueError):
        test_case.run_test(method_name)


@pytest.mark.parametrize("test_case", comparison_test_cases_same_lang)
@pytest.mark.parametrize(
    "method_name", ["__ge__", "__gt__", "__le__", "__lt__", "isdisjoint", "issubset", "issuperset"]
)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_comparison_methods_with_set(test_case, method_name, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    strict = Controller.get_flag(SetLangStringFlag.METHODS_MATCH_TYPES)
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
        # Expect the test to pass when strict is False
        result = getattr(set_lang_string, method_name)(regular_set)
        expected = test_case.expected_results[method_name]
        assert result == expected, f"Failed {method_name} comparison for {set_lang_string} and {regular_set}"
