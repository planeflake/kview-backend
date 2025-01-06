from datetime import datetime as dt_datetime, date as dt_date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import List, Optional
from geoalchemy2 import Geometry
from uuid import UUID
from typing import Dict
from pydantic import BaseModel, ConfigDict
from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping, Point

class LocationBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    country: str
    customer_id: UUID
    iso3: str
    coords: Optional[dict] = None
    countrycoords: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj):
        # If obj is already a dict, use it directly
        if isinstance(obj, dict):
            data = obj
        else:
            # Otherwise, convert from object
            data = {}
            for field in obj.__dict__:
                value = getattr(obj, field)
                if isinstance(value, Geometry) or hasattr(value, 'desc'):
                    # Convert WKB to GeoJSON
                    shape = to_shape(value)
                    data[field] = mapping(shape)
                else:
                    data[field] = value
        
        return super().model_validate(data)

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int = Field(..., description="The unique identifier for the location")

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the customer")

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: str = Field(..., description="The unique identifier (UUID) for the customer")

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the customer")

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: str = Field(..., description="The unique identifier (UUID) for the customer")

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the service")
    description: Optional[str] = Field(None, description="Description of the service")

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int = Field(..., description="The unique identifier for the service")

    class Config:
        from_attributes = True

class AOIResponse(BaseModel):
    id: int
    name: str
    geom: str
    customer_id: UUID
    country: str
    service_ids: Optional[List[int]] = Field(
        None, description="List of service IDs associated with the AOI"
    )

    class Config:
        orm_mode = True

class AOICreate(BaseModel):
    name: str
    geom: str
    customer_id: str
    country: str
    service_ids: Optional[List[int]] = Field(
        None, description="List of service IDs associated with the AOI"
    )

class NDVIStatsCreate(BaseModel):
    aoi_id: int = Field(..., description="The foreign key linking to the AOI table")
    date: dt_date = Field(..., description="The date of the NDVI statistics")
    min_ndvi: float = Field(..., description="The minimum NDVI value for the AOI")
    max_ndvi: float = Field(..., description="The maximum NDVI value for the AOI")
    median_ndvi: float = Field(..., description="The median NDVI value for the AOI")

class NDVIResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the NDVI record")
    aoi_id: int = Field(..., description="The foreign key linking to the AOI table")
    date: dt_date = Field(..., description="The date of the NDVI statistics")
    min_ndvi: float = Field(..., description="The minimum NDVI value for the AOI")
    max_ndvi: float = Field(..., description="The maximum NDVI value for the AOI")
    median_ndvi: float = Field(..., description="The median NDVI value for the AOI")
    created_at: dt_datetime = Field(..., description="The timestamp when the NDVI record was created")
    change: Optional[float] = Field(None, description="The change in NDVI value")

    class Config:
        orm_mode = True

class AlgaeStatsCreate(BaseModel):
    aoi_id: int = Field(..., description="The foreign key linking to the AOI table")
    datetime: dt_datetime = Field(..., description="The datetime of the algae statistics")
    min: float = Field(..., description="The minimum algae value for the AOI")
    max: float = Field(..., description="The maximum algae value for the AOI")
    mean: float = Field(..., description="The mean algae value for the AOI")

class AlgaeStatsResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the algae statistics record")
    aoi: int = Field(..., description="The foreign key linking to the AOI table")
    datetime: dt_datetime = Field(..., description="The datetime of the algae statistics")
    min_value: float = Field(..., description="The minimum algae value for the AOI")
    max_value: float = Field(..., description="The maximum algae value for the AOI")
    mean_value: float = Field(..., description="The mean algae value for the AOI")

    class Config:
        orm_mode = True

class VesselBase(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the vessel")
    type: Optional[str] = Field(None, max_length=100, description="The type of the vessel")
    classification: Optional[str] = Field(None, max_length=100, description="The classification of the vessel")
    certainty: Optional[str] = Field(None, max_length=100, description="The certainty level for vessel data")
    certainty_percentage: Optional[float] = Field(None, description="The percentage indicating certainty level")
    geom: str = Field(..., description="The WKT representation of the vessel's geometry")
    aoi_id: int = Field(..., description="The foreign key linking to the AOI table")
    location_id: int = Field(..., description="The vessel detections location id")
    order_date: dt_date = Field(..., description="The date of the vessel detection")

class VesselCreate(VesselBase):
    pass

class VesselUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="The name of the vessel")
    type: Optional[str] = Field(None, max_length=100, description="The type of the vessel")
    classification: Optional[str] = Field(None, max_length=100, description="The classification of the vessel")
    certainty: Optional[str] = Field(None, max_length=100, description="The certainty level for vessel data")
    certainty_percentage: Optional[float] = Field(None, description="The percentage indicating certainty level")
    geom: Optional[str] = Field(None, description="The WKT representation of the vessel's geometry")
    aoi_id: Optional[int] = Field(None, description="The foreign key linking to the AOI table")

class VesselResponse(BaseModel):
    id: int
    name: str
    type: Optional[str]
    classification: Optional[str]
    certainty: Optional[str]
    certainty_percentage: Optional[float]
    geom: Dict  # Expecting GeoJSON as a Python dictionary
    aoi_id: int
    location_id: int
    order_date: dt_date

    class Config:
        from_model = True

    class Config:
        from_attributes = True

class OilSlickCreate(BaseModel):
    id: int
    type: str
    source_vessel: str
    geom: str  # Accepting WKT or GeoJSON string for input
    certainty_percentage: int

class OilSlickResponse(BaseModel):
    id: int
    type: str
    source_vessel: str
    geom: str  # Define as a dictionary to hold GeoJSON
    certainty_percentage: int

    class Config:
        orm_mode = True