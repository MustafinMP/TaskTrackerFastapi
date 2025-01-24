from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models import StatusModel
from domain.entities import StatusDM


class StatusRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_id(self, status_id: int) -> StatusDM:
        stmt = select(StatusModel).where(StatusModel.id == status_id)
        status: StatusModel = await self.session.scalar(stmt)
        return StatusDM(
            id=status.id,
            name=status.name,
            color_tag=status.color_tag
        ) if status else None

    async def get_all(self) -> list[StatusDM]:
        stmt = select(StatusModel)
        statuses: list[StatusModel] = (await self.session.scalars(stmt)).all()
        return [
            StatusDM(
                id=status.id,
                name=status.name,
                color_tag=status.color_tag
            )
            for status in statuses
        ]
