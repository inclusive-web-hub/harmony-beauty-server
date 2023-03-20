"""The users models module"""

from datetime import (
    datetime,
)
from enum import Enum
from odmantic import (
    Field,
    Index,
    Model,
)
from pydantic import (
    EmailStr,
)
from typing import (
    Optional,
)


class UserStatus(int, Enum):
    """
    The UserStatus enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    ACTIVE = 1
    DISABLED = 0


class UserRole(str, Enum):
    """
    The UserRole enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    REGULAR = "regular"
    ADMIN = "admin"


class User(Model):
    """
    The User model

    Args:
        Model (odmantic.Model): Odmantic base model.
    """

    full_name: str = Field(index=True)
    birthday: Optional[str] = Field(default="")
    bio: Optional[str] = Field(default="")
    email: EmailStr = Field(index=True)
    password: str = Field(index=True)
    profile_picture: Optional[str] = Field(default="")
    phone_number: Optional[str] = Field(default="")
    user_status: Optional[UserStatus] = Field(default=UserStatus.ACTIVE.value)
    user_role: Optional[UserRole] = Field(default=UserRole.REGULAR.value)
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        """
        The User Config class.
        """

        @staticmethod
        def indexes() -> Index:
            """
            Indexes definition.

            Yields:
                Index: return a compound index on the email and password fields,
            """
            yield Index(User.email, User.password, name="email_password_index")


__all__ = [
    "UserStatus",
    "UserRole",
    "User",
]
