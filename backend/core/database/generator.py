from snowflake import SnowflakeGenerator

from backend.core.configs import settings


class IDGenerator:
    __snowflake: SnowflakeGenerator

    def __init__(self, worker_id: int) -> None:
        self.__snowflake = SnowflakeGenerator(worker_id)

    @property
    def id(self) -> int:
        return int(next(self.__snowflake))


gen: IDGenerator = IDGenerator(settings.db.gen.WORKER_ID)