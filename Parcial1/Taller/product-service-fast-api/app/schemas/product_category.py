from app.schemas.input import InputModel, PatchModel
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryRead
from app.schemas.product import ProductRead


class ProductCategoryCreate(InputModel):
    product_id: UUID
    category_id: UUID
    estado: bool = True


class ProductCategoryUpdate(PatchModel):
    estado: bool | None = None


class ProductCategoryRead(BaseModel):
    id: UUID
    product_id: UUID
    category_id: UUID
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    product: ProductRead | None = None
    category: CategoryRead | None = None

    model_config = ConfigDict(from_attributes=True)
