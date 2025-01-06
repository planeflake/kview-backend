import geopandas as gpd

def extract_aoi(file_path: str):
    aoi_data = gpd.read_file(file_path)
    return aoi_data.to_json()

# services/aoi_service.py
def calculate_aoi(geometry):
    """
    Process AOI geometry
    """
    return geometry
