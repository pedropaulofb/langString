from langstring import SetLangString


def test_copy_method_basic() -> None:
    """
    Test the basic functionality of the copy method to ensure it creates an exact copy of the SetLangString object.

    :return: None. Asserts if the copy is an exact replica of the original.
    """
    original = SetLangString(texts={"a", "b", "c"}, lang="en")
    copied = original.copy()
    assert (
        copied.texts == original.texts and copied.lang == original.lang
    ), "Copy method did not create an exact replica of the SetLangString object."


def test_copy_method_distinct_object() -> None:
    """
    Test that the copy method creates a new distinct object, not just a reference to the original object.

    :return: None. Asserts if the copy is a distinct object.
    """
    original = SetLangString(texts={"a", "b", "c"}, lang="en")
    copied = original.copy()
    assert copied is not original, "Copy method did not create a distinct object."


def test_copy_method_mutability() -> None:
    """
    Test that changes to the texts of the copied SetLangString do not affect the original object.

    :return: None. Asserts if the original object remains unchanged after modifications to the copy.
    """
    original = SetLangString(texts={"a", "b", "c"}, lang="en")
    copied = original.copy()
    copied.texts.add("d")
    assert "d" not in original.texts, "Changes to the copy affected the original SetLangString object."


def test_copy_method_empty_set() -> None:
    """
    Test the copy method on an empty SetLangString object.

    :return: None. Asserts if the copy of an empty SetLangString is correct.
    """
    original = SetLangString(texts=set(), lang="en")
    copied = original.copy()
    assert copied.texts == set() and copied.lang == "en", "Copy of an empty SetLangString is incorrect."


def test_copy_method_special_characters() -> None:
    """
    Test the copy method on a SetLangString object with special characters and emojis.

    :return: None. Asserts if the copy handles special characters and emojis correctly.
    """
    original = SetLangString(texts={"😊", "🍏", "#", "$"}, lang="en")
    copied = original.copy()
    assert copied.texts == original.texts, "Copy method failed with special characters and emojis."


def test_copy_method_large_dataset() -> None:
    """
    Test the copy method on a SetLangString object with a large dataset.

    :return: None. Asserts if the copy handles a large dataset correctly.
    """
    large_dataset = {str(i) for i in range(10000)}  # Large dataset with 10,000 elements
    original = SetLangString(texts=large_dataset, lang="en")
    copied = original.copy()
    assert copied.texts == original.texts, "Copy method failed with a large dataset."
