from fastapi import APIRouter

from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.product_categories import router as product_categories_router

api_router = APIRouter()
api_router.include_router(products_router)
api_router.include_router(categories_router)
api_router.include_router(product_categories_router)