# type: ignore  # noqa: PGH003

import pytest

from blueprintflow.core.settings import load_settings
from blueprintflow.llm.connector import LLMConnector


@pytest.fixture
def default_settings():
    return load_settings()


def test_get_embedding_normal_case(default_settings):
    connector = LLMConnector(models=default_settings.models)
    input_str = "test input"
    result = connector.get_embedding(input_str)
    assert isinstance(result, list), "The result should be a list"
    assert all(isinstance(x, float) for x in result), "All elements should be floats"
