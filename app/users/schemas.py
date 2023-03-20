"""The users schemas module"""

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
    List,
    Optional,
)


class UserObjectSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for fetching user info.
    """

    id: str = Field(..., example="6386fc625c60cfd607e97b44")
    full_name: str = Field(..., example="Your full name.")
    bio: Optional[str] = Field(..., example="bio.")
    birthday: Optional[str] = Field(..., example=str(datetime.utcnow().date()))
    email: EmailStr = Field(..., example="user@test.com")
    profile_picture: Optional[str] = Field(
        ..., example="A relative URL to Deta Drive."
    )
    user_status: Optional[int] = Field(default=1)
    user_role: Optional[str] = Field(default="regular")
    phone_number: Optional[str] = Field(default="12314")


class UserLoginSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for the login endpoint.
    """

    email: EmailStr = Field(..., example="testing@gmail.com")
    password: str = Field(..., example="A secure password goes here.")


class UserSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for response.
    """

    user: Optional[UserObjectSchema] = Field(
        ...,
        example=UserObjectSchema(
            id="asdWQdqw123",
            full_name="Your full name.",
            birthday=str(datetime.utcnow().date()),
            bio="your bio",
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


class UsersSchema(BaseModel):
    """
    A Pydantic class that defines the users schema for the all users endpoint.
    """

    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    result: List[UserObjectSchema] = Field(
        ...,
        example=[
            UserObjectSchema(
                id="asdWQdqw123",
                full_name="Your full name.",
                birthday=str(datetime.utcnow().date()),
                bio="your bio",
                email="user@test.com",
                profile_picture="A relative URL to Deta Drive.",
            ),
        ],
    )


class ResetPassword(BaseModel):
    """
    A Pydantic class that defines the users schema for the reset password endpoint.
    """

    old_password: str = Field(..., example="Your old password.")
    new_password: str = Field(..., example="Your new password.")
    confirm_password: str = Field(..., example="Your new password.")


class PersonalInfo(BaseModel):
    """
    A Pydantic class that defines the users schema for the updating user info.
    """

    full_name: str = Field(..., example="Full name.")
    bio: str = Field(..., example="bio.")
    birthday: str = Field(..., example="birthday.")
    phone_number: str = Field(..., example="123456789")
