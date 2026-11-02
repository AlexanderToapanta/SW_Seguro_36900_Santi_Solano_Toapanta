from typing import ClassVar
from pydantic import BaseModel, ConfigDict, model_validator


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class PatchModel(InputModel):
    nullable_fields: ClassVar[set[str]] = set()

    @model_validator(mode="before")
    @classmethod
    def reject_null_required_fields(cls, value):
        # Omitir un campo en PATCH no equivale a borrar su valor con null.
        if isinstance(value, dict):
            for field, content in value.items():
                if content is None and field not in cls.nullable_fields:
                    raise ValueError(f"{field} no puede ser null")
        return value
