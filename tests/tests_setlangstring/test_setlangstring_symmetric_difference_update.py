import pytest
from langstring import Controller
from langstring import SetLangString
from langstring import SetLangStringFlag


class SetLangStringSymDiffUpdateTestCase:
    def __init__(self, texts1, lang1, texts2, lang2):
        self.initial_texts1 = texts1
        self.lang1 = lang1
        self.initial_texts2 = texts2
        self.lang2 = lang2
        self.expected_result = self.calculate_expected_result(texts1, texts2)

    def recreate_set_lang_strings(self):
        self.set1 = SetLangString(texts=self.initial_texts1, lang=self.lang1)
        self.set2 = (
            SetLangString(texts=self.initial_texts2, lang=self.lang2)
            if isinstance(self.initial_texts2, set)
            else self.initial_texts2
        )

    @staticmethod
    def calculate_expected_result(texts1, texts2):
        temp_texts1 = texts1.copy()
        temp_texts2 = texts2.copy() if isinstance(texts2, set) else texts2.texts.copy()
        temp_texts1.symmetric_difference_update(temp_texts2)
        return temp_texts1


sym_diff_update_test_cases = [
    # Identical sets
    SetLangStringSymDiffUpdateTestCase({"a", "b", "c"}, "en", {"a", "b", "c"}, "en"),
    # Completely different sets
    SetLangStringSymDiffUpdateTestCase({"a", "b", "c"}, "en", {"d", "e", "f"}, "en"),
    # Partially overlapping sets
    SetLangStringSymDiffUpdateTestCase({"a", "b", "c"}, "en", {"b", "c", "d"}, "en"),
    # Single element sets
    SetLangStringSymDiffUpdateTestCase({"a"}, "en", {"b"}, "en"),
    # Empty set with non-empty set
    SetLangStringSymDiffUpdateTestCase(set(), "en", {"a", "b"}, "en"),
    # Non-empty set with empty set
    SetLangStringSymDiffUpdateTestCase({"a", "b"}, "en", set(), "en"),
    # Both sets empty
    SetLangStringSymDiffUpdateTestCase(set(), "en", set(), "en"),
    # Sets with numeric strings
    SetLangStringSymDiffUpdateTestCase({"1", "2", "3"}, "en", {"3", "4", "5"}, "en"),
    # Sets with mixed content (strings, numbers)
    SetLangStringSymDiffUpdateTestCase({"a", "1", "b"}, "en", {"1", "2", "c"}, "en"),
    # Sets with special characters
    SetLangStringSymDiffUpdateTestCase({"!", "@", "#"}, "en", {"$", "%", "^"}, "en"),
    # Sets with emojis
    SetLangStringSymDiffUpdateTestCase({"😊", "😂"}, "en", {"😂", "🤣"}, "en"),
    # Sets with mixed alphabets (e.g., Cyrillic, Latin)
    SetLangStringSymDiffUpdateTestCase({"hello", "мир"}, "en", {"мир", "world"}, "en"),
    # Case sensitivity check
    SetLangStringSymDiffUpdateTestCase({"Hello", "World"}, "en", {"hello", "world"}, "en"),
    # Sets with spaces and empty strings
    SetLangStringSymDiffUpdateTestCase({" ", "  "}, "en", {"   ", ""}, "en"),
    # Complex sets with mixed content
    SetLangStringSymDiffUpdateTestCase({"apple", "123", "😊"}, "en", {"banana", "123", "😂"}, "en"),
    # Other
    SetLangStringSymDiffUpdateTestCase({"a" * 1000, "b" * 1000}, "en", {"b" * 1000, "c" * 1000}, "en"),
    SetLangStringSymDiffUpdateTestCase({"こんにちは", "世界"}, "jp", {"世界", "地球"}, "jp"),
    SetLangStringSymDiffUpdateTestCase({"مرحبا", "عالم"}, "ar", {"عالم", "كوكب"}, "ar"),
    SetLangStringSymDiffUpdateTestCase({"Apple", "Banana"}, "en", {"apple", "banana"}, "en"),
    SetLangStringSymDiffUpdateTestCase({"valid", "<invalid>"}, "en", {"<invalid>", "also_valid"}, "en"),
]


@pytest.mark.parametrize("test_case", sym_diff_update_test_cases)
@pytest.mark.parametrize("strict", [False, True])
def test_setlangstring_symmetric_difference_update(test_case, strict):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict)
    test_case.recreate_set_lang_strings()  # Recreate SetLangString instances
    test_case.set1.symmetric_difference_update(test_case.set2)
    assert test_case.set1.texts == test_case.expected_result, "Symmetric difference update result mismatch"
