[![Project DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10211480.svg)](https://doi.org/10.5281/zenodo.10211480)
[![Project Status - Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![GitHub - Release Date - PublishedAt](https://img.shields.io/github/release-date/pedropaulofb/langstring)
![GitHub - Last Commit - Branch](https://img.shields.io/github/last-commit/pedropaulofb/langstring/main)
![PyPI - Project](https://img.shields.io/pypi/v/langstring)
![PyPI - Downloads](https://img.shields.io/pypi/dm/langstring)
![Language - Top](https://img.shields.io/github/languages/top/pedropaulofb/langstring)
![Language - Version](https://img.shields.io/pypi/pyversions/langstring)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/pedropaulofb/langstring)
![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/pedropaulofb/langstring/badge)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![License - GitHub](https://img.shields.io/github/license/pedropaulofb/langstring)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pedropaulofb/langstring/main.svg)](https://results.pre-commit.ci/latest/github/pedropaulofb/langstring/main)
![Website](https://img.shields.io/website/http/pedropaulofb.github.io/langstring.svg)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/pedropaulofb/langstring/code_testing.yml)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8328/badge)](https://www.bestpractices.dev/projects/8328)
![Static Badge](https://img.shields.io/badge/Test_Coverage-100%25-green)

# LangString Python Library

LangString is a Python library designed to handle multilingual text data with precision and flexibility. Although the need for robust management of multilingual content is critical, existing solutions often lack the necessary features to manage language-tagged strings, sets of strings, and collections of multilingual strings effectively. LangString addresses this gap by providing classes and utilities that enable the creation, manipulation, and validation of multilingual text data consistently and accurately. Inspired by [RDFS's langstrings](https://www.w3.org/TR/rdf-schema/), LangString integrates seamlessly into Python applications, offering familiar methods that mimic those of regular Python types, making it intuitive for developers to adopt and use.

**📦 PyPI Package:**
The library is conveniently [available as a PyPI package](https://pypi.org/project/langstring/), allowing users to easily import it into other Python projects.

**📚 Documentation:**
For detailed documentation and code examples, please refer to the library's [docstring-generated documentation](https://pedropaulofb.github.io/langstring).

## Contents

<!-- TOC -->
* [LangString Python Library](#langstring-python-library)
  * [Contents](#contents)
  * [Installation and Usage](#installation-and-usage)
    * [Dependencies](#dependencies)
      * [Mandatory Dependencies](#mandatory-dependencies)
      * [Optional Dependencies](#optional-dependencies)
      * [Dev Dependencies](#dev-dependencies)
    * [Installation](#installation)
      * [Basic Installation](#basic-installation)
      * [Full Installation](#full-installation)
      * [Dev Installation](#dev-installation)
    * [Importing Elements](#importing-elements)
    * [Basic Usage](#basic-usage)
  * [Basic Reference](#basic-reference)
    * [Classes](#classes)
      * [LangString Class](#langstring-class)
      * [SetLangString Class](#setlangstring-class)
      * [MultiLangString Class](#multilangstring-class)
      * [Controller Class](#controller-class)
      * [Converter Class](#converter-class)
    * [Configuration via Flags](#configuration-via-flags)
    * [Elements' Relationships](#elements-relationships)
  * [Testing](#testing)
    * [Test Organization](#test-organization)
    * [Running the Tests](#running-the-tests)
    * [Continuous Integration](#continuous-integration)
  * [How to Contribute](#how-to-contribute)
    * [Reporting Issues](#reporting-issues)
    * [Code Contributions](#code-contributions)
    * [Test Contributions](#test-contributions)
    * [General Guidelines](#general-guidelines)
  * [Related Libraries and Differences](#related-libraries-and-differences)
  * [License](#license)
  * [Author](#author)
<!-- TOC -->

## Installation and Usage

### Dependencies

The LangString Python Library has been designed to be lightweight and easy to install. It has no mandatory dependencies and a single optional dependency to keep the installation process straightforward and ensure compatibility with various environments.

All dependencies of the LangString library can be found in its [`pyproject.toml` file](https://github.com/pedropaulofb/langstring/blob/main/pyproject.toml).

#### Mandatory Dependencies
The LangString Library does not require mandatory dependencies.

#### Optional Dependencies

The LangString Library has a single optional dependency, the [langcodes package](https://pypi.org/project/langcodes/). It is used  particularly for validating language tags when the `ENSURE_VALID_LANG` flag is enabled. This dependency is crucial for ensuring that language tags used in LangString and `MultiLangString` instances are valid and conform to international standards, thereby maintaining the integrity and reliability of multilingual text processing.

#### Dev Dependencies

For a complete list of development dependencies, please refer to the [Dev Dependencies List](https://github.com/pedropaulofb/langstring/blob/main/documentation/dev_dependencies.md).

### Installation

#### Basic Installation

To install the LangString library using `pip`, which is the package installer for Python, run the following command in your terminal or command prompt:

```sh
pip install langstring
```

This will download and install the latest version of the LangString library from [PyPI (Python Package Index)](https://pypi.org/project/langstring/).

#### Full Installation

For the full functionally of the LangString library, you need to install it together with its [optional dependency](#optional-dependencies) [langcodes](https://github.com/rspeer/langcodes/). To do that, use the following `pip` command:

```sh
pip install langstring[langcodes]
```

This command will install LangString along with the `langcodes` package.

#### Dev Installation

If you are planning to contribute to the development of `langstring`, you should install the [development dependencies](#dev-dependencies). First, you need to clone the repository. Run the following commands:

```sh
git clone https://github.com/pedropaulofb/langstring.git
cd langstring
pip install -r requirements.txt
```

This will clone the repository, navigate into the project directory, and install all the necessary packages needed for development.

### Importing Elements

After installation, you can use the following elements in your project: LangString, SetLangString, MultiLangString, Controller, GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag, and Converter.

To import these elements, use the following import statement:

```python
from langstring import LangString, SetLangString, MultiLangString, Controller, GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag, Converter
```

### Basic Usage

1. **LangString** is used to handle a string in a specific language.

   ```python
   from langstring import LangString

   # Create a LangString object
   lang_str = LangString("Hello, World!", "en")

   # Print the string representation
   print(lang_str)  # Output: "Hello, World!"@en
   ```

2. **SetLangString** allows you to handle a set of strings in a specific language.

   ```python
   from langstring import SetLangString

   # Create a SetLangString object
   set_lang_str = SetLangString({"Hello", "Hi"}, "en")

   # Print the set of strings
   print(set_lang_str)  # Output: {'Hello', 'Hi'}@en
   ```

3. **MultiLangString** manages strings in multiple languages.

   ```python
   from langstring import MultiLangString

   # Create a MultiLangString object
   multi_lang_str = MultiLangString({"en": {"Hello", "Hi"}, "es": {"Hola"}})

   # Print the multilingual string representation
   print(multi_lang_str)  # Output: en: {'Hello', 'Hi'}, es: {'Hola'}
   ```

4. **Controller** and **Flags** are used to manage global and specific language string states.

   ```python
   from langstring import Controller, GlobalFlag

   # Set a flag
   Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)

   # Print the state of a specific flag
   Controller.print_flag(GlobalFlag.LOWERCASE_LANG)  # Output: GlobalFlag.LOWERCASE_LANG = True
   ```

5. **Converter** is used to convert language strings between different formats.

   ```python
   from langstring import Converter, LangString, SetLangString, MultiLangString

   # Convert a string to a LangString using the 'manual' method
   langstring = Converter.from_string_to_langstring("manual", "Hello", "en")
   print(langstring)  # Output: "Hello"@en

   # Convert a list of strings to a list of LangStrings using the 'parse' method
   langstrings = Converter.from_strings_to_langstrings("parse", ["Hello@en", "Bonjour@fr"], separator="@")
   for ls in langstrings:
       print(ls)  # Output: "Hello"@en
                  #         "Bonjour"@fr
   ```


## Basic Reference

### Classes

#### LangString Class

The `LangString` class encapsulates a string along with its associated language information. It is designed to work seamlessly with text strings that require language tags, providing functionalities such as validation of language tags, handling of empty strings, and enforcement of constraints through control flags. It is also possible to validate language tags using the `langcodes` library, ensuring that the language information is accurate.

Using the `LangString` class is beneficial when you need to manage multilingual text data in your applications. It is particularly useful in scenarios where strings need to be associated with specific languages, such as in internationalization and localization projects, or when processing text data that must be tagged with its language for further analysis or processing. The class can be utilized in any context where you need to ensure the integrity of language-tagged strings, enhancing data consistency and reducing errors.

To use the `LangString` class, simply create an instance by providing the text and the corresponding language tag. The class supports many standard string operations, which have been overridden to return `LangString` objects, allowing for seamless integration and extended functionality. For example, you can concatenate two `LangString` objects, convert the text to uppercase, or check if the text contains a specific substring, all while maintaining the associated language tag. This makes it easy to work with multilingual text data as if you were handling regular strings, but with the added benefit of language context.

Note that in this library's context, language tags are case-insensitive, meaning `en`, `EN`, `En`, and `eN` are considered equivalent. However, subtags such as `en`, `en-UK`, and `en-US` are treated as distinct entities. Additionally, spaces in language tags are not automatically trimmed unless the classes' `STRIP_LANG` flags are set to True. As an example, `"en"` is not considered equal to `"en "`. However, if the `STRIP_LANG` flag is set to True, `"en "` will be converted to `"en"`, thereby making the languages equal.


- [Functionalities' Descriptions](https://github.com/pedropaulofb/langstring/blob/main/documentation/methods_langstring.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/langstring/)

#### SetLangString Class

The `SetLangString` class is a structure designed to encapsulate a set of strings with a common language tag. This class provides a way to manage collections of text strings, ensuring that each string within the set is associated with a specified language tag. By using the `SetLangString` class, you can easily handle multilingual datasets, validate language tags, and manage string sets with enhanced functionality compared to standard Python sets.

Using `SetLangString` is beneficial when working with multilingual text data, as it integrates validation mechanisms and control flags to enforce constraints such as non-empty text strings and valid language tags. This ensures data integrity and consistency across your application. The class also overrides many standard set methods to return `SetLangString` objects, allowing seamless integration and extending the functionality of regular sets. This makes it an excellent choice for developers needing a more sophisticated way to manage and manipulate text data in different languages.

You should consider using `SetLangString` when you need to manage sets of text strings that are tagged with specific languages, such as in internationalization and localization projects, or when handling datasets that require strict validation of language tags. The `SetLangString` class makes it straightforward to add, remove, and manipulate text strings while maintaining the association with their respective language tags. For example, you can create a `SetLangString` object, add new strings, check for the existence of a string, and perform set operations like union and intersection, all while preserving language tag integrity.

- [Functionalities' Descriptions](https://github.com/pedropaulofb/langstring/blob/main/documentation/methods_setlangstring.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/setlangstring/)

#### MultiLangString Class

The `MultiLangString` class is designed to manage and manipulate multilingual text strings, providing a flexible and efficient way to handle multilingual content in various applications. It uses a dictionary to store text entries associated with language tags, allowing easy representation and manipulation of text in different languages. The class supports adding new entries, removing entries, and retrieving entries based on specific languages or across all languages. Additionally, it allows setting a preferred language, which can be used as a default for operations involving text retrieval.

Using `MultiLangString` is beneficial when you need to manage and organize text data in multiple languages within your application. This class integrates seamlessly with other components like `LangString` and `SetLangString`, offering extensive functionality for handling multilingual text data. By encapsulating text entries within a structured dictionary, it ensures that language-specific data is maintained with integrity, making it ideal for internationalization and localization projects. Furthermore, the class provides methods for merging multilingual data, validating inputs, and performing various set operations, enhancing its utility in complex multilingual environments.

You should consider using `MultiLangString` when your application requires management of text data in multiple languages. The class simplifies tasks like adding new language entries, retrieving texts in a specific language, and ensuring data consistency across languages. For instance, you can create a `MultiLangString` object, add or remove text entries in different languages, and easily access or manipulate these entries as needed.

- [Functionalities' Descriptions](https://github.com/pedropaulofb/langstring/blob/main/documentation/methods_multilangstring.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/multilangstring/)

#### Controller Class

The `Controller` class is a non-instantiable class (hence, it provides only static methods) designed to manage and manipulate [configuration flags](#configuration-via-flags) for the `LangString`, `SetLangString`, and `MultiLangString` classes. By centralizing the management of these flags, the `Controller` ensures consistent behavior and validation rules across the entire system. The class offers methods to set, retrieve, print, and reset these flags.

Using the `Controller` is beneficial because it enforces uniformity and reduces the potential for configuration errors across different parts of the application. It allows developers to dynamically adjust the behavior of multilingual text handling classes at runtime, catering to various needs and use cases. The centralized flag management system simplifies the maintenance and debugging processes, making it easier to track and modify configuration states.

You should use the `Controller` class when you need to enforce specific constraints or behaviors across multiple instances of multilingual text classes. It is especially useful in applications that require dynamic adjustments to text handling rules, such as ensuring non-empty strings, validating language codes, or controlling the inclusion of quotes and language tags in output. To use the `Controller`, simply call its class methods to set or get flag values, print the current states, or reset flags to their default settings. For example, `Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)` will set the lowercase language flag to true, affecting all relevant text handling classes.

- [Functionalities' Descriptions](https://github.com/pedropaulofb/langstring/blob/main/documentation/methods_controller.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/controller/)


#### Converter Class

The `Converter` class is a utility class designed to facilitate conversions between different string types used in language processing, specifically regular `str`, `LangString`, `SetLangString`, and `MultiLangString`. These string types are integral to managing and manipulating multilingual text data, ensuring that language-specific text handling is seamless. The `Converter` class provides a range of static methods to perform these conversions.

Using the `Converter` class ensures compatibility and ease of use when transforming between various string representations. This is particularly beneficial in scenarios where data interchange between different components or modules is required. By leveraging the `Converter`, developers can maintain consistency in data representation and avoid common pitfalls associated with manual string manipulation. The utility nature of the class, providing only static methods streamlines its integration into different parts of an application.

The `Converter` class should be used whenever there is a need to convert between regular `str`, `LangString`, `SetLangString`, and `MultiLangString` objects. For instance, if an application requires converting a list of language-tagged strings into a unified multilingual format, the `Converter` provides the necessary methods to accomplish this efficiently. By calling methods like `Converter.from_string_to_langstring()` or `Converter.from_langstring_to_multilangstring()`, developers can perform these conversions with minimal code and maximum reliability.


- [Functionalities' Descriptions](https://github.com/pedropaulofb/langstring/blob/main/documentation/methods_converter.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/converter/)

### Configuration via Flags

The configuration of behavior in this library is managed through a robust system of flags. These flags are predefined settings that control various aspects of how the library functions, allowing users to tailor its behavior to meet specific requirements. By adjusting these flags, users can enable or disable features, modify processing rules, and optimize performance for their particular use case. The flags are designed to be easily configurable, providing a flexible way to manage the library’s behavior without altering the underlying code.

Configuring behavior using flags is essential for several reasons. Firstly, it provides a high level of customization, enabling users to fine-tune the library’s operations to better align with their specific needs and workflows. This customization can lead to improved efficiency and effectiveness, as the library can be adapted to handle specific tasks more optimally. Additionally, configuring flags allows for better maintenance and scalability. As requirements evolve, users can adjust the flags to meet new demands without the need for significant code changes, thus ensuring the library remains versatile and future-proof.

Users should configure flags when they need to modify the default behavior of the library to suit their particular needs. For example, if a user needs to process multilingual data differently, they can set the appropriate flags to adjust the handling of language-tagged strings. Configurations can be made at the beginning of a session or dynamically throughout the usage of the library, depending on the context. To configure a flag, users simply need to call the `Controller` class’s methods designed for this purpose, such as `Controller.set_flag(flag_name, value)`. This straightforward approach makes it easy to manage and update configurations, ensuring the library operates as intended for any given application.

- [Flags' List](https://github.com/pedropaulofb/langstring/blob/main/documentation/flags_list.md)
- [Documentation with Examples](https://pedropaulofb.github.io/langstring/autoapi/langstring/flags/)

### Elements' Relationships

The elements of the library are interconnected to handle and manipulate multilingual data. Understanding these relationships is important for understanding the library's operations and how its components interact.

At the core are the Controller and flags, which manage configurations and settings. The `Controller` class interacts directly with the main data handling classes: `LangString`, `SetLangString`, and `MultiLangString`. The flags, manipulated via the `Controller`, provides the settings that dictate how the other classes should behave, allowing customization based on user requirements.

The data handling classes (`LangString`, `SetLangString`, and `MultiLangString`) are the backbone of the library, providing structures for representing and manipulating language-tagged strings. These classes are used by the `Converter` class, which offers functions for converting between these string types. This conversion ensures compatibility and ease of use across language processing tasks.

In summary, the `Controller` and the flags define and manage configurations. The core data handling classes (`LangString`, `SetLangString`, `MultiLangString`) are manipulated based on these configurations and are used by the `Converter` class to enable transformations between different string representations. This structure, represented in the image below, allows the library to provide solutions for multilingual data processing.

<p align="center">
  <img src="https://raw.githubusercontent.com/pedropaulofb/langstring/main/documentation/import_schema_basic.png" alt="Basic Import Scheme" style="width:500px">
</p>

## Testing

The LangString Python Library is rigorously tested to ensure robustness and reliability. We have achieved 100% test coverage, with tests implemented for each method provided by the library. This ensures that every aspect of the library is thoroughly validated and any potential issues are caught early.

### Test Organization

The tests are organized into [several directories](https://github.com/pedropaulofb/langstring/tree/main/tests), each focusing on different components of the library:

- `tests_langstring`: Tests for the core LangString functionalities.
- `tests_utils`: Utility tests to ensure the correctness of helper functions.
- `tests_setlangstring`: Tests for SetLangString functionalities.
- `tests_multilangstring`: Tests for MultiLangString functionalities.
- `tests_converter`: Tests for Conversor functionalities.
- `tests_controller`: Tests for Controller functionalities.

### Running the Tests

To run the tests, you can use the following command in the command line within the test directory of the project:

```sh
pytest
```

This command will execute all the tests and provide a detailed report on the coverage and any potential issues.

### Continuous Integration

We use GitHub Actions to automatically run our tests on every push to the repository. The [Action's workflow](https://github.com/pedropaulofb/langstring/blob/main/.github/workflows/code_testing.yml) execute the tests across multiple operating systems and Python versions to ensure compatibility and reliability.

- **Operating Systems**: Windows, Linux, and macOS.
- **Python Versions**: 3.11 and 3.12.

## How to Contribute

We welcome and appreciate contributions from the community! Whether you want to report a bug, suggest a new feature, or improve our codebase, your input is valuable.

### Reporting Issues

- If you find a bug or wish to suggest a feature, please [open a new issue](https://github.com/pedropaulofb/langstring/issues/new).
- If you notice any discrepancies in the documentation created with the aid of AI, feel free to [report them by opening an issue](https://github.com/pedropaulofb/langstring/issues/new).

### Code Contributions

1. Fork the project repository and create a new feature branch for your work: `git checkout -b feature/YourFeatureName`.
2. Make and commit your changes with descriptive commit messages.
3. Push your work back up to your fork: `git push origin feature/YourFeatureName`.
4. Submit a pull request to propose merging your feature branch into the main project repository.

### Test Contributions

- Enhance the project's reliability by adding new tests or improving existing ones.

### General Guidelines

- Ensure your code follows our coding standards.
- Update the documentation as necessary.
- Make sure your contributions do not introduce new issues.

We appreciate your time and expertise in contributing to this project!

## Related Libraries and Differences

The LangString Library offers unique functionalities for handling multilingual text in Python applications. While there are several libraries and tools available for internationalization, localization, and language processing, they differ from the LangString Library in scope and functionality. Below is an overview of related work and how they compare to the LangString library:

- **Babel**
    - https://pypi.org/project/Babel/
    - Babel is a Python library for internationalization and localization. It primarily focuses on formatting dates, numbers, and currency values for different locales.
    - Difference: Unlike Babel, the LangString Library specifically manages multilingual text strings, providing a more direct approach to handling language-specific text data.

- **gettext**
    - https://pypi.org/project/python-gettext/
    - gettext is a GNU system used for internationalizing applications. It allows for translating fixed strings in different languages using message catalogs.
    - Difference: The LangString Library, in contrast, is designed for dynamic management of multilingual content, not just for translation of static strings.

- **langcodes**
    - https://pypi.org/project/langcodes/
    - langcodes provides tools for parsing and understanding language tags.
    - Difference: While langcodes is useful for handling language codes, the LangString Library extends beyond this by managing actual multilingual text strings associated with these codes.

- **Polyglot**
    - https://pypi.org/project/polyglot/
    - Polyglot is a natural language pipeline that supports multiple languages for various NLP tasks.
    - Difference: Polyglot focuses on language processing rather than the structured management of multilingual text, which is the core functionality of the LangString Library.

- **CLD3**
    - https://pypi.org/project/gcld3/
    - Google's CLD3 is a model for language identification.
    - Difference: CLD3 is specialized in detecting the language of a text, whereas the LangString Library is about storing and manipulating text in multiple languages.

- **spaCy**
    - https://pypi.org/project/spacy/
    - spaCy is a comprehensive NLP library that supports multiple languages.
    - Difference: spaCy is geared towards analyzing text, not managing it. The LangString Library, on the other hand, is designed for the structured handling and storage of multilingual text.

In summary, while these related tools and libraries offer valuable functionalities for internationalization, localization, and language processing, the LangString Library has specific focus on managing and manipulating multilingual text strings in a structured and efficient manner.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/pedropaulofb/langstring/blob/main/LICENSE) file for details.

## Author

The LangString library is developed and maintained by:

- Pedro Paulo Favato Barcelos [[GitHub](https://github.com/pedropaulofb)] [[LinkedIn](https://www.linkedin.com/in/pedro-paulo-favato-barcelos/)]

Feel free to reach out using the provided links. For inquiries, contributions, or to report any issues, you can [open a new issue](https://github.com/pedropaulofb/langstring/issues/new) on this repository.
