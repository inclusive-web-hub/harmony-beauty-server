"""Auth Schemas module."""

from datetime import (
    datetime,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Dict,
    Optional,
)

from app.users import (
    schemas as users_schemas,
)


class UserSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for registration.
    """

    user: Optional[users_schemas.UserObjectSchema] = Field(
        ...,
        example=users_schemas.UserObjectSchema(
            id="asdWQdqw123",
            full_name="Your full name.",
            bio="Your bio",
            birthday=str(datetime.utcnow().date()),
            email="user@test.com",
            profile_picture="A relative URL to Deta Drive.",
        ),
    )
    token: Optional[Dict[str, str]] = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )
    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    message: str = Field(
        ...,
        example="A message to indicate whether or not the login was successful!",
    )


class UserLoginSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for logging in.
    """

    email: EmailStr = Field(..., example="Your email address to log in.")
    password: str = Field(..., example="A secure password goes here.")


class UserCreate(BaseModel):
    """
    A Pydantic class that defines the user schema for sign up.
    """

    full_name: str = Field(..., example="Your full name.")
    email: EmailStr = Field(..., example="user@test.com")
    password: str = Field(..., example="A secure password goes here.")


class Token(BaseModel):
    """
    A Pydantic class that defines the Token schema.
    """

    access_token: str = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )


class TokenData(BaseModel):
    """
    A Pydantic class that defines a Token schema to return the email address.
    """

    email: Optional[str] = Field(..., example="Your email address.")


class ResponseSchema(BaseModel):
    """
    A Pydantic class that defines a Response schema object.
    """

    status_code: int = Field(
        ...,
        example=400,
    )
    message: str = Field(
        ...,
        example="A message to indicate that the request was not successful!",
    )
