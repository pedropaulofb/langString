# Methods in Controller Class

## Controller's Regular Methods

- `set_flag(cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], state: bool) -> None`
  - Set the state of a specified configuration flag for LangString, SetLangString, or MultiLangString.

- `get_flag(cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]) -> bool`
  - Retrieve the current state of a specified configuration flag.

- `get_flags(cls) -> dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool]`
  - Retrieve the current state of all configuration flags.

- `print_flag(cls, flag: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]]) -> None`
  - Print the current state of a specific configuration flag.

- `print_flags(cls, flag_type: Optional[type] = None) -> None`
  - Print the current state of configuration flags in alphabetical order.

- `reset_flag(cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]) -> None`
  - Reset a specific flag to its default value.

- `reset_flags(cls, flag_type: Optional[type] = GlobalFlag) -> None`
  - Reset all flags of a specific type to their default values.
