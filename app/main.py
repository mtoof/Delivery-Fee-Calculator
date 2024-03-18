from fastapi import FastAPI, HTTPException 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from dateutil.parser import isoparse
from . import calculation
from . import consts
from . import time_validation

app = FastAPI(title="Calculate delivery fee")

class CartItems(BaseModel):
    '''
        In here, we use pydantic to validate the input data.
        int = Field(..., gt = 0) means that the input value must be an integer and greater than 0.
    '''
    cart_value: int = Field(..., gt = 0)
    delivery_distance: int = Field(..., gt = 0)
    number_of_items: int = Field(..., gt = 0)
    time: str
    

    @field_validator("time")
    @classmethod
    def check_datetime(cls, value) -> datetime:
        '''
            The following validator is used to check the input data for time item.
            If the input data is not ISO-Format,missing timezone,UTC time and if the year is less than 1999,
            it will raise an HTTPException with status code 400.
            Why 1999? Since the project currency is Euro and Finland joined the Eurozone in 1999.
        '''
        try:
            # isoparse() is used to parse the input data to datetime object.
            time_object = isoparse(value)
        except ValueError:
            raise HTTPException(status_code = 400, detail="Invalid datetime format. It should be ISO format.", 
                                headers={"Content-Type": "application/json"})
        time_validation.invalid_date_time(time_object)
        return time_object

@app.post("/calculate_fee/")
async def calculate_delivery_fee(cart_items:CartItems):
    '''
        If the cart value is greater than or equal to 200 euros, the delivery fee is 0.
        calculate the cart value surcharge
        calculate the distance fee and add it to the delivery fee
        if delivery fee is greater than delivery fee threshold which is 15 euros, return 15 euros
        calculate the extra items fee and add it to the delivery fee
        calculate the rush time fee for Friday, if the time is between 15:00 and 19:00 multiply the delivery fee to 1.2X
    '''
    delivery_fee = 0
    delivery_fee = calculation.total_calculation(cart_items, delivery_fee)

    return JSONResponse(content={"delivery_fee":delivery_fee}, status_code=200)

