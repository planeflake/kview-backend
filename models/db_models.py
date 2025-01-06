from sqlalchemy import Table,Date, Column, Integer, String, Float, DateTime, MetaData, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from datetime import datetime

metadata = MetaData()

customers = Table(
    "customers",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
)

services = Table(
    "services",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", Text, nullable=True)
)

customer_services = Table(
    "customer_services",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", UUID, ForeignKey("customers.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True)
)

aois = Table(
    "aois",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("geom", Geometry("Polygon", srid=4326), nullable=False),
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False),
    Column("country", String, nullable=False),
    Column("service_ids", ARRAY(Integer), nullable=True),
)

ndvi = Table(
    "ndvi",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("aoi_id", Integer, ForeignKey("aoi.id")),
    Column("filepath", String),
    Column("processed_date", DateTime),
    Column("created_at", DateTime),
)

ndvi_statistics = Table(
    "ndvi_statistics",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("aoi_id", Integer, ForeignKey("aoi.id")),
    Column("date", Date),
    Column("min_ndvi", Float),
    Column("max_ndvi", Float),
    Column("median_ndvi", Float),
    Column("created_at", DateTime),
    Column("change", Float, nullable=True)
)

algae_statistics = Table(
    "algae_statistics",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("aoi", Integer, ForeignKey("aoi.id")),
    Column("datetime", DateTime),
    Column("min_value", Float),
    Column("max_value", Float),
    Column("mean_value", Float)
)

vessel = Table(
    "vessels",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("type", String, nullable=True),
    Column("classification", String, nullable=True),
    Column("certainty", String, nullable=True),
    Column("certainty_percentage", Integer, nullable=True),
    Column("geom", Geometry("Point", srid=4326), nullable=False),  # Specify SRID (e.g., 4326 for WGS 84)
    Column("aoi_id", Integer, ForeignKey("aois.id"), nullable=False),
    Column("location_id", Integer, nullable=True),
    Column("order_date", Date)
)

oil_slicks = Table(
    "oil_slicks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False),
    Column("source_vessel", String, nullable=True),
    Column("certainty_percentage", Integer, nullable=True),
    Column("geom", Geometry("POLYGON", srid=4326), nullable=False)
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("description", Text, nullable=True),
    Column("country", String(100), nullable=True),
    Column("iso3",String(3),nullable=True),
    Column("customer_id", Integer, ForeignKey("customers.id"), nullable=True),
    Column("coords",Geometry,nullable=True),
    Column("countrycoords",Geometry,nullable=True)
)