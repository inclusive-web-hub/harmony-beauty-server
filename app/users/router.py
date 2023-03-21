"""The users router module"""

from deta import Deta
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    responses,
)
from fastapi.encoders import (
    jsonable_encoder,
)
from odmantic.session import (
    AIOSession,
)
from typing import (
    Any,
    Dict,
    Union,
)

from app.config import (
    settings,
)
from app.users import (
    crud as users_crud,
    schemas as users_schemas,
)
from app.utils import (
    dependencies,
    jwt,
)

router = APIRouter(prefix="/api/v1")

# initialize with a project key
deta = Deta(settings().DETA_PROJECT_KEY)

# create and use as many Drives as you want!
profile_images = deta.Drive("profile-images")


@router.get("/user/profile", response_model=users_schemas.UserSchema)
async def get_user_profile(
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
) -> Dict[str, Any]:
    """
    Get user profile info given a token provided in a request header.
    """
    results = {
        "token": None,
        "user": users_schemas.UserObjectSchema(
            **jsonable_encoder(current_user)
        ),
        "status_code": 200,
        "message": "Welcome to Harmony Beauty.",
    }
    return results


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt.get_token_user),
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Log out a user from the app by removing the access token from the list.
    """
    await users_crud.remove_token(current_user.id, token, session)
    return {"status": 200, "message": "Good Bye!"}


@router.put("/user/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Upload an image to a Deta drive.
    """
    try:
        file_name = "user/" + str(current_user.id) + "/" + "profile.png"
        profile_images.put(file_name, file.file)
        await users_crud.update_profile_picture(
            email=current_user.email, file_name=file_name, session=session
        )
        return {
            "status_code": 200,
            "message": "Profile picture has been uploaded successfully!",
        }

    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}


@router.get("/user/{user_id}/profile.png")
async def get_profile_user_image(
    user_id: str,
) -> Union[responses.StreamingResponse, Dict[str, Any]]:
    """
    An endpoint for streaming images.
    """
    try:
        img = profile_images.get(f"user/{user_id}/profile.png")
        return responses.StreamingResponse(
            img.iter_chunks(), media_type="image/png"
        )
    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}


@router.put("/user/reset-password")
async def reset_user_password(
    request: users_schemas.ResetPassword,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    An endpoint for resetting users passwords.
    """
    result = await users_crud.update_user_password(
        request, current_user.email, session
    )
    return result


@router.put("/user/profile")
async def update_personal_information(
    personal_info: users_schemas.PersonalInfo,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    An endpoint for updating users personel info.
    """
    await users_crud.update_user_info(personal_info, current_user, session)
    return {
        "status_code": 200,
        "message": "Your personal information has been updated successfully!",
    }
