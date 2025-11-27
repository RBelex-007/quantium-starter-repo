import pytest
from dashboard import app

@pytest.fixture
def dash_app():
    """Fixture to set up the Dash app for testing"""
    return app

def test_header_present(dash_app):
    """Test that the header is present in the dashboard"""
    header = dash_app.layout.children[0]
    assert header.children == "Pink Morsel Sales Dashboard"

def test_visualization_present(dash_app):
    """Test that the graph visualization is present"""
    card = dash_app.layout.children[2]
    graph_div = card.children[1]
    assert graph_div.id == 'sales-graph'

def test_region_picker_present(dash_app):
    """Test that region buttons are present"""
    card = dash_app.layout.children[2]
    buttons_div = card.children[0]
    button_ids = [btn.id for btn in buttons_div.children]
    expected_buttons = ['btn-all', 'btn-north', 'btn-east', 'btn-south', 'btn-west']
    assert button_ids == expected_buttons