from typing import Optional

from pydantic import BaseModel, confloat, conint, constr


class NewDealer(BaseModel):
    dealer_name: constr(max_length=50)
    address: Optional[str]
    phone: Optional[conint(gt=10000000000, lt=20000000000)]


class ChangeDealer(BaseModel):
    dealer_name: Optional[constr(max_length=50)]
    address: Optional[str]
    phone: Optional[conint(gt=10000000000, lt=20000000000)]


class SearchDealer(BaseModel):
    id: Optional[int]
    dealer_name: Optional[constr(max_length=50)]
    address: Optional[str]
    phone: Optional[conint(gt=10000000000, lt=20000000000)]


class NewCar(BaseModel):
    model: constr(max_length=50)
    year: Optional[conint(gt=1950, lt=2023)]
    color: Optional[constr(max_length=50)]
    mileage: Optional[conint(gt=0, lt=1000000)]
    price: Optional[confloat(ge=0, le=10000000)]
    dealer_id: int


class ChangeCar(BaseModel):
    model: Optional[constr(max_length=50)]
    year: Optional[conint(gt=1950, lt=2023)]
    color: Optional[constr(max_length=50)]
    mileage: Optional[conint(gt=0, lt=1000000)]
    price: Optional[confloat(ge=0, le=10000000)]
    dealer_id: Optional[int]


class SearchCar(BaseModel):
    id: Optional[int]
    model: Optional[constr(max_length=50)]
    year: Optional[conint(gt=1950, lt=2023)]
    color: Optional[constr(max_length=50)]
    mileage: Optional[conint(gt=0, lt=1000000)]
    price: Optional[confloat(ge=0, le=10000000)]
    dealer_id: Optional[int]
