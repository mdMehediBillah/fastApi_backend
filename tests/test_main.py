import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch
from server3.app.main import app

client = TestClient(app)

# Mock function to replace load_data()
def mock_load_data():
    return pd.DataFrame({
        "ISOTwoLetterCountryCode": ["US", "DE"],
        "Value": [100, 200]
    })


# Test the GET /data endpoint
def test_get_all_data():
    with patch("server3.app.main.load_data", side_effect=mock_load_data):  
        response = client.get("/data")

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert "headers" in response.json()
    assert "data" in response.json()



# Test the GET / Home or root endpoint
def test_read_root():
    response = client.get("/")  
    assert response.status_code == 200  
    assert response.json() == {"message": "Welcome to FastAPI!"}  




# Test the GET /data/country/{country_code} endpoint
@patch("server3.app.main.load_data", side_effect=mock_load_data)
def test_get_data_by_country(mock_load):
    response = client.get("/data/country/US")

    assert response.status_code == 200
    json_data = response.json()

    assert isinstance(json_data, list)  
    assert len(json_data) > 0  
    assert all(item["ISOTwoLetterCountryCode"] == "US" for item in json_data)  

    response = client.get("/data/country/DE")

    assert response.status_code == 200
    json_data = response.json()

    assert isinstance(json_data, list)
    assert len(json_data) > 0  
    assert all(item["ISOTwoLetterCountryCode"] == "DE" for item in json_data)  
