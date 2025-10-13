from geocube.api.core import make_geocube
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point


data = pd.read_csv(
    '/dmidata/users/clc/SMBMIP/Data/icemasks_others/ant_full_drainagesystem_polygons.txt',
    sep='\s+',  skiprows=7,  # Adjust as needed for header lines
    names=["Latitude", "Longitude", "BasinID"]
)

polygons = []
for basin_id, group in data.groupby("BasinID"):
    coords = list(zip(group["Longitude"], group["Latitude"]))
    polygons.append(Polygon(coords))

# Create a GeoDataFrame with the polygons
zwally_basins = gpd.GeoDataFrame({"BasinID": data["BasinID"].unique()}, geometry=polygons)#.set_index('BasinID')

# Set the CRS to WGS84 (EPSG:4326)
zwally_basins = zwally_basins.set_crs(epsg=4326).to_crs(epsg=3031)

out_grid = make_geocube(
    vector_data=zwally_basins,
    resolution=(-1000, 1000),
)

out_grid.to_netcdf('/dmidata/users/clc/SMBMIP/Data/icemasks_others/zwally_basins_rasterized_1km.nc')
