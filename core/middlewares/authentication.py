# from typing import Optional, Tuple
# from core.dependencies.auth import TokenHelper
# from fastapi import HTTPException

# import jwt
# from starlette.authentication import AuthenticationBackend
# from starlette.middleware.authentication import (
#     AuthenticationMiddleware as BaseAuthenticationMiddleware,
# )
# from starlette.requests import HTTPConnection

# from core.env import config
# from modules.users.schemas import BaseUser

# '''
# TODO: Check for permissions here and call from dependencies
# '''
# class AuthBackend(AuthenticationBackend):
#     async def authenticate(
#         self, conn: HTTPConnection
#     ) -> Tuple[bool, Optional[BaseUser]]:
#         current_user: BaseUser = None
#         authorization: str = conn.headers.get("Authorization")
#         if not authorization:
#             return False, current_user

#         try:
#             scheme, credentials = authorization.split(" ")
#             if scheme.lower() != "bearer":
#                 return False, current_user
#         except ValueError:
#             return False, current_user

#         if not credentials:
#             return False, current_user
#         try:
#             current_user: BaseUser = TokenHelper.decode(
#                 credentials
#             )
#         except jwt.exceptions.PyJWTError:
#             return False, current_user            
            
#         return True, current_user


# class AuthenticationMiddleware(BaseAuthenticationMiddleware):
#     pass
