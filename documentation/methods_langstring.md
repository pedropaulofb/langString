# Methods in LangString Class

<!-- TOC -->
* [Methods in LangString Class](#methods-in-langstring-class)
  * [Initialization and Properties](#initialization-and-properties)
  * [Overwritten String's Built-in Regular Methods](#overwritten-strings-built-in-regular-methods)
  * [LangString's Regular Methods](#langstrings-regular-methods)
  * [Overwritten String's Built-in Dunder Methods](#overwritten-strings-built-in-dunder-methods)
  * [Static Methods](#static-methods)
<!-- TOC -->

## Initialization and Properties

- `__init__(self, text: str = "", lang: str = "") -> None`
  - Initialize a new LangString object with text and an optional language tag.

- `text(self) -> str`
  - Get the text string.

- `text(self, new_text: Optional[str]) -> None`
  - Set the text string, with validation based on control flags.

- `lang(self) -> str`
  - Get the language tag.

- `lang(self, new_lang: Optional[str]) -> None`
  - Set the language tag, with validation based on control flags.

## Overwritten String's Built-in Regular Methods

- `capitalize(self) -> "LangString"`
  - Return a copy of the LangString with its first character capitalized and the rest lowercased.

- `casefold(self) -> "LangString"`
  - Return a casefolded copy of the LangString.

- `center(self, width: int, fillchar: str = " ") -> "LangString"`
  - Return a centered LangString of length width with specified fill character.

- `count(self, sub: str, start: int = 0, end: Optional[int] = None) -> int`
  - Return the number of non-overlapping occurrences of substring sub.

- `endswith(self, suffix: str, start: int = 0, end: Optional[int] = None) -> bool`
  - Return True if the LangString ends with the specified suffix.

- `expandtabs(self, tabsize: int = 8) -> "LangString"`
  - Return a copy of the LangString where all tab characters are expanded using spaces.

- `find(self, sub: str, start: int = 0, end: Optional[int] = None) -> int`
  - Return the lowest index where substring sub is found.

- `format(self, *args: Any, **kwargs: Any) -> "LangString"`
  - Perform a string formatting operation on the LangString.

- `format_map(self, mapping: dict[Any, Any]) -> "LangString"`
  - Perform a string formatting operation using a dictionary.

- `index(self, sub: str, start: int = 0, end: Optional[int] = None) -> int`
  - Return the lowest index where substring sub is found.

- `isalnum(self) -> bool`
  - Return True if all characters in the LangString are alphanumeric.

- `isalpha(self) -> bool`
  - Return True if all characters in the LangString are alphabetic.

- `isascii(self) -> bool`
  - Return True if all characters in the LangString are ASCII characters.

- `isdecimal(self) -> bool`
  - Return True if all characters in the LangString are decimal characters.

- `isdigit(self) -> bool`
  - Return True if all characters in the LangString are digits.

- `isidentifier(self) -> bool`
  - Return True if the LangString is a valid identifier according to Python language definition.

- `islower(self) -> bool`
  - Return True if all cased characters in the LangString are lowercase.

- `isnumeric(self) -> bool`
  - Return True if all characters in the LangString are numeric characters.

- `isprintable(self) -> bool`
  - Return True if all characters in the LangString are printable.

- `isspace(self) -> bool`
  - Return True if there are only whitespace characters in the LangString.

- `istitle(self) -> bool`
  - Return True if the LangString is a titlecased string.

- `isupper(self) -> bool`
  - Return True if all cased characters in the LangString are uppercase.

- `join(self, iterable: Iterable[str]) -> "LangString"`
  - Join an iterable of strings with the LangString's text.

- `ljust(self, width: int, fillchar: str = " ") -> "LangString"`
  - Return a left-justified LangString of length width with specified fill character.

- `lower(self) -> "LangString"`
  - Return a copy of the LangString with all characters converted to lowercase.

- `lstrip(self, chars: Optional[str] = None) -> "LangString"`
  - Return a copy of the LangString with leading characters removed.

- `partition(self, sep: str) -> tuple["LangString", "LangString", "LangString"]`
  - Split the LangString at the first occurrence of sep and return a 3-tuple.

- `replace(self, old: str, new: str, count: int = -1) -> "LangString"`
  - Return a copy of the LangString with all occurrences of substring old replaced by new.

- `removeprefix(self, prefix: str) -> "LangString"`
  - Remove the specified prefix from the LangString's text.

- `removesuffix(self, suffix: str) -> "LangString"`
  - Remove the specified suffix from the LangString's text.

- `rfind(self, sub: str, start: int = 0, end: Optional[int] = None) -> int`
  - Return the highest index where substring sub is found.

- `rindex(self, sub: str, start: int = 0, end: Optional[int] = None) -> int`
  - Return the highest index where substring sub is found.

- `rjust(self, width: int, fillchar: str = " ") -> "LangString"`
  - Return a right-justified LangString of length width with specified fill character.

- `rpartition(self, sep: str) -> tuple["LangString", "LangString", "LangString"]`
  - Split the LangString at the last occurrence of sep and return a 3-tuple.

- `rsplit(self, sep: Optional[str] = None, maxsplit: int = -1) -> list["LangString"]`
  - Return a list of the words in the LangString, using sep as the delimiter string.

- `rstrip(self, chars: Optional[str] = None) -> "LangString"`
  - Return a copy of the LangString with trailing characters removed.

- `split(self, sep: Optional[str] = None, maxsplit: int = -1) -> list["LangString"]`
  - Return a list of the words in the LangString, using sep as the delimiter string.

- `splitlines(self, keepends: bool = False) -> list["LangString"]`
  - Return a list of the lines in the LangString, breaking at line boundaries.

- `startswith(self, prefix: str, start: int = 0, end: Optional[int] = None) -> bool`
  - Return True if the LangString starts with the specified prefix.

- `strip(self, chars: Optional[str] = None) -> "LangString"`
  - Return a copy of the LangString with leading and trailing characters removed.

- `swapcase(self) -> "LangString"`
  - Return a copy of the LangString with uppercase characters converted to lowercase and vice versa.

- `title(self) -> "LangString"`
  - Return a titlecased version of the LangString.

- `translate(self, table: dict[int, str]) -> "LangString"`
  - Return a copy of the LangString with each character mapped through the given translation table.

- `upper(self) -> "LangString"`
  - Return a copy of the LangString with all characters converted to uppercase.

- `zfill(self, width: int) -> "LangString"`
  - Return a copy of the LangString left filled with ASCII '0' digits to make a string of length width.

## LangString's Regular Methods

- `to_string(self, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> str`
  - Return a string representation of the LangString with options for including quotes and language tag.

- `equals_str(self, other: str) -> bool`
  - Compare the LangString's text with a given string for equality.

- `equals_langstring(self, other: "LangString") -> bool`
  - Compare the LangString with another LangString for equality of text and language tag.

## Overwritten String's Built-in Dunder Methods

- `__add__(self, other: Union["LangString", str]) -> "LangString"`
  - Add another LangString or a string to this LangString.

- `__contains__(self, item: str) -> bool`
  - Check if a substring exists within the LangString's text.

- `__eq__(self, other: object) -> bool`
  - Check equality of this LangString with another object.

- `__ge__(self, other: object) -> bool`
  - Check if this LangString is greater than or equal to another str or LangString object.

- `__getitem__(self, key: Union[int, slice]) -> "LangString"`
  - Retrieve a substring or a reversed string from the LangString's text.

- `__gt__(self, other: object) -> bool`
  - Check if this LangString is greater than another LangString object.

- `__hash__(self) -> int`
  - Generate a hash value for a LangString object.

- `__iadd__(self, other: Union["LangString", str]) -> "LangString"`
  - Implement in-place addition for LangString objects.

- `__imul__(self, other: int) -> "LangString"`
  - Implement in-place multiplication of the LangString's text.

- `__iter__(self) -> Iterator[str]`
  - Enable iteration over the text part of the LangString.

- `__le__(self, other: object) -> bool`
  - Check if this LangString is less than or equal to another LangString object or string.

- `__len__(self) -> int`
  - Return the length of the LangString's text.

- `__lt__(self, other: object) -> bool`
  - Check if this LangString is less than another LangString object or string.

- `__mul__(self, other: int) -> "LangString"`
  - Multiply the LangString's text a specified number of times.

- `__radd__(self, other: str) -> str`
  - Handle concatenation when LangString is on the right side of the '+' operator.

- `__repr__(self) -> str`
  - Return an unambiguous string representation of the LangString.

- `__rmul__(self, other: int) -> "LangString"`
  - Implement right multiplication for LangString.

- `__str__(self) -> str`
  - Define the string representation of the LangString object.

## Static Methods

- `merge_langstrings(langstrings: list["LangString"]) -> list["LangString"]`
  - Merge duplicated LangStrings in a list based on content and language tags.

- `print_list(langstring_list: list["LangString"], print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> None`
  - Print a string representation of a list of LangString instances.
