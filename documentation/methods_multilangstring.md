# Methods in MultiLangString Class

<!-- TOC -->
* [Methods in MultiLangString Class](#methods-in-multilangstring-class)
  * [Initialization and Properties](#initialization-and-properties)
  * [MultiLangString's Regular Methods](#multilangstrings-regular-methods)
    * [Add Methods](#add-methods)
    * [Discard Methods](#discard-methods)
    * [Remove Methods](#remove-methods)
    * [Conversion Methods](#conversion-methods)
    * [Count Methods](#count-methods)
    * [Contain Methods](#contain-methods)
    * [Get Methods](#get-methods)
    * [Pop Methods](#pop-methods)
    * [General Methods](#general-methods)
  * [Overwritten Dictionary's Dunder Methods](#overwritten-dictionarys-dunder-methods)
  * [Static Methods](#static-methods)
<!-- TOC -->

## Initialization and Properties

- `__init__(self, mls_dict: Optional[dict[str, set[str]]] = None, pref_lang: Optional[str] = "en") -> None`
  - Initialize a MultiLangString object with an optional dictionary and preferred language.

- `mls_dict(self) -> dict[str, set[str]]`
  - Get the dictionary representing the internal structure of the MultiLangString.

- `mls_dict(self, in_mls_dict: Optional[dict[str, set[str]]]) -> None`
  - Set the dictionary representing the internal structure of the MultiLangString with validation.

- `pref_lang(self) -> str`
  - Get the preferred language for this MultiLangString.

- `pref_lang(self, new_pref_lang: Optional[str]) -> None`
  - Set the preferred language for this MultiLangString with validation.

## MultiLangString's Regular Methods

### Add Methods

- `add(self, arg: Union[tuple[str, str], LangString, SetLangString, "MultiLangString"]) -> None`
  - Add an element to the MultiLangString.

- `add_entry(self, text: str, lang: Optional[str]) -> None`
  - Add a text entry to the MultiLangString under a specified language.

- `add_text_in_pref_lang(self, text: str) -> None`
  - Add a text entry to the preferred language.

- `add_langstring(self, langstring: LangString) -> None`
  - Add a LangString to the MultiLangString.

- `add_setlangstring(self, setlangstring: SetLangString) -> None`
  - Add a SetLangString to the MultiLangString.

- `add_multilangstring(self, multilangstring: "MultiLangString") -> None`
  - Add a MultiLangString to the MultiLangString.

- `add_empty_lang(self, lang: str) -> None`
  - Add an empty language to the MultiLangString.

### Discard Methods

- `discard(self, arg: Union[tuple[str, str], LangString, SetLangString, "MultiLangString"], clean_empty: bool = False) -> None`
  - Discard an entry, LangString, SetLangString, or MultiLangString from the MultiLangString.

- `discard_entry(self, text: str, lang: str, clean_empty: bool = False) -> None`
  - Discard a text entry from a specified language in the MultiLangString.

- `discard_text_in_pref_lang(self, text: str, clean_empty: bool = False) -> None`
  - Discard a text entry from the preferred language.

- `discard_langstring(self, langstring: LangString, clean_empty: bool = False) -> None`
  - Discard a LangString from the MultiLangString.

- `discard_setlangstring(self, setlangstring: SetLangString, clean_empty: bool = False) -> None`
  - Discard a SetLangString from the MultiLangString.

- `discard_multilangstring(self, multilangstring: "MultiLangString", clean_empty: bool = False) -> None`
  - Discard a MultiLangString from the current MultiLangString.

- `discard_lang(self, lang: str) -> None`
  - Discard all entries for a specified language.

### Remove Methods

- `remove(self, arg: Union[tuple[str, str], LangString, SetLangString, "MultiLangString"], clean_empty: bool = False) -> None`
  - Remove an entry, LangString, SetLangString, or MultiLangString from the MultiLangString.

- `remove_entry(self, text: str, lang: str, clean_empty: bool = False) -> None`
  - Remove a single entry from the set of a given language key in the dictionary.

- `remove_text_in_pref_lang(self, text: str, clean_empty: bool = False) -> None`
  - Remove a text entry from the preferred language.

- `remove_langstring(self, langstring: LangString, clean_empty: bool = False) -> None`
  - Remove a LangString from the MultiLangString.

- `remove_setlangstring(self, setlangstring: SetLangString, clean_empty: bool = False) -> None`
  - Remove a SetLangString from the MultiLangString.

- `remove_multilangstring(self, multilangstring: "MultiLangString", clean_empty: bool = False) -> None`
  - Remove a MultiLangString from the current MultiLangString.

- `remove_lang(self, lang: str) -> None`
  - Remove all entries of a given language from the dictionary.

- `remove_empty_langs(self) -> None`
  - Remove all empty language entries from the dictionary.

### Conversion Methods

- `to_strings(self, langs: Optional[list[str]] = None, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert the MultiLangString to a list of formatted strings.

- `to_langstrings(self, langs: Optional[list[str]] = None) -> list[LangString]`
  - Convert the MultiLangString to a list of LangString objects.

- `to_setlangstrings(self, langs: Optional[list[str]] = None) -> list[SetLangString]`
  - Convert the MultiLangString to a list of SetLangString objects.

### Count Methods

- `count_entries_of_lang(self, lang: str) -> int`
  - Count the number of text entries for a given language.

- `count_entries_per_lang(self) -> dict[str, int]`
  - Return the number of text entries for each language.

- `count_entries_total(self) -> int`
  - Return the total number of text entries across all languages.

- `count_langs_total(self) -> int`
  - Count the total number of languages in the MultiLangString.

### Contain Methods

- `contains(self, arg: Union[tuple[str, str], LangString, SetLangString, "MultiLangString"]) -> bool`
  - Check if the MultiLangString contains the specified entry, LangString, SetLangString, or MultiLangString.

- `contains_entry(self, text: str, lang: str) -> bool`
  - Check if a specific text entry exists in a given language.

- `contains_lang(self, lang: str) -> bool`
  - Check if a specific language exists in the MultiLangString.

- `contains_text_in_pref_lang(self, text: str) -> bool`
  - Check if a specific text exists in the preferred language.

- `contains_text_in_any_lang(self, text: str) -> bool`
  - Check if a specific text exists in any language.

- `contains_langstring(self, langstring: LangString) -> bool`
  - Check if the given LangString's text and language are part of this MultiLangString.

- `contains_setlangstring(self, setlangstring: SetLangString) -> bool`
  - Check if all texts and the language of a SetLangString are part of this MultiLangString.

- `contains_multilangstring(self, multilangstring: "MultiLangString") -> bool`
  - Check if the current instance contains all languages and texts of another MultiLangString instance.

### Get Methods

- `get_langs(self, casefold: bool = False) -> list[str]`
  - Return a list of all languages in the MultiLangString.

- `get_texts(self) -> list[str]`
  - Return a sorted list of all texts in the MultiLangString.

- `get_langstring(self, text: str, lang: str) -> LangString`
  - Retrieve a LangString from the MultiLangString.

- `get_setlangstring(self, lang: str) -> SetLangString`
  - Retrieve a SetLangString from the MultiLangString.

- `get_multilangstring(self, langs: list[str]) -> "MultiLangString"`
  - Retrieve a MultiLangString containing only the specified languages.

### Pop Methods

- `pop_langstring(self, text: str, lang: str) -> Optional[LangString]`
  - Remove and return a LangString from the MultiLangString.

- `pop_setlangstring(self, lang: str) -> Optional[SetLangString]`
  - Remove and return a SetLangString from the MultiLangString.

- `pop_multilangstring(self, langs: list[str]) -> "MultiLangString"`
  - Remove and return a MultiLangString containing the specified languages.

### General Methods

- `has_pref_lang_entries(self) -> bool`
  - Check if there are any entries in the preferred language.

## Overwritten Dictionary's Dunder Methods

- `__contains__(self, lang: str) -> bool`
  - Check if a language is in the MultiLangString.

- `__delitem__(self, lang: str) -> None`
  - Allow deletion of language entries.

- `__eq__(self, other: object) -> bool`
  - Check equality of this MultiLangString with another MultiLangString.

- `__getitem__(self, lang: str) -> set[str]`
  - Allow retrieval of entries by language.

- `__hash__(self) -> int`
  - Generate a hash value for a MultiLangString object.

- `__iter__(self) -> Iterator[str]`
  - Allow iteration over the dictionary keys (language codes).

- `__len__(self) -> int`
  - Return the number of languages in the dictionary.

- `__repr__(self) -> str`
  - Return a detailed string representation of the MultiLangString object.

- `__reversed__(self) -> Iterator[str]`
  - Return a reverse iterator over the dictionary keys.

- `__setitem__(self, lang: str, texts: set[str]) -> None`
  - Allow setting entries by language.

- `__str__(self) -> str`
  - Return a string representation of the MultiLangString, including language tags.

## Static Methods

- `merge_multilangstrings(multilangstrings: list["MultiLangString"]) -> list["MultiLangString"]`
  - Merge multiple MultiLangString objects into one.
