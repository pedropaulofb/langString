"""Specific conftest for multilangstring tests."""

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
