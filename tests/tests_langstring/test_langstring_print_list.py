from typing import List
from typing import Optional

import pytest
from langstring import LangString


def test_print_list(capsys):
    """
    Test LangString.print_list method to ensure it correctly formats and prints a list of LangString objects.

    :param capsys: Pytest fixture to capture system output.
    :type capsys: fixture
    """
    lang_str1 = LangString("hello", "en")
    lang_str2 = LangString("world", "en")
    ls_list = [lang_str1, lang_str2]

    LangString.print_list(ls_list)
    captured = capsys.readouterr()
    assert captured.out == '["hello"@en, "world"@en]\n', "Default print with quotes and language tag failed"

    LangString.print_list(ls_list, print_quotes=False)
    captured = capsys.readouterr()
    assert captured.out == "[hello@en, world@en]\n", "Print without quotes failed"

    LangString.print_list(ls_list, print_lang=False)
    captured = capsys.readouterr()
    assert captured.out == '["hello", "world"]\n', "Print without language tag failed"

    LangString.print_list(ls_list, separator="#")
    captured = capsys.readouterr()
    assert captured.out == '["hello"#en, "world"#en]\n', "Print with custom separator failed"


@pytest.mark.parametrize(
    "langstring_list,print_quotes,separator,print_lang,expected_output",
    [
        ([LangString("a", "b"), LangString("c", "d")], None, "@", None, '["a"@b, "c"@d]\n'),
        ([LangString("a", "b"), LangString("c", "d")], False, "@", None, "[a@b, c@d]\n"),
        ([LangString("a", "b"), LangString("c", "d")], None, "@", False, '["a", "c"]\n'),
        ([LangString("a", "b"), LangString("c", "d")], None, "#", None, '["a"#b, "c"#d]\n'),
        ([LangString("", ""), LangString(" ", " ")], None, "@", None, '[""@, " "@ ]\n'),
        ([LangString("abc", "en"), LangString("ABC", "EN")], None, "@", None, '["abc"@en, "ABC"@EN]\n'),
        ([LangString("hello", "en"), LangString("γειά", "el")], None, "@", None, '["hello"@en, "γειά"@el]\n'),
        ([LangString("hello", "en"), LangString("мир", "ru")], None, "@", None, '["hello"@en, "мир"@ru]\n'),
        ([LangString("emoji", "en"), LangString("😀", "en")], None, "@", None, '["emoji"@en, "😀"@en]\n'),
        ([LangString("special", "en"), LangString("@#$%^&*", "en")], None, "@", None, '["special"@en, "@#$%^&*"@en]\n'),
        ([LangString("a ", "b"), LangString("c", "d")], None, "@", None, '["a "@b, "c"@d]\n'),
        ([LangString("a", "b "), LangString("c", "d")], None, "@", None, '["a"@b , "c"@d]\n'),
        ([LangString("a", "b"), LangString(" c", "d")], None, "@", None, '["a"@b, " c"@d]\n'),
        ([LangString("a", "b"), LangString("c", " d")], None, "@", None, '["a"@b, "c"@ d]\n'),
    ],
)
def test_print_list_parametrized(
    capsys,
    langstring_list: List[LangString],
    print_quotes: Optional[bool],
    separator: str,
    print_lang: Optional[bool],
    expected_output: str,
):
    """
    Parametrized test for LangString.print_list method to ensure it correctly formats and prints a list of LangString objects.

    :param capsys: Pytest fixture to capture system output.
    :type capsys: fixture
    :param langstring_list: List of LangString objects to be printed.
    :type langstring_list: List[LangString]
    :param print_quotes: If True, wrap the text in quotes. If None, use the default setting from the Controller.
    :type print_quotes: Optional[bool]
    :param separator: The separator to use between the text and language tag.
    :type separator: str
    :param print_lang: If True, include the language tag. If None, use the default setting from the Controller.
    :type print_lang: Optional[bool]
    :param expected_output: The expected output string.
    :type expected_output: str
    """
    LangString.print_list(langstring_list, print_quotes, separator, print_lang)
    captured = capsys.readouterr()
    assert (
        captured.out == expected_output
    ), f"Print list failed with print_quotes={print_quotes}, separator='{separator}', print_lang={print_lang}"


def test_print_list_empty_list(capsys):
    """
    Test LangString.print_list with an empty list to ensure it handles empty input correctly.

    :param capsys: Pytest fixture to capture system output.
    :type capsys: fixture
    """
    LangString.print_list([])
    captured = capsys.readouterr()
    assert captured.out == "[]\n", "Print with empty list failed"


def test_print_list_null_elements():
    """
    Test LangString.print_list with null elements in the list to ensure it raises an appropriate error.

    :raises TypeError: If an element in the list is None.
    """
    with pytest.raises(
        TypeError, match="Invalid item with value 'None' in 'list'. Expected one of 'LangString', but got 'NoneType'"
    ):
        LangString.print_list([None])


