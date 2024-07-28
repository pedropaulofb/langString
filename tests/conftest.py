"""This module contains pytest fixtures and configurations used across various test modules in the application.

The fixtures defined here are automatically discovered and utilized by pytest in all test modules. This allows for
consistent setup and teardown processes across multiple tests, ensuring a clean testing environment.
"""

import pytest
from langstring import Controller


@pytest.fixture(autouse=True)
def reset_configurations() -> None:
    """Reset automatically all controllable configurations before each test.

    Resets configurations in the Controller and Controller to False before each test.

    This fixture ensures that each test starts with a clean state regarding the flags used in the
    LangString and MultiLangString modules. It is applied to all tests automatically due to the 'autouse=True' setting.
    """
    Controller.reset_flags()


# CONSTANTS

TYPEERROR_MSG_SINGULAR = r"Invalid argument with value '.*?'. Expected '.*?', but got '.*?'."
TYPEERROR_MSG_PLURAL = r"Invalid argument with value '.+?'. Expected one of '.+?'( or '.+?')*, but got '.+?'\."
TYPEERROR_MSG_GENERAL = r"Invalid argument with value '.+?'. Expected (one of )*'.+?'( or '.+?')*, but got '.+?'\."
