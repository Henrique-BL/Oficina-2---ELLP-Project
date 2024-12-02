import pytest
from uuid import uuid4
from fastapi import status

@pytest.mark.asyncio
async def test_create_admin(client_test, admin_data):
    client = client_test
    response = client.post("/admins/register/", json=admin_data)
    print(f"response: {response}")
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == admin_data["name"]
    assert data["email"] == admin_data["email"]
    assert "password" not in data  # Ensure password is not returned in response

@pytest.mark.asyncio
async def test_create_admin_duplicate_email(client_test, admin_data):
    client = client_test
    # Create first admin
    client.post("/admins/register", json=admin_data)
    
    # Try to create admin with same email
    response = client.post("/admins/register", json=admin_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_get_admins(client_test, admin_data):
    client = client_test
    # Create an admin first
    client.post("/admins/register/", json=admin_data)
    
    response = client.get("/admins/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == admin_data["name"]
    assert data[0]["email"] == admin_data["email"]
    assert "password" not in data[0]

@pytest.mark.asyncio
async def test_get_admin_by_id(client_test, admin_data):
    client = client_test
    # Create an admin first
    response = client.post("/admins/register/", json=admin_data)
    print(f"response: {response}")
    admin_id = response.json()["id"]

    response = client.get(f"/admins/{admin_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == admin_id
    assert data["name"] == admin_data["name"]
    assert data["email"] == admin_data["email"]
    assert "password" not in data

@pytest.mark.asyncio
async def test_get_admin_by_invalid_id(client_test):
    client = client_test
    invalid_id = str(uuid4())
    
    response = client.get(f"/admins/{invalid_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
