from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import func, Column, TIMESTAMP


@as_declarative()
class Base:
    __name__: str

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
