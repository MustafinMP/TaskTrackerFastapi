import db_session
from infrastructure.entities import StatusDM
from infrastructure.repositories import StatusRepository


class StatusService:
    def __init__(self):
        with db_session.create_session() as session:
            self._repository = StatusRepository(session)

    def get_all_statuses(self) -> list[StatusDM]:
        return self._repository.get_all()