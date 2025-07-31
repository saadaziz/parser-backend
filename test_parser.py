from parser import parse_listing

def test_parse_listing():
    sample = "Asking Price: $125,000\nRevenue: $500,000\n"
    result = parse_listing(sample)
    assert result["asking_price"] == 125000
    assert result["revenue"] == 500000
