from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src import db_service, models, schemas
from src.logger import logger

app = FastAPI()


def handle_db_exceptions(err: SQLAlchemyError) -> None:
    """creating an exception if any errors occur during
    interaction with the database"""
    if err is not None:

        logger.exception(err)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{err}",
        )


def check_db_item(
    db: Session,
    model: "sqlalchemy.orm.decl_api.DeclarativeMeta",
    item_id: int,
    error_message: str,
) -> Optional[models.Base]:
    """check if item exist in the database"""
    item = db_service.get_db_item(session=db, model=model, item_id=item_id)
    if item is None:
        logger.exception(error_message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_message
        )
    return item


@app.post("/dealer", status_code=status.HTTP_201_CREATED, tags=["Dealer"])
def create_dealer(
    dealer: schemas.NewDealer,
    db: Session = Depends(db_service.get_session),
) -> Dict[str, str]:
    """create dealer instance"""
    err = db_service.create_db_item(db, scheme=dealer, model=models.Dealer)
    handle_db_exceptions(err=err)
    return {"detail": "created"}


@app.post("/dealer/search", tags=["Dealer"])
def get_dealers(
    dealer: schemas.SearchDealer,
    db: Session = Depends(db_service.get_session),
) -> List[models.Dealer]:
    """get dealers by search parameters"""
    return db_service.search_db_items(db, scheme=dealer, model=models.Dealer)


@app.put("/dealer/{dealer_id}", tags=["Dealer"])
async def change_dealer(
    dealer_id: int,
    dealer: schemas.ChangeDealer,
    db: Session = Depends(db_service.get_session),
) -> Dict[str, str]:
    """change dealer instance by its parameters"""
    old_dealer = check_db_item(
        db=db,
        model=models.Dealer,
        item_id=dealer_id,
        error_message="dealer with this ID doesn't exist",
    )
    err = db_service.change_db_item(db, dealer, old_dealer)
    handle_db_exceptions(err)
    return {"detail": "changed"}


@app.delete("/dealer/{dealer_id}", tags=["Dealer"])
async def delete_dealer(
    dealer_id: int,
    db: Session = Depends(db_service.get_session),
) -> Dict[str, str]:
    """delete dealer instance"""
    old_dealer = check_db_item(
        db=db,
        model=models.Dealer,
        item_id=dealer_id,
        error_message="dealer with this ID doesn't exist",
    )
    err = db_service.delete_db_item(db, old_dealer)
    handle_db_exceptions(err=err)
    return {"detail": "deleted"}


@app.post("/car", status_code=status.HTTP_201_CREATED, tags=["Car"])
async def create_car(
    car: schemas.NewCar, db: Session = Depends(db_service.get_session)
) -> Dict[str, str]:
    """create car instance"""
    check_db_item(
        db=db,
        model=models.Dealer,
        item_id=car.dealer_id,
        error_message="dealer with this ID doesn't exist",
    )
    db_service.create_db_item(db, scheme=car, model=models.Car)
    return {"detail": "created"}


@app.post("/car/search", tags=["Car"])
async def get_cars(
    car: schemas.SearchCar, db: Session = Depends(db_service.get_session)
) -> List[models.Car]:
    """get cars by search parameters"""
    return db_service.search_db_items(db, car, models.Car)


@app.put("/car/{car_id}", tags=["Car"])
async def change_car(
    car_id: int,
    car: schemas.ChangeCar,
    db: Session = Depends(db_service.get_session),
) -> Dict[str, str]:
    """change car instance by its parameters"""
    old_car = check_db_item(
        db=db,
        model=models.Car,
        item_id=car_id,
        error_message="car with this ID doesn't exist",
    )
    if car.dealer_id is not None:
        check_db_item(
            db=db,
            model=models.Dealer,
            item_id=car.dealer_id,
            error_message="dealer with this ID doesn't exist",
        )
    err = db_service.change_db_item(db, car, old_car)
    handle_db_exceptions(err=err)
    return {"detail": "changed"}


@app.delete("/car/{car_id}", tags=["Car"])
async def delete_car(
    car_id: int, db: Session = Depends(db_service.get_session)
) -> Dict[str, str]:
    """delete car instance"""
    old_car = check_db_item(
        db=db,
        model=models.Car,
        item_id=car_id,
        error_message="car with this ID doesn't exist",
    )
    db_service.delete_db_item(session=db, item=old_car)
    return {"detail": "deleted"}
