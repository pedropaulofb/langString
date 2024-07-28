# Methods in Converter Class

## Strings' Conversion Methods

- `from_string_to_langstring(cls, method: str, input_string: str, lang: Optional[str] = None, separator: str = "@") -> LangString`
  - Convert a string to a LangString using the specified method.

- `from_string_to_langstring_manual(input_string: Optional[str], lang: Optional[str]) -> LangString`
  - Convert a string to a LangString with the specified language.

- `from_string_to_langstring_parse(input_string: str, separator: str = "@") -> LangString`
  - Convert a string to a LangString by parsing it with the given separator.

- `from_strings_to_langstrings(cls, method: str, strings: list[str], lang: Optional[str] = None, separator: str = "@") -> list[LangString]`
  - Convert a list of strings to a list of LangStrings using the specified method.

- `from_strings_to_setlangstring(cls, strings: list[str], lang: Optional[str] = None) -> SetLangString`
  - Convert a list of strings to a SetLangString using the 'manual' method.

- `from_strings_to_multilangstring(cls, method: str, strings: list[str], lang: Optional[str] = None, separator: str = "@") -> MultiLangString`
  - Convert a list of strings to a MultiLangString using the specified method.

## LangStrings' Conversion Methods

- `from_langstring_to_string(arg: LangString, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> str`
  - Convert a LangString to a string.

- `from_langstrings_to_strings(arg: list[LangString], print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert a list of LangStrings to a list of strings.

- `from_langstring_to_setlangstring(arg: LangString) -> SetLangString`
  - Convert a LangString to a SetLangString.

- `from_langstrings_to_setlangstring(arg: list[LangString]) -> SetLangString`
  - Convert a list of LangStrings to a SetLangString.

- `from_langstrings_to_setlangstrings(cls, arg: list[LangString]) -> list[SetLangString]`
  - Convert a list of LangStrings to a list of SetLangStrings.

- `from_langstring_to_multilangstring(arg: LangString) -> MultiLangString`
  - Convert a LangString to a MultiLangString.

- `from_langstrings_to_multilangstring(arg: list[LangString]) -> MultiLangString`
  - Convert a list of LangStrings to a MultiLangString.

## SetLangStrings' Conversion Methods

- `from_setlangstring_to_string(arg: SetLangString) -> str`
  - Convert a SetLangString to a string.

- `from_setlangstring_to_strings(arg: SetLangString, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert a SetLangString to a list of strings.

- `from_setlangstrings_to_strings(arg: list[SetLangString], print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert a list of SetLangStrings to a list of strings.

- `from_setlangstring_to_langstrings(arg: SetLangString) -> list[LangString]`
  - Convert a SetLangString to a list of LangStrings.

- `from_setlangstrings_to_langstrings(arg: list[SetLangString]) -> list[LangString]`
  - Convert a list of SetLangStrings to a list of LangStrings.

- `from_setlangstring_to_multilangstring(arg: SetLangString) -> MultiLangString`
  - Convert a SetLangString to a MultiLangString.

- `from_setlangstrings_to_multilangstring(arg: list[SetLangString]) -> MultiLangString`
  - Convert a list of SetLangString objects to a MultiLangString object.

## MultiLangStrings' Conversion Methods

- `from_multilangstring_to_string(arg: MultiLangString) -> str`
  - Convert a MultiLangString to a string.

- `from_multilangstring_to_strings(arg: MultiLangString, langs: Optional[list[str]] = None, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert a MultiLangString to a list of strings.

- `from_multilangstrings_to_strings(arg: list[MultiLangString], languages: Optional[list[str]] = None, print_quotes: bool = True, separator: str = "@", print_lang: bool = True) -> list[str]`
  - Convert a list of MultiLangStrings to a list of strings.

- `from_multilangstring_to_langstrings(arg: MultiLangString, languages: Optional[list[str]] = None) -> list[LangString]`
  - Convert a MultiLangString to a list of LangStrings.

- `from_multilangstrings_to_langstrings(arg: list[MultiLangString], languages: Optional[list[str]] = None) -> list[LangString]`
  - Convert a list of MultiLangStrings to a list of LangStrings.

- `from_multilangstring_to_setlangstrings(arg: MultiLangString, languages: Optional[list[str]] = None) -> list[SetLangString]`
  - Convert a MultiLangString to a list of SetLangStrings.

- `from_multilangstrings_to_setlangstrings(arg: list[MultiLangString], languages: Optional[list[str]] = None) -> list[SetLangString]`
  - Convert a list of MultiLangString objects to a list of SetLangString objects.
