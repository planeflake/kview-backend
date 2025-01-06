from fastapi import APIRouter, HTTPException
from database import database
from models.db_models import services, customer_services
from models.api_models import ServiceResponse, ServiceCreate
from typing import List
from uuid import UUID
from sqlalchemy.sql import select

service_router = APIRouter()

@service_router.get("/services", response_model=List[ServiceResponse])
async def get_services():
    query = services.select()
    return await database.fetch_all(query)

@service_router.get("/services/{customer_id}", response_model=ServiceResponse)
async def get_services_by_customer(customer_id: UUID):
    query = (
        select([services.c.id, services.c.name])
        .select_from(
            customer_services.join(services, services.c.id == customer_services.c.service_id, isouter=True)
        )
        .where(customer_services.c.customer_id == customer_id)
    )
    # Execute the query and return the result
    result = await database.fetch_all(query)
    return result

@service_router.post("/services", response_model=ServiceResponse)
async def create_service(service: ServiceCreate):
    query = services.insert().values(**service.dict())
    last_record_id = await database.execute(query)
    return {**service.dict(), "id": last_record_id}
