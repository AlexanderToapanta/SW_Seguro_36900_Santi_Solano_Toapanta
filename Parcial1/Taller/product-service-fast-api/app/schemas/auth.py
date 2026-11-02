from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class AuthenticatedUser(BaseModel):

    userId: UUID

    username: str

    email: str

    roles: list[str] = Field(
        default_factory=list,
    )

    @field_validator("roles")
    @classmethod
    def normalize_roles(
        cls,
        values: list[str],
    ) -> list[str]:

        return sorted(
            {
                role
                .strip()
                .upper()
                for role in values
                if role.strip()
            }
        )