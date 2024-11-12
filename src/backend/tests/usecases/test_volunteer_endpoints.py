import pytest
from httpx import AsyncClient
from fastapi import status
from app import app

@pytest.mark.asyncio
async def test_create_volunteer(async_session, volunteer_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/atletas/volunteers", json=volunteer_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == volunteer_data["name"]
        assert data["email"] == volunteer_data["email"]
        assert data["phone"] == volunteer_data["phone"]
        assert data["student_code"] == volunteer_data["student_code"]
        assert data["sector"]["name"] == volunteer_data["sector"]["name"]
        assert "id" in data
        assert "created_at" in data

@pytest.mark.asyncio
async def test_create_volunteer_invalid_sector(async_session, volunteer_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        invalid_data = volunteer_data.copy()
        invalid_data["sector"]["name"] = "NonExistentSector"
        
        response = await client.post("/atletas/volunteers", json=invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "sector" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_get_volunteers(async_session, volunteer_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a volunteer
        await client.post("/atletas/volunteers", json=volunteer_data)
        
        # Then get all volunteers
        response = await client.get("/atletas/volunteers")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["name"] == volunteer_data["name"]
        assert data[0]["sector"]["name"] == volunteer_data["sector"]["name"]

@pytest.mark.asyncio
async def test_get_volunteer_by_id(async_session, volunteer_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a volunteer
        create_response = await client.post("/atletas/volunteers", json=volunteer_data)
        created_data = create_response.json()
        volunteer_id = created_data["id"]
        
        # Then get the volunteer by ID
        response = await client.get(f"/atletas/volunteers/{volunteer_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == volunteer_id
        assert data["name"] == volunteer_data["name"]
        assert data["sector"]["name"] == volunteer_data["sector"]["name"]

@pytest.mark.asyncio
async def test_get_volunteer_not_found(async_session):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/atletas/volunteers/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_delete_volunteer(async_session, volunteer_data):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a volunteer
        create_response = await client.post("/atletas/volunteers", json=volunteer_data)
        volunteer_id = create_response.json()["id"]
        
        # Then delete the volunteer
        response = await client.delete(f"/atletas/volunteers/{volunteer_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify volunteer is deleted
        get_response = await client.get(f"/atletas/volunteers/{volunteer_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND