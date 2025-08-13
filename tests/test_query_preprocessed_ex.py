import pytest
from search_engine.core.processed_exact import preprocess_query_ex

@pytest.mark.parametrize("input_text, expected", [
    ("", ""),
    ("Hello, world!", "hello world"),
    ("well-being", "wellbeing"),
    ("OpenAI", "openai"),
])

def test_preprocess_query_ex(input_text, expected):
    assert preprocess_query_ex(input_text) == expected