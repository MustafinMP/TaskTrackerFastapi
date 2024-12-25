from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db_models.task_models import StatusModel
from infrastructure.entities.status import StatusDTO


class StatusRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_id(self, status_id: int) -> StatusDTO:
        stmt = select(StatusModel).where(StatusModel.id == status_id)
        status: StatusModel = await self.session.scalar(stmt)
        return StatusDTO(
            id=status.id,
            name=status.name,
            color_tag=status.color_tag
        )

    async def get_all(self) -> list[StatusDTO]:
        stmt = select(StatusModel)
        statuses: list[StatusModel] = (await self.session.scalars(stmt)).all()
        return [
            StatusDTO(
                id=status.id,
                name=status.name,
                color_tag=status.color_tag
            )
            for status in statuses
        ]
