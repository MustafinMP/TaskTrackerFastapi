import db_session
from application.exceptions import EmailIsAlreadyExists
from application.services import PasswordHasher
from domain.entities import UserDM
from infrastructure.repositories import UserRepository
from presentation.schemas import AddUserSchema


class UserService:

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_id(user_id)

    @staticmethod
    async def get_user_by_email(user_email: str) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_email(user_email)

    @staticmethod
    async def get_user_by_yandex_uid(uid: int) -> UserDM | None:
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            return await repository.get_by_yandex_id(uid)

    @staticmethod
    async def add_user(user_data: AddUserSchema) -> UserDM:
        hashed_password = PasswordHasher().hash_password(user_data.password)
        async with db_session.create_session() as session:
            repository = UserRepository(session)
            if await repository.exist_by_email(user_data.email):
                raise EmailIsAlreadyExists
            user = await repository.create(
                user_data.name,
                user_data.email,
                hashed_password
            )
            return user
