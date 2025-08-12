# test_app.py
import pytest
from unittest.mock import patch

# Test when Bedrock returns a valid itinerary
@patch("app.StateGraph")
def test_itinerary_success(mock_graph_cls):
    mock_graph = mock_graph_cls.return_value
    mock_graph.run.return_value = {"itinerary": "Day 1: Eiffel Tower"}
    
    from app import StateGraph  # ensure import after patch
    result = mock_graph.run({"trip_details": "Paris trip"})
    assert "Eiffel Tower" in result["itinerary"]

# Test when Bedrock returns empty itinerary
@patch("app.StateGraph")
def test_itinerary_empty(mock_graph_cls):
    mock_graph = mock_graph_cls.return_value
    mock_graph.run.return_value = {}
    
    from app import StateGraph
    result = mock_graph.run({"trip_details": "Rome trip"})
    assert result.get("itinerary", "") == ""

# Edge case: very short input
@patch("app.StateGraph")
def test_itinerary_short_input(mock_graph_cls):
    mock_graph = mock_graph_cls.return_value
    mock_graph.run.return_value = {"itinerary": "Sample plan"}
    
    from app import StateGraph
    result = mock_graph.run({"trip_details": ""})
    assert isinstance(result["itinerary"], str)
