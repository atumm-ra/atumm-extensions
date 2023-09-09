from pydantic import BaseModel, EmailStr, Field


class CurrentUser(BaseModel):
    class Config:
        validate_assignment = True

    email: EmailStr = Field(None, description="Email")
    id: str = Field(None, description="ID")
