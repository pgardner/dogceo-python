import httpx
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Dog CEO API Client",
    description="A FastAPI wrapper for the Dog CEO API",
    version="1.0.0"
)

# Base URL for the Dog CEO API
BASE_URL = "https://dog.ceo/api"

# Pydantic models for responses
class DogApiResponse(BaseModel):
    status: str
    message: Union[str, List[str], Dict[str, List[str]], List[Dict[str, Any]]]

class AllBreedsResponse(BaseModel):
    status: str
    message: Dict[str, List[str]]

class BreedsListResponse(BaseModel):
    status: str
    message: List[str]

class RandomImageResponse(BaseModel):
    status: str
    message: str

class MultipleImagesResponse(BaseModel):
    status: str
    message: List[str]

# HTTP client for making requests
async def make_request(endpoint: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{endpoint}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from Dog CEO API")
        return response.json()

# Routes for Breeds
@app.get("/breeds/list/all", response_model=AllBreedsResponse, tags=["breeds"])
async def get_all_breeds():
    """
    Get all dog breeds and their sub-breeds
    """
    return await make_request("/breeds/list/all")

@app.get("/breeds/list", response_model=BreedsListResponse, tags=["breeds"])
async def get_primary_breeds():
    """
    Get a list of all primary dog breeds
    """
    return await make_request("/breeds/list")

@app.get("/breed/{breed}/list", response_model=BreedsListResponse, tags=["breeds"])
async def get_sub_breeds(
    breed: str = Path(..., description="The breed name")
):
    """
    Get a list of sub-breeds for a specific breed
    """
    return await make_request(f"/breed/{breed}/list")

# Routes for Images
@app.get("/breeds/image/random", response_model=RandomImageResponse, tags=["images"])
async def get_random_image():
    """
    Get a random dog image from any breed
    """
    return await make_request("/breeds/image/random")

@app.get("/breeds/image/random/{count}", response_model=MultipleImagesResponse, tags=["images"])
async def get_multiple_random_images(
    count: int = Path(..., description="Number of images to return", ge=1, le=50)
):
    """
    Get multiple random dog images from any breed
    """
    return await make_request(f"/breeds/image/random/{count}")

@app.get("/breed/{breed}/images", response_model=MultipleImagesResponse, tags=["images"])
async def get_breed_images(
    breed: str = Path(..., description="The breed name")
):
    """
    Get all images for a specific breed
    """
    return await make_request(f"/breed/{breed}/images")

@app.get("/breed/{breed}/images/random", response_model=RandomImageResponse, tags=["images"])
async def get_random_breed_image(
    breed: str = Path(..., description="The breed name")
):
    """
    Get a random image for a specific breed
    """
    return await make_request(f"/breed/{breed}/images/random")

@app.get("/breed/{breed}/images/random/{count}", response_model=MultipleImagesResponse, tags=["images"])
async def get_multiple_random_breed_images(
    breed: str = Path(..., description="The breed name"),
    count: int = Path(..., description="Number of images to return", ge=1, le=50)
):
    """
    Get multiple random images for a specific breed
    """
    return await make_request(f"/breed/{breed}/images/random/{count}")

@app.get("/breed/{breed}/{sub_breed}/images", response_model=MultipleImagesResponse, tags=["images"])
async def get_sub_breed_images(
    breed: str = Path(..., description="The breed name"),
    sub_breed: str = Path(..., description="The sub-breed name")
):
    """
    Get all images for a specific sub-breed
    """
    return await make_request(f"/breed/{breed}/{sub_breed}/images")

@app.get("/breed/{breed}/{sub_breed}/images/random", response_model=RandomImageResponse, tags=["images"])
async def get_random_sub_breed_image(
    breed: str = Path(..., description="The breed name"),
    sub_breed: str = Path(..., description="The sub-breed name")
):
    """
    Get a random image for a specific sub-breed
    """
    return await make_request(f"/breed/{breed}/{sub_breed}/images/random")

@app.get("/breed/{breed}/{sub_breed}/images/random/{count}", response_model=MultipleImagesResponse, tags=["images"])
async def get_multiple_random_sub_breed_images(
    breed: str = Path(..., description="The breed name"),
    sub_breed: str = Path(..., description="The sub-breed name"),
    count: int = Path(..., description="Number of images to return", ge=1, le=50)
):
    """
    Get multiple random images for a specific sub-breed
    """
    return await make_request(f"/breed/{breed}/{sub_breed}/images/random/{count}")

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": str(exc.detail)},
    )

# Root endpoint
@app.get("/", tags=["info"])
async def root():
    return {
        "name": "Dog CEO API Client",
        "description": "A FastAPI wrapper for the Dog CEO API",
        "documentation": "/docs",
        "original_api": "https://dog.ceo/dog-api/"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