def test_print_list_invalid_type():
    """
    Test LangString.print_list with invalid type elements in the list to ensure it raises an appropriate error.

    :raises TypeError: If an element in the list is not a LangString.
    """
    with pytest.raises(
        TypeError, match="Invalid item with value 'invalid_type' in 'list'. Expected one of 'LangString', but got 'str'"
    ):
        LangString.print_list(["invalid_type"])


def test_print_list_mixed_types():
    """
    Test LangString.print_list with a mix of valid and invalid types in the list to ensure it raises an appropriate error.

    :raises TypeError: If an element in the list is not a LangString.
    """
    lang_str1 = LangString("hello", "en")
    with pytest.raises(
        TypeError, match="Invalid item with value '123' in 'list'. Expected one of 'LangString', but got 'int'"
    ):
        LangString.print_list([lang_str1, 123])


def test_print_list_self_reference(capsys):
    """
    Test LangString.print_list with a list containing itself to check for self-reference handling.

    :param capsys: Pytest fixture to capture system output.
    :type capsys: fixture
    """
    lang_str1 = LangString("self", "ref")
    ls_list = [lang_str1]
    LangString.print_list(ls_list)
    captured = capsys.readouterr()
    assert captured.out == '["self"@ref]\n', "Print list with self-reference failed"


@pytest.mark.parametrize(
    "langstring_list,print_quotes,separator,print_lang,expected_output",
    [
        ([LangString("a", "b"), LangString("c", "d")], None, "@", None, '["a"@b, "c"@d]\n'),
        ([LangString("", "b"), LangString("c", "d")], None, "@", None, '[""@b, "c"@d]\n'),
        ([LangString("a", ""), LangString("c", "d")], None, "@", None, '["a"@, "c"@d]\n'),
        ([LangString("a", "b"), LangString("c", "d")], None, "@", True, '["a"@b, "c"@d]\n'),
        ([LangString("a", "b"), LangString("c", "d")], None, "@", False, '["a", "c"]\n'),
        ([LangString("a", "b"), LangString("c", "d")], True, "#", True, '["a"#b, "c"#d]\n'),
        ([LangString("ΑΒΓ", "el"), LangString("αβγ", "el")], None, "@", None, '["ΑΒΓ"@el, "αβγ"@el]\n'),
        (
            [LangString("кириллица", "ru"), LangString("КИРИЛЛИЦА", "ru")],
            None,
            "@",
            None,
            '["кириллица"@ru, "КИРИЛЛИЦА"@ru]\n',
        ),
        ([LangString("test", "en"), LangString("テスト", "jp")], None, "@", None, '["test"@en, "テスト"@jp]\n'),
        ([LangString("hello", "en"), LangString("世界", "zh")], None, "@", None, '["hello"@en, "世界"@zh]\n'),
        ([LangString("hello", "en"), LangString("💖", "emoji")], None, "@", None, '["hello"@en, "💖"@emoji]\n'),
        (
            [LangString("special", "en"), LangString("!@#$%^&*()_+", "en")],
            None,
            "@",
            None,
            '["special"@en, "!@#$%^&*()_+"@en]\n',
        ),
        ([LangString(" a", "b"), LangString("c", "d")], None, "@", None, '[" a"@b, "c"@d]\n'),
        ([LangString("a", "b"), LangString(" c", "d")], None, "@", None, '["a"@b, " c"@d]\n'),
        ([LangString("a", "b "), LangString("c", "d")], None, "@", None, '["a"@b , "c"@d]\n'),
        ([LangString("a", "b"), LangString("c", " d")], None, "@", None, '["a"@b, "c"@ d]\n'),
        ([LangString("a ", "b"), LangString("c", "d")], None, "@", None, '["a "@b, "c"@d]\n'),
    ],
)
def test_print_list_parametrized_edge_cases(
    capsys,
    langstring_list: List[LangString],
    print_quotes: Optional[bool],
    separator: str,
    print_lang: Optional[bool],
    expected_output: str,
):
    """
    Parametrized test for LangString.print_list method to ensure it correctly formats and prints a list of LangString objects, including edge cases.

    :param capsys: Pytest fixture to capture system output.
    :type capsys: fixture
    :param langstring_list: List of LangString objects to be printed.
    :type langstring_list: List[LangString]
    :param print_quotes: If True, wrap the text in quotes. If None, use the default setting from the Controller.
    :type print_quotes: Optional[bool]
    :param separator: The separator to use between the text and language tag.
    :type separator: str
    :param print_lang: If True, include the language tag. If None, use the default setting from the Controller.
    :type print_lang: Optional[bool]
    :param expected_output: The expected output string.
    :type expected_output: str
    """
    LangString.print_list(langstring_list, print_quotes, separator, print_lang)
    captured = capsys.readouterr()
    assert (
        captured.out == expected_output
    ), f"Print list failed with print_quotes={print_quotes}, separator='{separator}', print_lang={print_lang}"
