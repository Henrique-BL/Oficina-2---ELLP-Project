import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_sector(client_test, sector_data):
    client = client_test
    response =  client.post("/sectors/", json=sector_data)
    assert response.status_code == status.HTTP_201_CREATED
    

@pytest.mark.asyncio
async def test_get_sectors(client_test, sector_data, volunteer_data):
    client = client_test

    client.post("/sectors/", json=sector_data)
    response = client.get("/sectors/")
    
    print('Response', response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == sector_data["name"]

@pytest.mark.asyncio
async def test_get_sector_by_id(client_test, sector_data):
    client = client_test
    sector = client.post("/sectors/", json=sector_data)
    data = sector.json()
    sector_id = data["id"]

    response = client.get(f"/sectors/{sector_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sector_id
    assert data["name"] == sector_data["name"]