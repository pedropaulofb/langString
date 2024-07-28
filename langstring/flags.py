"""
The `flags` module provides enumerations for various control flags used to configure the behavior of the `LangString`, \
`SetLangString`, and `MultiLangString` classes.

This module defines several enumerations (`Enums`), each specifying different flags that can be set to influence the
operation and validation rules of the respective classes. These flags offer a flexible way to enforce constraints and
manage the behavior of multilingual text handling within the application.

Enums defined in this module:

- **GlobalFlag**: Flags that affect the behavior of all classes. These global flags ensure consistent behavior across
  the entire system when dealing with multilingual strings.
- **LangStringFlag**: Flags specific to the `LangString` class. These flags control how individual language strings
  are handled, validated, and displayed.
- **SetLangStringFlag**: Flags specific to the `SetLangString` class. These flags manage the behavior of sets of
  language strings, allowing for batch operations and validations.
- **MultiLangStringFlag**: Flags specific to the `MultiLangString` class. These flags configure the behavior of
  multilingual string collections, enabling complex multilingual text management.

Each enumeration includes flags for various aspects such as text validation, language code handling,
and output formatting.
These flags can be used to enforce rules like ensuring non-empty strings, validating language codes, converting language
codes to lowercase, and controlling the inclusion of quotes and language tags in output.

Using these flags, developers can customize and control the behavior of multilingual text handling classes, ensuring
that they meet the specific needs of their applications.
"""

from enum import auto
from enum import Enum


class GlobalFlag(Enum):
    """
    Enumeration for global control flags.

    This enum defines various flags that can be used to configure the behavior of all classes in the multilingual text
    handling system. These flags provide a flexible way to enforce constraints and manage behavior consistently across
    different classes.

    :cvar DEFINED_LANG: Ensures that a non-empty string is used for the 'lang' field of all classes.
    :vartype DEFINED_LANG: Enum
    :cvar DEFINED_TEXT: Ensures that a non-empty string is used for the 'text' field of all classes.
    :vartype DEFINED_TEXT: Enum
    :cvar ENFORCE_EXTRA_DEPEND: Enforces additional dependencies required by all classes.
    :vartype ENFORCE_EXTRA_DEPEND: Enum
    :cvar LOWERCASE_LANG: Converts all language codes to lowercase.
    :vartype LOWERCASE_LANG: Enum
    :cvar METHODS_MATCH_TYPES: Ensures that methods match the expected types for arguments and return values.
    :vartype METHODS_MATCH_TYPES: Enum
    :cvar PRINT_WITH_LANG: Includes language tags when printing multilingual text.
    :vartype PRINT_WITH_LANG: Enum
    :cvar PRINT_WITH_QUOTES: Wraps text entries in quotes when printing multilingual text.
    :vartype PRINT_WITH_QUOTES: Enum
    :cvar STRIP_LANG: Removes leading and trailing whitespace from language codes.
    :vartype STRIP_LANG: Enum
    :cvar STRIP_TEXT: Removes leading and trailing whitespace from text entries.
    :vartype STRIP_TEXT: Enum
    :cvar VALID_LANG: Ensures that a valid language code string is used for the 'lang' field of all classes.
    :vartype VALID_LANG: Enum
    """

    DEFINED_LANG = auto()
    DEFINED_TEXT = auto()
    ENFORCE_EXTRA_DEPEND = auto()
    LOWERCASE_LANG = auto()
    METHODS_MATCH_TYPES = auto()
    PRINT_WITH_LANG = auto()
    PRINT_WITH_QUOTES = auto()
    STRIP_LANG = auto()
    STRIP_TEXT = auto()
    VALID_LANG = auto()


class LangStringFlag(Enum):
    """
    Enumeration for LangString control flags.

    This enum defines various flags that can be used to configure the behavior of the LangString class. These flags
    provide a flexible way to enforce constraints and manage the behavior of multilingual text handling within the
    LangString class.

    :cvar DEFINED_LANG: Ensures that a non-empty string is used for the 'lang' field of a LangString.
    :vartype DEFINED_LANG: Enum
    :cvar DEFINED_TEXT: Ensures that a non-empty string is used for the 'text' field of a LangString.
    :vartype DEFINED_TEXT: Enum
    :cvar LOWERCASE_LANG: Converts all language codes to lowercase within a LangString.
    :vartype LOWERCASE_LANG: Enum
    :cvar METHODS_MATCH_TYPES: Ensures that methods match the expected types for arguments and return values within
                               a LangString.
    :vartype METHODS_MATCH_TYPES: Enum
    :cvar PRINT_WITH_LANG: Includes language tags when printing a LangString.
    :vartype PRINT_WITH_LANG: Enum
    :cvar PRINT_WITH_QUOTES: Wraps text entries in quotes when printing a LangString.
    :vartype PRINT_WITH_QUOTES: Enum
    :cvar STRIP_LANG: Removes leading and trailing whitespace from language codes within a LangString.
    :vartype STRIP_LANG: Enum
    :cvar STRIP_TEXT: Removes leading and trailing whitespace from text entries within a LangString.
    :vartype STRIP_TEXT: Enum
    :cvar VALID_LANG: Ensures that a valid language code string is used for the 'lang' field of a LangString.
    :vartype VALID_LANG: Enum
    """

    DEFINED_LANG = auto()
    DEFINED_TEXT = auto()
    LOWERCASE_LANG = auto()
    METHODS_MATCH_TYPES = auto()
    PRINT_WITH_LANG = auto()
    PRINT_WITH_QUOTES = auto()
    STRIP_LANG = auto()
    STRIP_TEXT = auto()
    VALID_LANG = auto()


