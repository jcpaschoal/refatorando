from re import A
from typing import Any, Optional, Type, TypeVar, Union, Dict
from fastapi.encoders import jsonable_encoder
from database.models.base_model import Base
from pydantic import BaseModel
from sqlalchemy.orm import Session


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)


class SqlAlchemyRepository:
    
    def create(self, db: Session, db_obj: ModelType ,obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        if  isinstance(obj_in, dict):          
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)
        
        db_obj = db_obj(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
   
    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> None:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if update_data.get(field, None):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


