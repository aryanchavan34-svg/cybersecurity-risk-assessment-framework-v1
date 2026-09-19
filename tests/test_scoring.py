from app.app import calculate_criticality

def test_critical_asset():
    score, level = calculate_criticality(5, 5, 4)
    assert score == 4.67
    assert level == "Critical"

def test_medium_asset():
    score, level = calculate_criticality(2, 2, 2)
    assert score == 2.0
    assert level == "Medium"
