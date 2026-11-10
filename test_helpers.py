import pytest
import pandas as pd
from coddy.agent import CoddyAgent

def test_extract_file_id():
    agent = CoddyAgent()
    url1 = "https://drive.google.com/file/d/ABC123XYZ/view?usp=sharing"
    assert agent.extract_file_id(url1) == "ABC123XYZ"
    
    url2 = "https://drive.google.com/open?id=XYZ789"
    assert agent.extract_file_id(url2) == "XYZ789"
    
    assert agent.extract_file_id("direct_id") == "direct_id"
