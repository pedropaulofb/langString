"""
The langstring module provides the LangString class to encapsulate a string with its language information.

This module is designed to work with text strings and their associated language tags, offering functionalities
such as validation of language tags, handling of empty strings and language tags based on control flags. It optionally
utilizes the langcodes library for validating language tags, enhancing the robustness of the language tag validation
process.

Control flags from the controller module are used to enforce certain behaviors like ensuring non-empty text and valid
language tags. These flags can be set externally to alter the behavior of the LangString class.

The LangString class aims to make user interaction as similar as possible to working with regular strings. To achieve
this, many of the standard string methods have been overridden to return LangString objects, allowing seamless
integration and extended functionality. Additionally, the class provides mechanisms for validating input types,
matching language tags, and merging LangString objects.

:Example:

    # Create a LangString object
    lang_str = LangString("Hello, World!", "en")

    # Print the string representation
    print(lang_str)  # Output: '"Hello, World!"@en'

    # Convert to uppercase
    upper_lang_str = lang_str.upper()
    print(upper_lang_str)  # Output: '"HELLO, WORLD!"@en'

    # Check if the text contains a substring
    contains_substring = "World" in lang_str
    print(contains_substring)  # Output: True

    # Concatenate two LangString objects
    lang_str2 = LangString(" How are you?", "en")
    combined_lang_str = lang_str + lang_str2
    print(combined_lang_str)  # Output: '"Hello, World! How are you?"@en'

Modules:
    controller: Provides control flags that influence the behavior of the LangString class.
    flags: Defines the LangStringFlag class with various control flags for the LangString class.
    utils.validators: Provides validation methods used within the LangString class.
"""

from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Union


from .controller import Controller
from .flags import LangStringFlag
from .utils.validators import FlagValidator
from .utils.validators import TypeValidator


