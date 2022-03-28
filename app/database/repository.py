from typing import Any, Optional, Type, TypeVar
from database.models.base_model import Base
from pydantic import BaseModel
from sqlalchemy.orm import Session


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)


class SqlAlchemyRepository:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == model_id).first()

    def add(self, db: Session, obj_in: CreateSchemaType) -> None:
        db_object = self.model(**obj_in)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> None:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj:
            if update_data.get(field, None):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def remove(self, db: Session, model_id: Any) -> Any:
        db_object = db.query(self.model).get(model_id)
        db.delete(db_object)
        db.commit()
        return model_id



