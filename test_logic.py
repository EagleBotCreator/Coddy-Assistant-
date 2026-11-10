import pytest
import pandas as pd
from coddy.agent import CoddyAgent

def test_groupby_aggregate():
    agent = CoddyAgent()
    df = pd.DataFrame({
        "region": ["North", "North", "South"],
        "price": [100, 200, 300]
    })
    agent.load_csv("dummy", df=df)
    res = agent.group_by_aggregate("region", "price", "sum")
    assert "North" in res
    assert "300" in res
    assert "South" in res
    assert "300" in res
