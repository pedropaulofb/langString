import pytest
from langstring import SetLangString


class SetLangStringOperationTestCase:
    def __init__(self, texts, lang, text_to_remove):
        self.texts = texts
        self.lang = lang
        self.text_to_remove = text_to_remove

    def run_test(self, method_name):
        set_lang_string = SetLangString(texts=self.texts, lang=self.lang)
        method = getattr(set_lang_string, method_name)
        try:
            method(self.text_to_remove)
            return set_lang_string, None
        except KeyError as e:
            return set_lang_string, e


def calculate_expected_result(texts, text_to_remove, method_name):
    result_set = set(texts)
    if method_name == "discard_text":
        result_set.discard(text_to_remove)
    elif method_name == "remove_text":
        if text_to_remove in result_set:
            result_set.remove(text_to_remove)
        else:
            return result_set, KeyError
    return result_set, None


# Define test cases
operation_test_cases = [
    # Removing existing elements
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", "b"),
    SetLangStringOperationTestCase({"x", "y", "z"}, "en", "y"),
    SetLangStringOperationTestCase({"1", "2", "3"}, "en", "2"),
    SetLangStringOperationTestCase({"apple", "banana", "cherry"}, "en", "cherry"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", "hello"),
    # Attempting to remove elements not in the set
    SetLangStringOperationTestCase({"a", "b", "c"}, "en", "d"),
    SetLangStringOperationTestCase({"x", "y", "z"}, "en", "a"),
    SetLangStringOperationTestCase({"1", "2", "3"}, "en", "4"),
    SetLangStringOperationTestCase({"apple", "banana", "cherry"}, "en", "grape"),
    SetLangStringOperationTestCase({"hello", "world"}, "en", "universe"),
    # Sets with mixed content
    SetLangStringOperationTestCase({"hello", "😊", "world"}, "en", "😊"),
    SetLangStringOperationTestCase({"123", "abc", "😜"}, "en", "abc"),
    SetLangStringOperationTestCase({"HELLO", "WORLD"}, "en", "WORLD"),
    SetLangStringOperationTestCase({"apple", "1", "banana"}, "en", "1"),
    # Sets with special characters
    SetLangStringOperationTestCase({"!", "@", "#"}, "en", "@"),
    SetLangStringOperationTestCase({"$", "%", "^"}, "en", "%"),
    # Sets with emojis
    SetLangStringOperationTestCase({"😊", "😂", "😜"}, "en", "😜"),
    SetLangStringOperationTestCase({"🍏", "🍎"}, "en", "🍏"),
    # Sets with numeric strings
    SetLangStringOperationTestCase({"123", "456"}, "en", "123"),
    SetLangStringOperationTestCase({"100", "200"}, "en", "300"),  # Not in set
    # Sets with empty strings and spaces
    SetLangStringOperationTestCase({"", " "}, "en", " "),
    SetLangStringOperationTestCase({"   ", ""}, "en", "   "),
    # Sets with case sensitivity
    SetLangStringOperationTestCase({"Hello", "World"}, "en", "hello"),  # Not in set
    SetLangStringOperationTestCase({"APPLE", "BANANA"}, "en", "apple"),  # Not in set
    # Sets with spaces
    SetLangStringOperationTestCase({" hello ", " world"}, "en", "hello"),  # Not in set
    SetLangStringOperationTestCase({" good ", " morning"}, "en", " good "),
    # More complex sets
    SetLangStringOperationTestCase({"apple", "orange", "banana"}, "en", "melon"),  # Not in set
    SetLangStringOperationTestCase({"cat", "dog", "bird"}, "en", "dog"),
    # Sets with Cyrillic and Japanese characters
    SetLangStringOperationTestCase({"привет", "мир"}, "ru", "мир"),
    SetLangStringOperationTestCase({"こんにちは", "世界"}, "jp", "地球"),  # Not in set
    # Sets with mixed alphabets and special characters
    SetLangStringOperationTestCase({"a", "#", "c"}, "en", "#"),
    SetLangStringOperationTestCase({"1", "b", "@"}, "en", "c"),  # Not in set
]


@pytest.mark.parametrize("test_case", operation_test_cases)
@pytest.mark.parametrize("method_name", ["discard_text", "remove_text"])
def test_setlangstring_operation_methods(test_case, method_name):
    result_set_lang_string, error = test_case.run_test(method_name)
    expected_result, expected_error = calculate_expected_result(test_case.texts, test_case.text_to_remove, method_name)

    assert (
        set(result_set_lang_string.texts) == expected_result
    ), f"Failed {method_name} for texts={test_case.texts} with text_to_remove={test_case.text_to_remove}"
    assert (error is None) == (
        expected_error is None
    ), f"Unexpected error behavior in {method_name} for text_to_remove={test_case.text_to_remove}"
