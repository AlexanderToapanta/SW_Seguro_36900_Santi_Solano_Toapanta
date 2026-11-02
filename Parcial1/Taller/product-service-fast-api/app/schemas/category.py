from app.schemas.input import InputModel, PatchModel
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(InputModel):
    codigo: str = Field(min_length=2, max_length=50)
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: str | None = Field(default=None, max_length=1000)
    estado: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(PatchModel):
    nullable_fields = {"descripcion"}
    codigo: str | None = Field(default=None, min_length=2, max_length=50)
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    descripcion: str | None = Field(default=None, max_length=1000)
    estado: bool | None = None


class CategoryRead(CategoryBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_eliminacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
