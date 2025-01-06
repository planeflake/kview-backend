from models.api_models import CustomerCreate, CustomerResponse
from fastapi import APIRouter, HTTPException
from models.db_models import customers
from database import database
from typing import List
from logger import logger

customer_router = APIRouter()

@customer_router.get("/", response_model=List[CustomerResponse])
async def get_customers():
    try:
        query = customers.select()
        results = await database.fetch_all(query)
        logger.debug(f"Fetched customers: {results}")
        response_data = [{"id": str(r["id"]), "name": r["name"]} for r in results]
        return response_data
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail="Error fetching customers.")


@customer_router.post("/", response_model=CustomerResponse)
async def create_customer(customer_data: CustomerCreate):
    try:
        query = customers.insert().values(**customer_data.dict()).returning(customers.c.id)
        customer_id = await database.execute(query)
        logger.debug(f"Inserted customer with ID: {customer_id}")
        return {"id": str(customer_id), **customer_data.dict()}
    except Exception as e:
        logger.error(f"Error inserting customer: {e}")
        raise HTTPException(status_code=500, detail="Error creating customer.")