class SetLangStringFlag(Enum):
    """
    Enumeration for SetLangString control flags.

    This enum defines various flags that can be used to configure the behavior of the SetLangString class. These flags
    provide a flexible way to enforce constraints and manage the behavior of multilingual text handling within the
    SetLangString class.

    :cvar DEFINED_LANG: Ensures that a non-empty string is used for the 'lang' field of a SetLangString.
    :vartype DEFINED_LANG: Enum
    :cvar DEFINED_TEXT: Ensures that a non-empty string is used for the 'text' field of a SetLangString.
    :vartype DEFINED_TEXT: Enum
    :cvar LOWERCASE_LANG: Converts all language codes to lowercase within a SetLangString.
    :vartype LOWERCASE_LANG: Enum
    :cvar METHODS_MATCH_TYPES: Ensures that methods match the expected types for arguments and return values within
                               a SetLangString.
    :vartype METHODS_MATCH_TYPES: Enum
    :cvar PRINT_WITH_LANG: Includes language tags when printing a SetLangString.
    :vartype PRINT_WITH_LANG: Enum
    :cvar PRINT_WITH_QUOTES: Wraps text entries in quotes when printing a SetLangString.
    :vartype PRINT_WITH_QUOTES: Enum
    :cvar STRIP_LANG: Removes leading and trailing whitespace from language codes within a SetLangString.
    :vartype STRIP_LANG: Enum
    :cvar STRIP_TEXT: Removes leading and trailing whitespace from text entries within a SetLangString.
    :vartype STRIP_TEXT: Enum
    :cvar VALID_LANG: Ensures that a valid language code string is used for the 'lang' field of a SetLangString.
    :vartype VALID_LANG: Enum
    """

    DEFINED_LANG = auto()
    DEFINED_TEXT = auto()
    LOWERCASE_LANG = auto()
    METHODS_MATCH_TYPES = auto()
    PRINT_WITH_LANG = auto()
    PRINT_WITH_QUOTES = auto()
    STRIP_LANG = auto()
    STRIP_TEXT = auto()
    VALID_LANG = auto()


class MultiLangStringFlag(Enum):
    """
    Enumeration for MultiLangString control flags.

    This enum defines various flags that can be used to configure the behavior of the MultiLangString class. These flags
    provide a flexible way to enforce constraints and manage the behavior of multilingual text handling within the
    MultiLangString class.

    :cvar DEFINED_LANG: Ensures that a non-empty string is used for the 'lang' field of a MultiLangString.
    :vartype DEFINED_LANG: Enum
    :cvar DEFINED_TEXT: Ensures that a non-empty string is used for the 'text' field of a MultiLangString.
    :vartype DEFINED_TEXT: Enum
    :cvar LOWERCASE_LANG: Converts all language codes to lowercase within a MultiLangString.
    :vartype LOWERCASE_LANG: Enum
    :cvar PRINT_WITH_LANG: Includes language tags when printing a MultiLangString.
    :vartype PRINT_WITH_LANG: Enum
    :cvar PRINT_WITH_QUOTES: Wraps text entries in quotes when printing a MultiLangString.
    :vartype PRINT_WITH_QUOTES: Enum
    :cvar STRIP_LANG: Removes leading and trailing whitespace from language codes within a MultiLangString.
    :vartype STRIP_LANG: Enum
    :cvar STRIP_TEXT: Removes leading and trailing whitespace from text entries within a MultiLangString.
    :vartype STRIP_TEXT: Enum
    :cvar VALID_LANG: Ensures that a valid language code string is used for the 'lang' field of a MultiLangString.
    :vartype VALID_LANG: Enum
    """

    DEFINED_LANG = auto()
    DEFINED_TEXT = auto()
    LOWERCASE_LANG = auto()
    PRINT_WITH_LANG = auto()
    PRINT_WITH_QUOTES = auto()
    STRIP_LANG = auto()
    STRIP_TEXT = auto()
    VALID_LANG = auto()
