import pytest
from uuid import uuid4
from fastapi import status

@pytest.mark.asyncio
async def test_create_volunteer(client_test, volunteer_data, sector_data):
    client = client_test

    response =  client.post("/volunteers/", json=volunteer_data)
    print('Response', response.json())
    assert response.status_code == status.HTTP_201_CREATED
    
@pytest.mark.asyncio
async def test_create_volunteer_invalid_sector(client_test, volunteer_data):
    client = client_test
    invalid_data = volunteer_data.copy()

    response = client.post("/volunteers/", json=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_volunteers(client_test, sector_data, volunteer_data):
    client = client_test
    client.post("/volunteers/", json=volunteer_data)

    response = client.get("/volunteers/")
    
    print('Response', response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == volunteer_data["name"]


@pytest.mark.asyncio
async def test_get_volunteer_by_id(client_test, volunteer_data, sector_data):
    client = client_test
    response = client.post("/volunteers/", json=volunteer_data)
    data = response.json()
    volunteer_id = data["id"]

    response = client.get(f"/volunteers/{volunteer_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == volunteer_id
    assert data["name"] == volunteer_data["name"]
