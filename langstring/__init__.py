"""
The langstring package provides classes and utilities for handling multilingual text.

This package is designed to support the management and manipulation of strings in multiple languages, providing a
framework for applications that require multilingual support.

Modules and Classes:
--------------------
- controller:
    Handles the control mechanisms for language strings.

- converter:
    Provides utilities for converting language strings between different formats.

- flags:
    Defines various flag classes used for global settings and specific types of language strings.

    - GlobalFlag:
        A flag for global settings affecting all language string types.

    - LangStringFlag:
        A flag specific to single language strings.

    - SetLangStringFlag:
        A flag specific to sets of language strings.

    - MultiLangStringFlag:
        A flag specific to multi-language strings.

- langstring:
    Represents a single language string, encapsulating its properties and behaviors.

- multilangstring:
    Represents a string in multiple langs, providing methods to manage and manipulate the different language variants.

- setlangstring:
    Represents a set of language strings, facilitating operations on groups of multilingual texts.

Package Contents:
-----------------
The package exports the following classes and flags for use in external modules:

- LangString
- SetLangString
- MultiLangString
- Controller
- GlobalFlag
- LangStringFlag
- SetLangStringFlag
- MultiLangStringFlag
- Converter

Language Tag Handling:
----------------------
In this library's context, language tags are case-insensitive, meaning ,e.g., `en` and `EN` are considered equivalent.
However, subtags such as `en`, `en-UK`, and `en-US` are treated as distinct entities.
Additionally, spaces in language tags are not automatically trimmed unless the classes' `STRIP_LANG` flags are True.
As an example, `"en"` is not considered equal to `"en "`. However, if the `STRIP_LANG` flag is set to True, `"en "`
will be converted to `"en"`, thereby making the languages equal.


Usage:
------
To use this package, import the necessary classes and flags as follows:

    from langstring import (
        LangString, MultiLangString, SetLangString, Controller,
        GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag, Converter
    )
"""

from .controller import Controller
from .converter import Converter
from .flags import GlobalFlag
from .flags import LangStringFlag
from .flags import MultiLangStringFlag
from .flags import SetLangStringFlag
from .langstring import LangString
from .multilangstring import MultiLangString
from .setlangstring import SetLangString

"""
The __all__ variable defines the public interface of the module.

It is a list of the module's public classes, functions, and variables that will be imported
when `from langstring import *` is used.

This helps to control the namespace and avoids importing unnecessary components.
"""
__all__ = [
    "LangString",
    "SetLangString",
    "MultiLangString",
    "Controller",
    "GlobalFlag",
    "LangStringFlag",
    "SetLangStringFlag",
    "MultiLangStringFlag",
    "Converter",
]
