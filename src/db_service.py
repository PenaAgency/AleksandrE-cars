from typing import Generator, List, Optional

import pydantic
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src import models
from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Get session generator to work with the db"""
    session = Session()
    try:
        yield session
    finally:
        session.close()


def create_db_item(
    session: Session,
    scheme: pydantic.BaseModel,
    model: "sqlalchemy.orm.decl_api.DeclarativeMeta",
) -> Optional[SQLAlchemyError]:
    item = model(**scheme.dict())
    session.add(item)
    try:
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        return err


def search_db_items(
    session: Session,
    scheme: pydantic.BaseModel,
    model: "sqlalchemy.orm.decl_api.DeclarativeMeta",
) -> List[models.Base]:
    """get database items by search parameters"""
    item_params = scheme.dict()
    search_params = {}
    for item_param in item_params:
        if item_params[item_param] is not None:
            search_params[item_param] = item_params[item_param]
    items = session.query(model).filter_by(**search_params)
    return [item for item in items]


def get_db_item(
    session: Session,
    model: "sqlalchemy.orm.decl_api.DeclarativeMeta",
    item_id: int,
) -> Optional[models.Base]:
    return session.query(model).get(item_id)


def change_db_item(
    session: Session, scheme: pydantic.BaseModel, item: models.Base
) -> Optional[SQLAlchemyError]:
    """change database item by parameters"""
    schema_params = scheme.dict()
    for schema_param in schema_params:
        if schema_params[schema_param] is not None:
            setattr(item, schema_param, schema_params[schema_param])
    try:
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        return err


def delete_db_item(
    session: Session, item: models.Base
) -> Optional[SQLAlchemyError]:
    try:
        session.delete(item)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        return err