class LangString:
    """
    A class to encapsulate a string with its language information.

    This class provides functionality to associate a text string with a language tag, offering methods for string
    representation, equality comparison, and hashing. The behavior of this class is influenced by control flags
    from the Controller class, which can enforce non-empty text, valid language tags, and other constraints.

    Many standard string methods are overridden to return LangString objects, allowing seamless integration and
    extended functionality. This design ensures that users can work with LangString instances similarly to regular
    strings.

    :ivar text: The text string.
    :vartype text: Optional[str]
    :ivar lang: The language tag of the text.
    :vartype lang: str
    :raises ValueError: If control flags enforce non-empty text and the text is empty.
    :raises TypeError: If the types of parameters are incorrect based on validation.
    """

    def __init__(self, text: str = "", lang: str = "") -> None:
        """
        Initialize a new LangString object with text and an optional language tag.

        The behavior of this method is influenced by control flags set in the Controller. For instance, if the
        DEFINED_TEXT flag is enabled, an empty 'text' string will raise a ValueError.

        :param text: The text string.
        :type text: str
        :param lang: The language tag of the text.
        :type lang: str
        :raises ValueError: If the DEFINED_TEXT flag is enabled and the text string is empty.
        :raises TypeError: If the provided text or lang is not a string.
        """
        self._text: str = ""
        self._lang: str = ""
        self.text: str = text
        self.lang: str = lang

    # ---------------------------------------------
    # Getters and Setters
    # ---------------------------------------------

    @property
    def text(self) -> str:
        """
        Get the text string.

        :return: The text string.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, new_text: Optional[str]) -> None:
        """
        Set the text string.

        If the provided text is None, it defaults to an empty string.
        This method also validates the type and the text based on control flags.

        :param new_text: The new text string.
        :type new_text: Optional[str]
        :raises TypeError: If the new text is not of type str or None.
        :raises ValueError: If the control flags enforce non-empty text and the new text is empty.
        """
        TypeValidator.validate_type_single(new_text, str, optional=True)
        new_text = new_text or ""
        self._text = FlagValidator.validate_flags_text(LangStringFlag, new_text)

    @property
    def lang(self) -> str:
        """
        Get the language tag.

        :return: The language tag.
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, new_lang: Optional[str]) -> None:
        """
        Set the language tag.

        If the provided language tag is None, it defaults to an empty string. This method also
        validates the type and the language tag based on control flags.

        :param new_lang: The new language tag.
        :type new_lang: Optional[str]
        :raises TypeError: If the new language tag is not of type str or None.
        :raises ValueError: If the control flags enforce valid language tags and the new language tag is invalid.
        """
        TypeValidator.validate_type_single(new_lang, str, optional=True)
        new_lang = new_lang or ""
        self._lang = FlagValidator.validate_flags_lang(LangStringFlag, new_lang)

    # ---------------------------------------------
    # Overwritten String's Built-in Regular Methods
    # ---------------------------------------------

    def capitalize(self) -> "LangString":
        """
        Return a copy of the LangString with its first character capitalized and the rest lowercased.

        This method mimics the behavior of the standard string's capitalize method but returns a LangString object.

        :return: A new LangString with the first character capitalized.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello, world!", "en")
        >>> capitalized_lang_str = lang_str.capitalize()
        >>> print(capitalized_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString(self.text.capitalize(), self.lang)

    def casefold(self) -> "LangString":
        """
        Return a casefolded copy of the LangString. Casefolding is a more aggressive version of lowercasing.

        This method mimics the behavior of the standard string's casefold method but returns a LangString object.

        :return: A new LangString that is casefolded.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, WORLD!", "en")
        >>> casefolded_lang_str = lang_str.casefold()
        >>> print(casefolded_lang_str)  # Output: "hello, world!"@en
        """
        return LangString(self.text.casefold(), self.lang)

    def center(self, width: int, fillchar: str = " ") -> "LangString":
        """
        Return a centered LangString of length width.

        Padding is done using the specified fill character (default is a space).

        This method mimics the behavior of the standard string's center method but returns a LangString object.

        :param width: The total width of the resulting LangString.
        :type width: int
        :param fillchar: The character to fill the padding with.
        :type fillchar: str
        :return: A new LangString centered with padding.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> centered_lang_str = lang_str.center(11, "*")
        >>> print(centered_lang_str)  # Output: "***hello***"@en
        """
        return LangString(self.text.center(width, fillchar), self.lang)

    def count(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the number of non-overlapping occurrences of substring sub in the LangString.

        This method mimics the behavior of the standard string's count method.

        :param sub: The substring to count.
        :type sub: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: The number of occurrences of the substring.
        :rtype: int

        :Example:

        >>> lang_str = LangString("hello, hello, hello!", "en")
        >>> count_hello = lang_str.count("hello")
        >>> print(count_hello)  # Output: 3
        """
        return (self.text).count(sub, start, end)

    def endswith(self, suffix: str, start: int = 0, end: Optional[int] = None) -> bool:
        """
        Return True if the LangString ends with the specified suffix, otherwise return False.

        This method mimics the behavior of the standard string's endswith method.

        :param suffix: The suffix to check.
        :type suffix: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: True if the LangString ends with the suffix, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("hello, world!", "en")
        >>> ends_with_world = lang_str.endswith("world!")
        >>> print(ends_with_world)  # Output: True
        """
        return self.text.endswith(suffix, start, end)

    def expandtabs(self, tabsize: int = 8) -> "LangString":
        r"""
        Return a copy of the LangString where all tab characters are expanded using spaces.

        This method mimics the behavior of the standard string's expandtabs method but returns a LangString object.

        :param tabsize: The number of spaces to use for each tab character.
        :type tabsize: int
        :return: A new LangString with tabs expanded.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello\tworld", "en")
        >>> expanded_lang_str = lang_str.expandtabs(4)
        >>> print(expanded_lang_str)  # Output: "hello   world"@en
        """
        return LangString(self.text.expandtabs(tabsize), self.lang)

    def find(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the lowest index in the LangString where substring sub is found.

        This method mimics the behavior of the standard string's find method.

        :param sub: The substring to find.
        :type sub: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: The lowest index where the substring is found, or -1 if not found.
        :rtype: int

        :Example:

        >>> lang_str = LangString("hello, world", "en")
        >>> index = lang_str.find("world")
        >>> print(index)  # Output: 7
        """
        return self.text.find(sub, start, end)

    def format(self, *args: Any, **kwargs: Any) -> "LangString":
        """
        Perform a string formatting operation on the LangString.

        This method mimics the behavior of the standard string's format method but returns a LangString object.

        :param args: Positional arguments for formatting.
        :type args: Any
        :param kwargs: Keyword arguments for formatting.
        :type kwargs: Any
        :return: A new LangString with the formatted text.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, {}!", "en")
        >>> formatted_lang_str = lang_str.format("world")
        >>> print(formatted_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString(self.text.format(*args, **kwargs), self.lang)

    def format_map(self, mapping: dict[Any, Any]) -> "LangString":
        """
        Perform a string formatting operation using a dictionary.

        This method mimics the behavior of the standard string's format_map method but returns a LangString object.

        :param mapping: A dictionary for formatting.
        :type mapping: dict
        :return: A new LangString with the formatted text.
        :rtype: LangString
        :raises TypeError: If the provided mapping is not a dictionary.

        :Example:

        >>> lang_str = LangString("Hello, {name}!", "en")
        >>> formatted_lang_str = lang_str.format_map({"name": "world"})
        >>> print(formatted_lang_str)  # Output: "Hello, world!"@en
        """
        TypeValidator.validate_type_single(mapping, dict)

        return LangString(self.text.format_map(mapping), self.lang)

    def index(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the lowest index in the LangString where substring sub is found.

        This method mimics the behavior of the standard string's index method.

        :param sub: The substring to find.
        :type sub: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: The lowest index where the substring is found.
        :rtype: int
        :raises ValueError: If the substring is not found.

        :Example:

        >>> lang_str = LangString("hello, world", "en")
        >>> index = lang_str.index("world")
        >>> print(index)  # Output: 7
        """
        return self.text.index(sub, start, end)

    def isalnum(self) -> bool:
        """
        Return True if all characters in the LangString are alphanumeric and there is at least one character.

        This method mimics the behavior of the standard string's isalnum method.

        :return: True if the LangString is alphanumeric, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello123", "en")
        >>> is_alnum = lang_str.isalnum()
        >>> print(is_alnum)  # Output: True

        >>> lang_str = LangString("Hello 123", "en")
        >>> is_alnum = lang_str.isalnum()
        >>> print(is_alnum)  # Output: False
        """
        return (self.text).isalnum()

    def isalpha(self) -> bool:
        """
        Return True if all characters in the LangString are alphabetic and there is at least one character.

        This method mimics the behavior of the standard string's isalpha method.

        :return: True if the LangString is alphabetic, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello", "en")
        >>> is_alpha = lang_str.isalpha()
        >>> print(is_alpha)  # Output: True

        >>> lang_str = LangString("Hello123", "en")
        >>> is_alpha = lang_str.isalpha()
        >>> print(is_alpha)  # Output: False
        """
        return (self.text).isalpha()

    def isascii(self) -> bool:
        """
        Return True if all characters in the LangString are ASCII characters.

        This method mimics the behavior of the standard string's isascii method.

        :return: True if the LangString is ASCII, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello", "en")
        >>> is_ascii = lang_str.isascii()
        >>> print(is_ascii)  # Output: True

        >>> lang_str = LangString("Héllo", "en")
        >>> is_ascii = lang_str.isascii()
        >>> print(is_ascii)  # Output: False
        """
        return (self.text).isascii()

    def isdecimal(self) -> bool:
        """
        Return True if all characters in the LangString are decimal characters and there is at least one character.

        This method mimics the behavior of the standard string's isdecimal method.

        :return: True if the LangString is decimal, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("12345", "en")
        >>> is_decimal = lang_str.isdecimal()
        >>> print(is_decimal)  # Output: True

        >>> lang_str = LangString("123.45", "en")
        >>> is_decimal = lang_str.isdecimal()
        >>> print(is_decimal)  # Output: False
        """
        return (self.text).isdecimal()

    def isdigit(self) -> bool:
        """
        Return True if all characters in the LangString are digits and there is at least one character.

        This method mimics the behavior of the standard string's isdigit method.

        :return: True if the LangString is numeric, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("12345", "en")
        >>> is_digit = lang_str.isdigit()
        >>> print(is_digit)  # Output: True

        >>> lang_str = LangString("123.45", "en")
        >>> is_digit = lang_str.isdigit()
        >>> print(is_digit)  # Output: False
        """
        return (self.text).isdigit()

    def isidentifier(self) -> bool:
        """
        Return True if the LangString is a valid identifier according to Python language definition.

        This method mimics the behavior of the standard string's isidentifier method.

        :return: True if the LangString is a valid identifier, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("variable_name", "en")
        >>> is_identifier = lang_str.isidentifier()
        >>> print(is_identifier)  # Output: True

        >>> lang_str = LangString("123variable", "en")
        >>> is_identifier = lang_str.isidentifier()
        >>> print(is_identifier)  # Output: False
        """
        return (self.text).isidentifier()

    def islower(self) -> bool:
        """
        Return True if all cased characters in the LangString are lowercase and there is at least one cased character.

        This method mimics the behavior of the standard string's islower method.

        :return: True if the LangString is in lowercase, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> is_lower = lang_str.islower()
        >>> print(is_lower)  # Output: True

        >>> lang_str = LangString("Hello", "en")
        >>> is_lower = lang_str.islower()
        >>> print(is_lower)  # Output: False
        """
        return (self.text).islower()

    def isnumeric(self) -> bool:
        """
        Return True if all characters in the LangString are numeric characters and there is at least one character.

        This method mimics the behavior of the standard string's isnumeric method.

        :return: True if the LangString is numeric, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("12345", "en")
        >>> is_numeric = lang_str.isnumeric()
        >>> print(is_numeric)  # Output: True

        >>> lang_str = LangString("123.45", "en")
        >>> is_numeric = lang_str.isnumeric()
        >>> print(is_numeric)  # Output: False
        """
        return (self.text).isnumeric()

    def isprintable(self) -> bool:
        r"""
        Return True if all characters in the LangString are printable or the LangString is empty.

        This method mimics the behavior of the standard string's isprintable method.

        :return: True if the LangString is printable, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> is_printable = lang_str.isprintable()
        >>> print(is_printable)  # Output: True

        >>> lang_str = LangString("Hello,\tworld!", "en")
        >>> is_printable = lang_str.isprintable()
        >>> print(is_printable)  # Output: False
        """
        return (self.text).isprintable()

    def isspace(self) -> bool:
        """
        Return True if there are only whitespace characters in the LangString and there is at least one character.

        This method mimics the behavior of the standard string's isspace method.

        :return: True if the LangString is whitespace, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("   ", "en")
        >>> is_space = lang_str.isspace()
        >>> print(is_space)  # Output: True

        >>> lang_str = LangString("Hello, world!", "en")
        >>> is_space = lang_str.isspace()
        >>> print(is_space)  # Output: False
        """
        return (self.text).isspace()

    def istitle(self) -> bool:
        """
        Return True if the LangString is a titlecased string and there is at least one character.

        This method mimics the behavior of the standard string's istitle method.

        :return: True if the LangString is titlecased, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello, World!", "en")
        >>> is_title = lang_str.istitle()
        >>> print(is_title)  # Output: True

        >>> lang_str = LangString("hello, world!", "en")
        >>> is_title = lang_str.istitle()
        >>> print(is_title)  # Output: False
        """
        return (self.text).istitle()

    def isupper(self) -> bool:
        """
        Return True if all cased characters in the LangString are uppercase and there is at least one cased character.

        This method mimics the behavior of the standard string's isupper method.

        :return: True if the LangString is in uppercase, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("HELLO, WORLD!", "en")
        >>> is_upper = lang_str.isupper()
        >>> print(is_upper)  # Output: True

        >>> lang_str = LangString("Hello, World!", "en")
        >>> is_upper = lang_str.isupper()
        >>> print(is_upper)  # Output: False
        """
        return (self.text).isupper()

    def join(self, iterable: Iterable[str]) -> "LangString":
        """
        Join an iterable of strings with the LangString's text.

        This method mimics the behavior of the standard string's join method but returns a LangString object.

        :param iterable: An iterable of strings to be joined.
        :type iterable: Iterable[str]
        :return: A new LangString with the joined text.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString(", ", "en")
        >>> joined_lang_str = lang_str.join(["Hello", "world"])
        >>> print(joined_lang_str)  # Output: "Hello, world"@en
        """
        joined_text = self.text.join(iterable)
        return LangString(joined_text, self.lang)

    def ljust(self, width: int, fillchar: str = " ") -> "LangString":
        """
        Return a left-justified LangString of length width.

        Padding is done using the specified fill character (default is a space).

        This method mimics the behavior of the standard string's ljust method but returns a LangString object.

        :param width: The total width of the resulting LangString.
        :type width: int
        :param fillchar: The character to fill the padding with.
        :type fillchar: str
        :return: A new LangString left-justified with padding.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> left_justified_lang_str = lang_str.ljust(10, "*")
        >>> print(left_justified_lang_str)  # Output: "hello*****"@en
        """
        justified_text = self.text.ljust(width, fillchar)
        return LangString(justified_text, self.lang)

    def lower(self) -> "LangString":
        """
        Return a copy of the LangString with all the cased characters converted to lowercase.

        This method mimics the behavior of the standard string's lower method but returns a LangString object.

        :return: A new LangString with all characters in lowercase.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("HELLO, WORLD!", "en")
        >>> lower_lang_str = lang_str.lower()
        >>> print(lower_lang_str)  # Output: "hello, world!"@en
        """
        return LangString(self.text.lower(), self.lang)

    def lstrip(self, chars: Optional[str] = None) -> "LangString":
        """
        Return a copy of the LangString with leading characters removed.

        This method mimics the behavior of the standard string's lstrip method but returns a LangString object.

        :param chars: A string specifying the set of characters to be removed.
        If None, whitespace characters are removed.
        :type chars: Optional[str]
        :return: A new LangString with leading characters removed.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("   Hello, world!", "en")
        >>> stripped_lang_str = lang_str.lstrip()
        >>> print(stripped_lang_str)  # Output: "Hello, world!"@en

        >>> lang_str = LangString("...Hello, world!", "en")
        >>> stripped_lang_str = lang_str.lstrip(".")
        >>> print(stripped_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString(self.text.lstrip(chars), self.lang)

    def partition(self, sep: str) -> tuple["LangString", "LangString", "LangString"]:
        """
        Split the LangString at the first occurrence of sep, and return a 3-tuple containing the part \
        before the separator, the separator itself, and the part after the separator.

        This method mimics the behavior of the standard string's partition method but returns LangString objects.

        :param sep: The separator to split the LangString.
        :type sep: str
        :return: A 3-tuple containing the part before the separator, the separator itself,
                 and the part after the separator.
        :rtype: tuple[LangString, LangString, LangString]

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> before, sep, after = lang_str.partition(", ")
        >>> print(before)  # Output: "Hello"@en
        >>> print(sep)     # Output: ", "@en
        >>> print(after)   # Output: "world!"@en
        """
        before, sep, after = self.text.partition(sep)
        return LangString(before, self.lang), LangString(sep, self.lang), LangString(after, self.lang)

    def replace(self, old: str, new: str, count: int = -1) -> "LangString":
        """
        Return a copy of the LangString with all occurrences of substring old replaced by new.

        This method mimics the behavior of the standard string's replace method but returns a LangString object.

        :param old: The substring to be replaced.
        :type old: str
        :param new: The substring to replace with.
        :type new: str
        :param count: The maximum number of occurrences to replace. If -1, all occurrences are replaced.
        :type count: int
        :return: A new LangString with the replacements.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> replaced_lang_str = lang_str.replace("world", "Python")
        >>> print(replaced_lang_str)  # Output: "Hello, Python!"@en

        >>> lang_str = LangString("abababab", "en")
        >>> replaced_lang_str = lang_str.replace("ab", "cd", 2)
        >>> print(replaced_lang_str)  # Output: "cdcdabab"@en
        """
        return LangString(self.text.replace(old, new, count), self.lang)

    def removeprefix(self, prefix: str) -> "LangString":
        """
        Remove the specified prefix from the LangString's text.

        If the text starts with the prefix string, return a new LangString with the prefix string removed.
        Otherwise, return a copy of the original LangString.

        This method mimics the behavior of the standard string's removeprefix method but returns a LangString object.

        :param prefix: The prefix to remove from the text.
        :type prefix: str
        :return: A new LangString with the prefix removed, or the original LangString if the prefix is not found.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> removed_prefix_lang_str = lang_str.removeprefix("Hello, ")
        >>> print(removed_prefix_lang_str)  # Output: "world!"@en

        >>> lang_str = LangString("Hello, world!", "en")
        >>> removed_prefix_lang_str = lang_str.removeprefix("Goodbye, ")
        >>> print(removed_prefix_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString((self.text).removeprefix(prefix), self.lang)

    def removesuffix(self, suffix: str) -> "LangString":
        """
        Remove the specified suffix from the LangString's text.

        If the text ends with the suffix string, return a new LangString with the suffix string removed.
        Otherwise, return a copy of the original LangString.

        This method mimics the behavior of the standard string's removesuffix method but returns a LangString object.

        :param suffix: The suffix to remove from the text.
        :type suffix: str
        :return: A new LangString with the suffix removed, or the original LangString if the suffix is not found.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> removed_suffix_lang_str = lang_str.removesuffix(", world!")
        >>> print(removed_suffix_lang_str)  # Output: "Hello"@en

        >>> lang_str = LangString("Hello, world!", "en")
        >>> removed_suffix_lang_str = lang_str.removesuffix("planet")
        >>> print(removed_suffix_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString((self.text).removesuffix(suffix), self.lang)

    def rfind(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the highest index in the LangString where substring sub is found, such that sub is contained within \
        [start, end].

        Optional arguments start and end are interpreted as in slice notation. Return -1 if sub is
        not found.

        This method mimics the behavior of the standard string's rfind method.

        :param sub: The substring to find.
        :type sub: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: The highest index where the substring is found, or -1 if not found.
        :rtype: int

        :Example:

        >>> lang_str = LangString("Hello, world! Hello, universe!", "en")
        >>> index = lang_str.rfind("Hello")
        >>> print(index)  # Output: 14
        """
        return self.text.rfind(sub, start, end)

    def rindex(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the highest index in the LangString where substring sub is found, such that sub is contained within \
        [start, end].

        Optional arguments start and end are interpreted as in slice notation. Raises ValueError when
        the substring is not found.

        This method mimics the behavior of the standard string's rindex method.

        :param sub: The substring to find.
        :type sub: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: The highest index where the substring is found.
        :rtype: int
        :raises ValueError: If the substring is not found.

        :Example:

        >>> lang_str = LangString("Hello, world! Hello, universe!", "en")
        >>> index = lang_str.rindex("Hello")
        >>> print(index)  # Output: 14

        >>> lang_str = LangString("Hello, world!", "en")
        >>> index = lang_str.rindex("Hi")
        >>> print(index)  # Output: ValueError
        """
        return self.text.rindex(sub, start, end)

    def rjust(self, width: int, fillchar: str = " ") -> "LangString":
        """
        Return a right-justified LangString of length width.

        Padding is done using the specified fill character (default is a space).

        This method mimics the behavior of the standard string's rjust method but returns a LangString object.

        :param width: The total width of the resulting LangString.
        :type width: int
        :param fillchar: The character to fill the padding with.
        :type fillchar: str
        :return: A new LangString right-justified with padding.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> right_justified_lang_str = lang_str.rjust(10, "*")
        >>> print(right_justified_lang_str)  # Output: "*****hello"@en
        """
        justified_text = self.text.rjust(width, fillchar)
        return LangString(justified_text, self.lang)

    def rpartition(self, sep: str) -> tuple["LangString", "LangString", "LangString"]:
        """
        Split the LangString at the last occurrence of sep, and return a 3-tuple containing the \
        part before the separator, the separator itself, and the part after the separator.

        This method mimics the behavior of the standard string's rpartition method but returns LangString objects.

        :param sep: The separator to split the LangString.
        :type sep: str
        :return: A 3-tuple containing the part before the separator, the separator itself,
                 and the part after the separator.
        :rtype: tuple[LangString, LangString, LangString]

        :Example:

        >>> lang_str = LangString("Hello, world! Hello, universe!", "en")
        >>> before, sep, after = lang_str.rpartition("Hello")
        >>> print(before)  # Output: "Hello, world! "@en
        >>> print(sep)     # Output: "Hello"@en
        >>> print(after)   # Output: ", universe!"@en
        """
        before, sep, after = self.text.rpartition(sep)
        return LangString(before, self.lang), LangString(sep, self.lang), LangString(after, self.lang)

    def rsplit(self, sep: Optional[str] = None, maxsplit: int = -1) -> list["LangString"]:
        """
        Return a list of the words in the LangString, using sep as the delimiter string.

        The list is split from the right starting from the end of the string.

        This method mimics the behavior of the standard string's rsplit method but returns a list of LangString objects.

        :param sep: The delimiter string. If None, any whitespace string is a separator.
        :type sep: Optional[str]
        :param maxsplit: Maximum number of splits. If -1, there is no limit.
        :type maxsplit: int
        :return: A list of LangString objects.
        :rtype: list[LangString]

        :Example:

        >>> lang_str = LangString("one two three", "en")
        >>> split_lang_str = lang_str.rsplit()
        >>> for part in split_lang_str:
        ...     print(part)
        ...
        >>> # Output: "one"@en
        >>> #         "two"@en
        >>> #         "three"@en

        >>> lang_str = LangString("one,two,three", "en")
        >>> split_lang_str = lang_str.rsplit(",", 1)
        >>> for part in split_lang_str:
        ...     print(part)
        ...
        >>> # Output: "one,two"@en
        >>> #         "three"@en
        """
        split_texts = self.text.rsplit(sep, maxsplit)
        return [LangString(part, self.lang) for part in split_texts]

    def rstrip(self, chars: Optional[str] = None) -> "LangString":
        """
        Return a copy of the LangString with trailing characters removed.

        This method mimics the behavior of the standard string's rstrip method but returns a LangString object.

        :param chars: A string specifying the set of characters to be removed.
                      If None, whitespace characters are removed.
        :type chars: Optional[str]
        :return: A new LangString with trailing characters removed.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, world!   ", "en")
        >>> stripped_lang_str = lang_str.rstrip()
        >>> print(stripped_lang_str)  # Output: "Hello, world!"@en

        >>> lang_str = LangString("Hello, world!!!", "en")
        >>> stripped_lang_str = lang_str.rstrip("!")
        >>> print(stripped_lang_str)  # Output: "Hello, world"@en
        """
        return LangString(self.text.rstrip(chars), self.lang)

    def split(self, sep: Optional[str] = None, maxsplit: int = -1) -> list["LangString"]:
        """
        Return a list of the words in the LangString, using sep as the delimiter string.

        This method mimics the behavior of the standard string's split method but returns a list of LangString objects.

        :param sep: The delimiter string. If None, any whitespace string is a separator.
        :type sep: Optional[str]
        :param maxsplit: Maximum number of splits. If -1, there is no limit.
        :type maxsplit: int
        :return: A list of LangString objects.
        :rtype: list[LangString]

        :Example:

        >>> lang_str = LangString("one two three", "en")
        >>> split_lang_str = lang_str.split()
        >>> for part in split_lang_str:
        ...     print(part)
        ...
        >>> # Output: "one"@en
        >>> #         "two"@en
        >>> #         "three"@en

        >>> lang_str = LangString("one,two,three", "en")
        >>> split_lang_str = lang_str.split(",")
        >>> for part in split_lang_str:
        ...     print(part)
        ...
        >>> # Output: "one"@en
        >>> #         "two"@en
        >>> #         "three"@en
        """
        split_texts = self.text.split(sep, maxsplit)
        return [LangString(part, self.lang) for part in split_texts]

    @TypeValidator.validate_type_decorator
    def splitlines(self, keepends: bool = False) -> list["LangString"]:
        r"""
        Return a list of the lines in the LangString, breaking at line boundaries.

        This method mimics the behavior of the standard string's splitlines method but returns
        a list of LangString objects.

        :param keepends: If True, line breaks are included in the resulting list.
        :type keepends: bool
        :return: A list of LangString objects.
        :rtype: list[LangString]

        :Example:

        >>> lang_str = LangString("Hello\\nworld", "en") # For the test, remove one escape char before the line break.
        >>> split_lang_str = lang_str.splitlines()
        >>> print(split_lang_str)
        # Output:
        # [LangString(text='Hello', lang='en'), LangString(text='world', lang='en')]

        >>> lang_str = LangString("Hello\\nworld", "en") # For the test, remove one escape char before the line break.
        >>> split_lang_str = lang_str.splitlines(True)
        >>> print(split_lang_str)
        # Output:
        # [LangString(text='Hello\n', lang='en'), LangString(text='world', lang='en')]
        """
        lines = self.text.splitlines(keepends)
        return [LangString(line, self.lang) for line in lines]

    def startswith(self, prefix: str, start: int = 0, end: Optional[int] = None) -> bool:
        """
        Return True if the LangString starts with the specified prefix, otherwise return False.

        This method mimics the behavior of the standard string's startswith method.

        :param prefix: The prefix to check.
        :type prefix: str
        :param start: The starting position (default is 0).
        :type start: int, optional
        :param end: The ending position (default is the end of the string).
        :type end: int, optional
        :return: True if the LangString starts with the prefix, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello, world!", "en")
        >>> starts_with_hello = lang_str.startswith("Hello")
        >>> print(starts_with_hello)  # Output: True

        >>> lang_str = LangString("Hello, world!", "en")
        >>> starts_with_hello = lang_str.startswith("world")
        >>> print(starts_with_hello)  # Output: False
        """
        return self.text.startswith(prefix, start, end)

    def strip(self, chars: Optional[str] = None) -> "LangString":
        """
        Return a copy of the LangString with leading and trailing characters removed.

        This method mimics the behavior of the standard string's strip method but returns a LangString object.

        :param chars: A string specifying the set of characters to be removed.
                      If None, whitespace characters are removed.
        :type chars: Optional[str]
        :return: A new LangString with leading and trailing characters removed.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("   Hello, world!   ", "en")
        >>> stripped_lang_str = lang_str.strip()
        >>> print(stripped_lang_str)  # Output: "Hello, world!"@en

        >>> lang_str = LangString("***Hello, world!***", "en")
        >>> stripped_lang_str = lang_str.strip("*")
        >>> print(stripped_lang_str)  # Output: "Hello, world!"@en
        """
        return LangString(self.text.strip(chars), self.lang)

    def swapcase(self) -> "LangString":
        """
        Return a copy of the LangString with uppercase characters converted to lowercase and vice versa.

        This method mimics the behavior of the standard string's swapcase method but returns a LangString object.

        :return: A new LangString with swapped case.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("Hello, WORLD!", "en")
        >>> swapcase_lang_str = lang_str.swapcase()
        >>> print(swapcase_lang_str)  # Output: "hELLO, world!"@en
        """
        return LangString(self.text.swapcase(), self.lang)

    def title(self) -> "LangString":
        """
        Return a titlecased version of the LangString where words start with an uppercase character and the remaining \
        characters are lowercase.

        This method mimics the behavior of the standard string's title method but returns a LangString object.

        :return: A new LangString that is titlecased.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello world", "en")
        >>> title_lang_str = lang_str.title()
        >>> print(title_lang_str)  # Output: "Hello World"@en
        """
        return LangString(self.text.title(), self.lang)

    def translate(self, table: dict[int, str]) -> "LangString":
        """
        Return a copy of the LangString in which each character has been mapped through the given translation table.

        This method mimics the behavior of the standard string's translate method but returns a LangString object.

        :param table: A translation table mapping Unicode ordinals to Unicode ordinals, strings, or None.
        :type table: dict[int, str]
        :return: A new LangString with the characters translated.
        :rtype: LangString

        :Example:

        >>> translation_table = str.maketrans("aeiou", "12345")
        >>> lang_str = LangString("hello world", "en")
        >>> translated_lang_str = lang_str.translate(translation_table)
        >>> print(translated_lang_str) # Output: "h2ll4 w4rld"@en
        """
        return LangString(self.text.translate(table), self.lang)

    def upper(self) -> "LangString":
        """
        Return a copy of the LangString with all the characters converted to uppercase.

        This method mimics the behavior of the standard string's upper method but returns a LangString object.

        :return: A new LangString with all characters in uppercase.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello world", "en")
        >>> upper_lang_str = lang_str.upper()
        >>> print(upper_lang_str)  # Output: "HELLO WORLD"@en
        """
        return LangString(self.text.upper(), self.lang)

    def zfill(self, width: int) -> "LangString":
        """
        Return a copy of the LangString left filled with ASCII '0' digits to make a string of length width.

        This method mimics the behavior of the standard string's zfill method but returns a LangString object.

        :param width: The total width of the resulting LangString.
        :type width: int
        :return: A new LangString left filled with '0' digits.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("42", "en")
        >>> zfilled_lang_str = lang_str.zfill(5)
        >>> print(zfilled_lang_str)  # Output: "00042"@en
        """
        return LangString(self.text.zfill(width), self.lang)

    # ---------------------------------------------
    # LangString's Regular Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    def to_string(
        self, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None
    ) -> str:
        """
        Return a string representation of the LangString with options for including quotes and language tag.

        :param print_quotes: If True, wrap the text in quotes. If None, use the default setting from the Controller.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between the text and language tag.
        :type separator: str
        :param print_lang: If True, include the language tag. If None, use the default setting from the Controller.
        :type print_lang: Optional[bool]
        :return: A string representation of the LangString.
        :rtype: str

        :Example:

        >>> lang_str = LangString("Hello, World!", "en")
        >>> print(lang_str.to_string())  # Output: '"Hello, World!"@en'
        >>> print(lang_str.to_string(print_quotes=False))  # Output: 'Hello, World!@en'
        >>> print(lang_str.to_string(print_lang=False))  # Output: '"Hello, World!"'
        """
        if print_quotes is None:
            # Get the default setting for print_quotes from the Controller
            print_quotes = Controller.get_flag(LangStringFlag.PRINT_WITH_QUOTES)
        if print_lang is None:
            # Get the default setting for print_lang from the Controller
            print_lang = Controller.get_flag(LangStringFlag.PRINT_WITH_LANG)

        # Wrap text in quotes if print_quotes is True
        text_value: str = f'"{self.text}"' if print_quotes else f"{self.text}"
        # Append the language tag if print_lang is True
        lang_value: str = f"{separator}{self.lang}" if print_lang else ""

        return text_value + lang_value

    @TypeValidator.validate_type_decorator
    def equals_str(self, other: str) -> bool:
        """
        Compare the LangString's text with a given string for equality.

        :param other: The string to compare with.
        :type other: str
        :return: True if the text matches the given string, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello, World!", "en")
        >>> print(lang_str.equals_str("Hello, World!"))  # Output: True
        >>> print(lang_str.equals_str("hello, world!"))  # Output: False
        """
        return self.text == other

    @TypeValidator.validate_type_decorator
    def equals_langstring(self, other: "LangString") -> bool:
        """
        Compare the LangString with another LangString for equality of text and language tag (case-insensitive).

        :param other: The LangString to compare with.
        :type other: LangString
        :return: True if both text and language tag match (case-insensitive), otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str1 = LangString("Hello, World!", "en")
        >>> lang_str2 = LangString("Hello, World!", "EN")
        >>> print(lang_str1.equals_langstring(lang_str2))  # Output: True
        >>> lang_str3 = LangString("Hello, World!", "fr")
        >>> print(lang_str1.equals_langstring(lang_str3))  # Output: False
        """
        return self.text == other.text and self.lang.casefold() == other.lang.casefold()

    # ---------------------------------------------
    # Overwritten String's Built-in Dunder Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    def __add__(self, other: Union["LangString", str]) -> "LangString":
        """
        Add another LangString or a string to this LangString.

        The operation can only be performed if:
        - Both are LangString objects with the same language tag.
        - The other is a string, which will be concatenated to the text of this LangString.

        :param other: The LangString or string to add.
        :type other: Union[LangString, str]
        :return: A new LangString with the concatenated text.
        :rtype: LangString
        :raises TypeError: If the objects are not compatible for addition.

        :Example:

        >>> lang_str1 = LangString("Hello", "en")
        >>> lang_str2 = LangString(" World", "en")
        >>> result = lang_str1 + lang_str2
        >>> print(result)  # Output: "Hello World"@en

        >>> lang_str3 = LangString("Hello", "en")
        >>> result = lang_str3 + " World"
        >>> print(result)  # Output: "Hello World"@en
        """
        self._validate_match_types(other)
        self._validate_match_langs(other)

        if isinstance(other, LangString):
            return LangString(self.text + other.text, self.lang)

        # No need to check 'isinstance(other, str)' as type validation assures that
        return LangString(self.text + other, self.lang)

    @TypeValidator.validate_type_decorator
    def __contains__(self, item: str) -> bool:
        """
        Check if a substring exists within the LangString's text.

        :param item: The substring to check.
        :type item: str
        :return: True if the substring exists within the text, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str = LangString("Hello, World!", "en")
        >>> contains = "World" in lang_str
        >>> print(contains)  # Output: True

        >>> contains = "Python" in lang_str
        >>> print(contains)  # Output: False
        """
        return item in self.text

    def __eq__(self, other: object) -> bool:
        """
        Check equality of this LangString with another object.

        :param other: Another object to compare with.
        :type other: object
        :return: True if the objects are equal, otherwise False.
        :rtype: bool

        :Example:

        >>> lang_str1 = LangString("Hello, World!", "en")
        >>> lang_str2 = LangString("Hello, World!", "en")
        >>> is_equal = lang_str1 == lang_str2
        >>> print(is_equal)  # Output: True

        >>> lang_str3 = LangString("Hello, World!", "fr")
        >>> is_equal = lang_str1 == lang_str3
        >>> print(is_equal)  # Output: False

        >>> is_equal = lang_str1 == "Hello, World!"
        >>> print(is_equal)  # Output: True

        >>> is_equal = lang_str1 == "Bonjour, Monde!"
        >>> print(is_equal)  # Output: False
        """
        self._validate_match_types(other)

        if isinstance(other, str):
            return self.text == other
        if isinstance(other, LangString):
            return self.text == other.text and self.lang.casefold() == other.lang.casefold()
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """
        Check if this LangString is greater than or equal to another str or LangString object.

        :param other: The str or LangString object to compare with.
        :type other: object
        :return: True if this LangString is greater than or equal to the other, otherwise False.
        :rtype: bool
        :raises TypeError: If the objects are not compatible for comparison.
        :raises ValueError: If the language tags are incompatible.

        :Example:

        >>> lang_str1 = LangString("banana", "en")
        >>> lang_str2 = LangString("apple", "en")
        >>> is_ge = lang_str1 >= lang_str2
        >>> print(is_ge)  # Output: True

        >>> lang_str3 = LangString("apple", "en")
        >>> is_ge = lang_str2 >= lang_str3
        >>> print(is_ge)  # Output: True

        >>> is_ge = lang_str1 >= "banana"
        >>> print(is_ge)  # Output: True

        >>> is_ge = lang_str2 >= "cherry"
        >>> print(is_ge)  # Output: False
        """
        self._validate_match_langs(other)  # remove diff langs
        self._validate_match_types(other)  # case strict is true, remove str

        if isinstance(other, str):
            return self.text >= other
        if isinstance(other, LangString):
            return self.text >= other.text
        return NotImplemented

    def __getitem__(self, key: Union[int, slice]) -> "LangString":
        """
        Retrieve a substring or a reversed string from the LangString's text.

        :param key: The index or slice to access.
        :type key: Union[int, slice]
        :return: A new LangString with the substring or single character.
        :rtype: LangString

        :Example:

        >>> lang_str = LangString("hello, world", "en")
        >>> substring = lang_str[0:5]
        >>> print(substring)  # Output: "hello"@en

        >>> single_char = lang_str[1]
        >>> print(single_char)  # Output: "e"@en
        """
        if isinstance(key, slice):
            # Handle slicing
            sliced_text = self.text[key]
            return LangString(sliced_text, self.lang)

        # Handle single index access
        return LangString(self.text[key], self.lang)

    def __gt__(self, other: object) -> bool:
        """
        Check if this LangString is greater than another LangString object.

        :param other: The str or LangString object to compare with.
        :type other: object
        :return: True if this LangString is greater than the other, otherwise False.
        :rtype: bool
        :raises TypeError: If the objects are not compatible for comparison.
        :raises ValueError: If the language tags are incompatible.

        :Example:

        >>> lang_str1 = LangString("banana", "en")
        >>> lang_str2 = LangString("apple", "en")
        >>> is_gt = lang_str1 > lang_str2
        >>> print(is_gt)  # Output: True

        >>> lang_str3 = LangString("apple", "en")
        >>> is_gt = lang_str2 > lang_str3
        >>> print(is_gt)  # Output: False

        >>> is_gt = lang_str1 > "apple"
        >>> print(is_gt)  # Output: True

        >>> is_gt = lang_str2 > "cherry"
        >>> print(is_gt)  # Output: False
        """
        self._validate_match_langs(other)
        self._validate_match_types(other)

        if isinstance(other, str):
            return self.text > other
        if isinstance(other, LangString):
            return self.text > other.text
        return NotImplemented

    def __hash__(self) -> int:
        """
        Generate a hash value for a LangString object.

        The hash value is computed based on the text and a casefolded version of the language tag.

        :return: The hash value of the LangString object, based on its text and language tag.
        :rtype: int

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> hash_value = hash(lang_str)
        >>> print(hash_value)  # Output: A unique integer representing the hash value
        """
        return hash((self.text, self.lang.casefold()))

    @TypeValidator.validate_type_decorator
    def __iadd__(self, other: Union["LangString", str]) -> "LangString":
        """
        Implement in-place addition for LangString objects.

        This method allows the LangString's text to be concatenated with another LangString's text or a regular string.
        The operation is only allowed if both LangString objects have the same language tag or if the other operand
        is a string.

        :param other: The LangString or string to add.
        :type other: Union[LangString, str]
        :return: A new LangString instance with the concatenated text.
        :rtype: LangString
        :raises TypeError: If the objects are not compatible for addition.
        :raises ValueError: If the language tags are incompatible.

        :Example:

        >>> lang_str1 = LangString("Hello", "en")
        >>> lang_str2 = LangString(" World", "en")
        >>> lang_str1 += lang_str2
        >>> print(lang_str1)  # Output: "Hello World"@en

        >>> lang_str1 += "!"
        >>> print(lang_str1)  # Output: "Hello World!"@en
        """
        return self + other

    @TypeValidator.validate_type_decorator
    def __imul__(self, other: int) -> "LangString":
        """
        Implement in-place multiplication of the LangString's text.

        This method allows the LangString's text to be repeated a specified number of times.

        :param other: The number of times to repeat the text.
        :type other: int
        :return: The same LangString instance with the text repeated.
        :rtype: LangString
        :raises TypeError: If the operand is not an integer.

        :Example:

        >>> lang_str = LangString("Hello", "en")
        >>> lang_str *= 3
        >>> print(lang_str)  # Output: "HelloHelloHello"@en
        """
        self.text *= other
        return self

    def __iter__(self) -> Iterator[str]:
        """
        Enable iteration over the text part of the LangString.

        This method allows the LangString to be iterable, returning each character in the text part one by one.

        :return: An iterator over the characters in the text.
        :rtype: Iterator[str]

        :Example:

        >>> lang_str = LangString("Hello", "en")
        >>> for char in lang_str:
        ...     print(char)
        ...
        # Output:   H
        #           e
        #           l
        #           l
        #           o
        """
        return iter(self.text)

    def __le__(self, other: object) -> bool:
        """
        Check if this LangString is less than or equal to another LangString object or string.

        This method compares the LangString's text with another LangString's text or a regular string.

        :param other: The LangString or string to compare with.
        :type other: object
        :return: True if this LangString's text is less than or equal to the other text, otherwise False.
        :rtype: bool
        :raises TypeError: If the objects are not compatible for comparison.
        :raises ValueError: If the language tags are incompatible.

        :Example:

        >>> lang_str1 = LangString("apple", "en")
        >>> lang_str2 = LangString("banana", "en")
        >>> print(lang_str1 <= lang_str2)  # Output: True
        >>> print(lang_str1 <= "apple")  # Output: True
        """
        self._validate_match_langs(other)
        self._validate_match_types(other)

        if isinstance(other, str):
            return self.text <= other
        if isinstance(other, LangString):
            return self.text <= other.text
        return NotImplemented

    def __len__(self) -> int:
        """
        Return the length of the LangString's text.

        :return: The length of the text.
        :rtype: int

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> length = len(lang_str)
        >>> print(length)  # Output: 5
        """
        return len(self.text)

    def __lt__(self, other: object) -> bool:
        """
        Check if this LangString is less than another LangString object or string.

        This method compares the LangString's text with another LangString's text or a regular string.

        :param other: The LangString or string to compare with.
        :type other: object
        :return: True if this LangString's text is less than the other text, otherwise False.
        :rtype: bool
        :raises TypeError: If the objects are not compatible for comparison.
        :raises ValueError: If the language tags are incompatible.

        :Example:

        >>> lang_str1 = LangString("apple", "en")
        >>> lang_str2 = LangString("banana", "en")
        >>> print(lang_str1 < lang_str2)  # Output: True
        >>> print(lang_str1 < "banana")  # Output: True
        """
        self._validate_match_langs(other)
        self._validate_match_types(other)

        if isinstance(other, str):
            return self.text < other
        if isinstance(other, LangString):
            return self.text < other.text
        return NotImplemented

    @TypeValidator.validate_type_decorator
    def __mul__(self, other: int) -> "LangString":
        """
        Multiply the LangString's text a specified number of times.

        This method repeats the LangString's text a specified number of times and returns a new LangString.

        :param other: The number of times to repeat the text.
        :type other: int
        :return: A new LangString with the text repeated.
        :rtype: LangString
        :raises TypeError: If the operand is not an integer.

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> multiplied_lang_str = lang_str * 3
        >>> print(multiplied_lang_str)  # Output: "hellohellohello"@en
        """
        return LangString(self.text * other, self.lang)

    @TypeValidator.validate_type_decorator
    def __radd__(self, other: str) -> str:
        """
        Handle concatenation when LangString is on the right side of the '+' operator.

        This method is only defined for 'other' of type string because the __add__ method is used when 'other'
        is a LangString. It concatenates the other's text to the LangString's text (in this order) and returns a
        string, which loses its language tag.

        :param other: The string to concatenate with.
        :type other: str
        :return: A new string with the concatenated text.
        :rtype: str
        :raises TypeError: If 'other' is not a string.

        :Example:

        >>> lang_str = LangString("world", "en")
        >>> result = "hello " + lang_str
        >>> print(result)  # Output: 'hello world'
        """
        return other + self.text

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the LangString.

        :return: The unambiguous string representation of the LangString.
        :rtype: str

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> print(repr(lang_str))  # Output: 'LangString(text="hello", lang="en")'
        """
        return f"{self.__class__.__name__}(text={repr(self.text)}, lang={repr(self.lang)})"

    @TypeValidator.validate_type_decorator
    def __rmul__(self, other: int) -> "LangString":
        """
        Implement right multiplication.

        This method is called for the reversed operation of multiplication, i.e., when LangString is on the right side.
        It is typically used for repeating the LangString's text a specified number of times.

        :param other: The number of times the LangString's text should be repeated.
        :type other: int
        :return: A new LangString with the text repeated.
        :rtype: LangString
        :raises TypeError: If 'other' is not an integer.

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> multiplied_lang_str = 3 * lang_str
        >>> print(multiplied_lang_str)  # Output: "hellohellohello"@en
        """
        return LangString(self.text * other, self.lang)

    def __str__(self) -> str:
        """
        Define the string representation of the LangString object.

        :return: The string representation of the LangString object.
        :rtype: str

        :Example:

        >>> lang_str = LangString("hello", "en")
        >>> print(lang_str)  # Output: '"hello"@en'
        """
        print_with_quotes = Controller.get_flag(LangStringFlag.PRINT_WITH_QUOTES)
        print_with_lang = Controller.get_flag(LangStringFlag.PRINT_WITH_LANG)

        text_representation = f'"{self.text}"' if print_with_quotes else self.text
        lang_representation = f"@{self.lang}" if print_with_lang else ""

        return text_representation + lang_representation

    # ---------------------------------------------
    # Static Methods
    # ---------------------------------------------

    @staticmethod
    def merge_langstrings(langstrings: list["LangString"]) -> list["LangString"]:
        """
        Merge duplicated LangStrings in a list based on content and language tags.

        This method processes a list of LangString instances, identifying and merging duplicates
        based on their text and language tags. If there are multiple LangStrings with the same text
        but different language tag casings, the resulting LangString will use a casefolded version
        of the language tag.

        :param langstrings: List of LangString instances to be merged.
        :type langstrings: list[LangString]
        :return: A list of merged LangString instances without duplicates.
        :rtype: list[LangString]

        :Example:

        >>> lang_str1 = LangString("Hello", "en")
        >>> lang_str2 = LangString("Hello", "EN")
        >>> lang_str3 = LangString("Bonjour", "fr")
        >>> merged_list = LangString.merge_langstrings([lang_str1, lang_str2, lang_str3])
        >>> for ls in merged_list:
        ...     print(ls)
        ...
        >>> # Output: '"Hello"@en'
        >>> #         '"Bonjour"@fr'
        """
        TypeValidator.validate_type_iterable(langstrings, list, LangString)

        merged: dict[tuple[str, str], LangString] = {}
        lang_case_map: dict[tuple[str, str], str] = {}
        for ls in langstrings:
            key = (ls.text, ls.lang.casefold())
            if key in merged:
                if merged[key].lang != ls.lang:
                    lang_case_map[key] = ls.lang.casefold()
            else:
                merged[key] = ls
                lang_case_map[key] = ls.lang  # Keep track of the original casing

        # Adjust the language tags based on detected case variations
        for key, ls in merged.items():
            ls.lang = lang_case_map.get(key, ls.lang)  # Using get() to safely handle missing entries

        return list(merged.values())

    @TypeValidator.validate_type_decorator
    @staticmethod
    def print_list(
        langstring_list: list["LangString"],
        print_quotes: Optional[bool] = None,
        separator: str = "@",
        print_lang: Optional[bool] = None,
    ) -> None:
        """
        Print a string representation of a list of LangString instances using the to_string method \
        with specified formatting options.

        :param langstring_list: The list of LangString instances.
        :type langstring_list: list[LangString]
        :param print_quotes: If True, wrap the text in quotes. If None, use the default setting from the Controller.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between the text and language tag.
        :type separator: str
        :param print_lang: If True, include the language tag. If None, use the default setting from the Controller.
        :type print_lang: Optional[bool]

        :Example:

        >>> lang_str1 = LangString("a", "b")
        >>> lang_str2 = LangString("c", "d")
        >>> ls_list = [lang_str1, lang_str2]
        >>> LangString.print_list(ls_list)  # Output: ['"a"@b', '"c"@d']
        """
        formatted_strings = [ls.to_string(print_quotes, separator, print_lang) for ls in langstring_list]
        print("[" + ", ".join(formatted_strings) + "]")

    # ---------------------------------------------
    # Private Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    def _validate_match_types(self, other: Union[object, str, "LangString"], overwrite_strict: bool = False) -> None:
        """
        Validate that the type of the other operand matches the expected type.

        This method checks if the operand type is valid based on the control flag for type matching.
        If strict type matching is enabled, only LangString type is allowed. The strict mode can be
        overridden by passing the `overwrite_strict` parameter.

        :param other: The operand to be validated.
        :type other: Union[object, str, LangString]
        :param overwrite_strict: If True, enforces strict type matching regardless of the control flag.
        :type overwrite_strict: bool
        :raises TypeError: If strict mode is enabled and the operand is not of type LangString.

        :Example:

        >>> lang_str = LangString("Hello", "en")
        >>> lang_str._validate_match_types(lang_str, False)  # No exception
        >>> lang_str._validate_match_types(lang_str, True)  # Raises TypeError
        """
        strict = Controller.get_flag(LangStringFlag.METHODS_MATCH_TYPES) if not overwrite_strict else overwrite_strict

        # If strict mode is enabled, only allow LangString type
        if strict and not isinstance(other, LangString):
            raise TypeError(
                f"Strict mode is enabled. Operand must be of type LangString, but got {type(other).__name__}."
            )

    @TypeValidator.validate_type_decorator
    def _validate_match_langs(self, other: object) -> None:
        """
        Validate that the language of the other LangString operand matches the current LangString's language.

        This method checks if the language tags of both LangString objects are compatible. If the languages
        do not match, a ValueError is raised.

        :param other: The operand to be validated.
        :type other: object
        :raises ValueError: If the languages of both LangString objects do not match.

        :Example:

        >>> lang_str1 = LangString("Hello", "en")
        >>> lang_str2 = LangString("Bonjour", "fr")
        >>> lang_str1._validate_match_langs(LangString("world", "en"))  # No exception
        >>> lang_str1._validate_match_langs(lang_str2)  # Raises ValueError due to incompatible languages
        """
        # Check language compatibility for LangString type
        if isinstance(other, LangString) and self.lang.casefold() != other.lang.casefold():
            raise ValueError(
                f"Operation cannot be performed. "
                f"Incompatible languages between LangString and {type(other).__name__} object."
            )
