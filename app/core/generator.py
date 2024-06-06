from snowflake import SnowflakeGenerator


class Generator:
    __snowflake: SnowflakeGenerator

    def __init__(self, worker_id: int) -> None:
        self.__snowflake = SnowflakeGenerator(worker_id)

    def new_id(self) -> int:
        return int(next(self.__snowflake))


gen: Generator = Generator(1023)
