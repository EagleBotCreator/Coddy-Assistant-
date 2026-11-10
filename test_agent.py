import pytest
import pandas as pd
from coddy.agent import CoddyAgent

@pytest.fixture
def sample_agent():
    agent = CoddyAgent()
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "product": ["Widget A", "Widget B", "Widget A"],
        "price": [19.99, 29.99, 49.99],
        "quantity": [1, 2, 5],
        "region": ["North", "South", "East"]
    })
    agent.load_csv("dummy", df=df, file_name="test.csv")
    return agent

def test_load_csv(sample_agent):
    assert sample_agent.current_df is not None
    assert len(sample_agent.current_df) == 3
    assert sample_agent.current_file_name == "test.csv"

def test_describe_columns(sample_agent):
    desc = sample_agent.describe_columns()
    assert "price" in desc
    assert "product" in desc

def test_filter_rows(sample_agent):
    res = sample_agent.filter_rows("price > 25")
    assert "Filtered to 2 rows" in res
    assert len(sample_agent.current_df) == 2
