import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_workshop(client_test, workshop_data):
    client = client_test
    response =  client.post("/workshops/", json=workshop_data)
    print('Response', response.json())
    assert response.status_code == status.HTTP_201_CREATED
    

@pytest.mark.asyncio
async def test_get_workshops(client_test, workshop_data):
    client = client_test
    client.post("/workshops/", json=workshop_data)


    response = client.get("/workshops/")
    
    print('Response', response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == workshop_data["name"]



@pytest.mark.asyncio
async def test_get_workshop_by_id(client_test, workshop_data):
    client = client_test
    response = client.post("/workshops/", json=workshop_data)
    data = response.json()

    workshop_id = data["id"]

    response = client.get(f"/workshops/{workshop_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == workshop_id
    assert data["name"] == workshop_data["name"]

